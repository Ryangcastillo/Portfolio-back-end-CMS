"""
Error management service for centralized error handling, tracking, and cleanup.
"""

import logging
import traceback
import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
from fastapi import Request

from ..models.error import ErrorRecord, ErrorSeverity, ErrorCategory, ErrorSource, SystemCleanupLog
from ..database import get_db_session
from ..config import get_settings


logger = logging.getLogger("stitch.error_management")


class ErrorManager:
    """Centralized error management service."""
    
    def __init__(self):
        self.settings = get_settings()
    
    async def capture_error(
        self,
        error: Exception,
        request: Optional[Request] = None,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        custom_severity: Optional[ErrorSeverity] = None,
        custom_category: Optional[ErrorCategory] = None
    ) -> ErrorRecord:
        """
        Capture and process an error.
        
        Args:
            error: The exception that occurred
            request: FastAPI request object (if available)
            context: Additional context information
            user_id: User ID associated with the error
            custom_severity: Override automatic severity classification
            custom_category: Override automatic category classification
        
        Returns:
            ErrorRecord: The created error record
        """
        try:
            # Extract error details
            error_type = type(error).__name__
            error_message = str(error)
            stack_trace = traceback.format_exc()
            
            # Classify the error
            severity = custom_severity or self._classify_severity(error, error_type)
            category = custom_category or self._classify_category(error, error_type)
            source = self._determine_source(error, stack_trace)
            
            # Extract request context
            request_context = {}
            request_id = None
            url = None
            method = None
            status_code = None
            
            if request:
                request_id = getattr(request.state, "request_id", None)
                url = str(request.url)
                method = request.method
                
                # Extract additional context from request
                request_context.update({
                    "headers": dict(request.headers),
                    "query_params": dict(request.query_params),
                    "client_host": request.client.host if request.client else None,
                })
            
            # Merge context
            full_context = {**(context or {}), **request_context}
            
            # Create error record
            with get_db_session() as db:
                error_record = ErrorRecord(
                    severity=severity,
                    category=category,
                    source=source,
                    message=error_message,
                    error_type=error_type,
                    stack_trace=stack_trace,
                    context=full_context,
                    request_id=request_id,
                    user_id=uuid.UUID(user_id) if user_id else None,
                    url=url,
                    method=method,
                    status_code=status_code,
                )
                
                # Check for existing similar errors
                existing_error = self._find_similar_error(db, error_record)
                if existing_error:
                    # Update existing error occurrence count
                    existing_error.occurrence_count += 1
                    existing_error.last_occurrence = datetime.utcnow()
                    db.commit()
                    error_record = existing_error
                else:
                    # Create new error record
                    db.add(error_record)
                    db.commit()
                    db.refresh(error_record)
            
            # Log the error
            self._log_error(error_record)
            
            # Send alerts for high-severity errors
            if severity in [ErrorSeverity.CRITICAL, ErrorSeverity.HIGH]:
                await self._send_alerts(error_record)
            
            return error_record
            
        except Exception as e:
            # Fallback logging if error management itself fails
            logger.critical(
                f"Error management system failed: {e}",
                extra={
                    "original_error": str(error),
                    "error_type": type(error).__name__,
                    "management_error": str(e),
                    "management_error_type": type(e).__name__,
                }
            )
            raise
    
    def _classify_severity(self, error: Exception, error_type: str) -> ErrorSeverity:
        """Classify error severity based on error type and characteristics."""
        
        # Critical errors
        if isinstance(error, (SystemExit, KeyboardInterrupt, MemoryError)):
            return ErrorSeverity.CRITICAL
        
        if "database" in str(error).lower() or "connection" in str(error).lower():
            return ErrorSeverity.CRITICAL
            
        # High severity errors
        if isinstance(error, (PermissionError, FileNotFoundError)):
            return ErrorSeverity.HIGH
            
        if error_type in ["HTTPException", "ConnectionError", "TimeoutError"]:
            return ErrorSeverity.HIGH
        
        # Medium severity errors
        if isinstance(error, (ValueError, TypeError, KeyError, IndexError)):
            return ErrorSeverity.MEDIUM
            
        # Low severity for validation and expected errors
        if "validation" in str(error).lower() or "invalid" in str(error).lower():
            return ErrorSeverity.LOW
        
        # Default to medium
        return ErrorSeverity.MEDIUM
    
    def _classify_category(self, error: Exception, error_type: str) -> ErrorCategory:
        """Classify error category based on error type and context."""
        
        # Security-related errors
        if any(term in str(error).lower() for term in ["auth", "permission", "unauthorized", "forbidden", "security"]):
            return ErrorCategory.SECURITY
        
        # External service errors
        if any(term in str(error).lower() for term in ["http", "connection", "timeout", "api", "external"]):
            return ErrorCategory.EXTERNAL_SERVICE
        
        # Database/system errors
        if any(term in str(error).lower() for term in ["database", "sql", "connection", "disk", "memory"]):
            return ErrorCategory.SYSTEM
        
        # Validation/input errors
        if any(term in str(error).lower() for term in ["validation", "invalid", "format", "parse"]):
            return ErrorCategory.USER_INPUT
        
        # Default to business logic
        return ErrorCategory.BUSINESS_LOGIC
    
    def _determine_source(self, error: Exception, stack_trace: str) -> ErrorSource:
        """Determine the source of the error based on stack trace."""
        
        if "backend/" in stack_trace:
            return ErrorSource.BACKEND
        elif "database" in stack_trace.lower() or "sqlalchemy" in stack_trace.lower():
            return ErrorSource.DATABASE
        elif "external" in stack_trace.lower() or "requests" in stack_trace.lower():
            return ErrorSource.EXTERNAL_API
        else:
            return ErrorSource.SYSTEM
    
    def _find_similar_error(self, db: Session, error_record: ErrorRecord) -> Optional[ErrorRecord]:
        """Find similar existing error to avoid duplicates."""
        
        # Look for errors with same type and message in the last hour
        recent_cutoff = datetime.utcnow() - timedelta(hours=1)
        
        similar_error = db.query(ErrorRecord).filter(
            and_(
                ErrorRecord.error_type == error_record.error_type,
                ErrorRecord.message == error_record.message,
                ErrorRecord.last_occurrence > recent_cutoff,
                ErrorRecord.resolved == False
            )
        ).first()
        
        return similar_error
    
    def _log_error(self, error_record: ErrorRecord):
        """Log the error using structured logging."""
        
        log_data = {
            "error_id": str(error_record.id),
            "severity": error_record.severity.value,
            "category": error_record.category.value,
            "source": error_record.source.value,
            "error_type": error_record.error_type,
            "message": error_record.message,
            "request_id": error_record.request_id,
            "user_id": str(error_record.user_id) if error_record.user_id else None,
            "url": error_record.url,
            "method": error_record.method,
            "occurrence_count": error_record.occurrence_count,
        }
        
        if error_record.severity == ErrorSeverity.CRITICAL:
            logger.critical("Critical error occurred", extra=log_data)
        elif error_record.severity == ErrorSeverity.HIGH:
            logger.error("High severity error occurred", extra=log_data)
        elif error_record.severity == ErrorSeverity.MEDIUM:
            logger.warning("Medium severity error occurred", extra=log_data)
        else:
            logger.info("Low severity error occurred", extra=log_data)
    
    async def _send_alerts(self, error_record: ErrorRecord):
        """Send alerts for high-severity errors."""
        
        try:
            # In a real implementation, this would send to Slack, email, PagerDuty, etc.
            alert_message = (
                f"🚨 {error_record.severity.value.upper()} ERROR ALERT\n"
                f"Error ID: {error_record.id}\n"
                f"Type: {error_record.error_type}\n"
                f"Message: {error_record.message}\n"
                f"Source: {error_record.source.value}\n"
                f"Request ID: {error_record.request_id}\n"
                f"Time: {error_record.timestamp}\n"
            )
            
            logger.critical(f"ALERT: {alert_message}", extra={"alert": True, "error_id": str(error_record.id)})
            
            # TODO: Implement actual alerting (Slack, email, etc.)
            
        except Exception as e:
            logger.error(f"Failed to send alert for error {error_record.id}: {e}")
    
    def get_error_statistics(self, db: Session, days: int = 7) -> Dict[str, Any]:
        """Get error statistics for the specified number of days."""
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        errors = db.query(ErrorRecord).filter(
            ErrorRecord.timestamp > cutoff_date
        ).all()
        
        stats = {
            "total_errors": len(errors),
            "by_severity": {},
            "by_category": {},
            "by_source": {},
            "unresolved_count": 0,
            "top_errors": [],
        }
        
        # Count by severity
        for severity in ErrorSeverity:
            stats["by_severity"][severity.value] = len([e for e in errors if e.severity == severity])
        
        # Count by category
        for category in ErrorCategory:
            stats["by_category"][category.value] = len([e for e in errors if e.category == category])
        
        # Count by source
        for source in ErrorSource:
            stats["by_source"][source.value] = len([e for e in errors if e.source == source])
        
        # Count unresolved
        stats["unresolved_count"] = len([e for e in errors if not e.resolved])
        
        # Top errors by occurrence
        error_counts = {}
        for error in errors:
            key = f"{error.error_type}: {error.message[:100]}"
            if key not in error_counts:
                error_counts[key] = {"count": 0, "latest": error.timestamp}
            error_counts[key]["count"] += error.occurrence_count
            if error.timestamp > error_counts[key]["latest"]:
                error_counts[key]["latest"] = error.timestamp
        
        stats["top_errors"] = sorted(
            [{"error": k, "count": v["count"], "latest": v["latest"]} for k, v in error_counts.items()],
            key=lambda x: x["count"],
            reverse=True
        )[:10]
        
        return stats
    
    def resolve_error(self, db: Session, error_id: str, resolved_by: Optional[str] = None, notes: Optional[str] = None):
        """Mark an error as resolved."""
        
        error = db.query(ErrorRecord).filter(ErrorRecord.id == uuid.UUID(error_id)).first()
        if error:
            error.resolved = True
            error.resolved_at = datetime.utcnow()
            if resolved_by:
                error.resolved_by = uuid.UUID(resolved_by)
            if notes:
                error.resolution_notes = notes
            db.commit()
            
            logger.info(f"Error {error_id} marked as resolved", extra={"error_id": error_id, "resolved_by": resolved_by})
            return error
        
        return None


# Global error manager instance
error_manager = ErrorManager()