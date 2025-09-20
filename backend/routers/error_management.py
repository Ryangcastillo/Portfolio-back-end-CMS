"""
Error management API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import uuid

from ..database import get_db
from ..models.error import ErrorRecord, ErrorSeverity, ErrorCategory, ErrorSource, SystemCleanupLog
from ..services.error_management import error_manager
from ..auth import get_current_user  # Assuming auth is implemented
from pydantic import BaseModel


class ErrorReportRequest(BaseModel):
    """Request model for frontend error reporting."""
    errorId: str
    message: str
    name: str
    stack: Optional[str] = None
    componentStack: Optional[str] = None
    timestamp: str
    url: str
    userAgent: str
    severity: Optional[str] = "medium"
    context: Optional[Dict[str, Any]] = None


router = APIRouter()


class ErrorListParams(BaseModel):
    """Parameters for error listing."""
    severity: Optional[ErrorSeverity] = None
    category: Optional[ErrorCategory] = None
    source: Optional[ErrorSource] = None
    resolved: Optional[bool] = None
    days: Optional[int] = 7
    limit: Optional[int] = 100
    offset: Optional[int] = 0


class ErrorResolveRequest(BaseModel):
    """Request model for resolving errors."""
    notes: Optional[str] = None


@router.post("/report", response_model=Dict[str, Any])
async def report_error(
    error_report: ErrorReportRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """Accept error reports from frontend or external sources."""
    
    try:
        # Create a synthetic exception for the error management system
        class FrontendError(Exception):
            def __init__(self, message: str, error_type: str = "FrontendError"):
                self.message = message
                self.error_type = error_type
                super().__init__(message)
        
        synthetic_error = FrontendError(error_report.message, error_report.name)
        
        # Map severity string to enum
        severity_map = {
            "low": ErrorSeverity.LOW,
            "medium": ErrorSeverity.MEDIUM,
            "high": ErrorSeverity.HIGH,
            "critical": ErrorSeverity.CRITICAL,
            "info": ErrorSeverity.INFO,
        }
        severity = severity_map.get(error_report.severity, ErrorSeverity.MEDIUM)
        
        # Enhance context with frontend-specific information
        enhanced_context = {
            **(error_report.context or {}),
            "frontend_error_id": error_report.errorId,
            "component_stack": error_report.componentStack,
            "user_agent": error_report.userAgent,
            "client_url": error_report.url,
            "client_timestamp": error_report.timestamp,
            "error_source": "frontend",
        }
        
        # Capture the error using the error management system
        error_record = await error_manager.capture_error(
            error=synthetic_error,
            request=request,
            context=enhanced_context,
            custom_severity=severity,
            custom_category=ErrorCategory.USER_INPUT,  # Frontend errors often related to user input
        )
        
        # Override source to frontend
        with get_db_session() as db_session:
            db_error = db_session.query(ErrorRecord).filter(ErrorRecord.id == error_record.id).first()
            if db_error:
                db_error.source = ErrorSource.FRONTEND
                db_error.stack_trace = error_report.stack
                db_session.commit()
        
        return {
            "success": True,
            "error_id": str(error_record.id),
            "message": "Error report received and processed",
            "timestamp": error_record.timestamp.isoformat()
        }
        
    except Exception as e:
        # Avoid infinite recursion by not using error_manager here
        logger.error(f"Failed to process error report: {e}", extra={"error_report": error_report.dict()})
        raise HTTPException(status_code=500, detail="Failed to process error report")


@router.get("/errors", response_model=List[Dict[str, Any]])
async def list_errors(
    request: Request,
    db: Session = Depends(get_db),
    severity: Optional[ErrorSeverity] = Query(None, description="Filter by severity"),
    category: Optional[ErrorCategory] = Query(None, description="Filter by category"),
    source: Optional[ErrorSource] = Query(None, description="Filter by source"),
    resolved: Optional[bool] = Query(None, description="Filter by resolution status"),
    days: int = Query(7, description="Number of days to look back"),
    limit: int = Query(100, description="Maximum number of results"),
    offset: int = Query(0, description="Offset for pagination"),
):
    """List errors with optional filtering."""
    
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        query = db.query(ErrorRecord).filter(ErrorRecord.timestamp > cutoff_date)
        
        # Apply filters
        if severity:
            query = query.filter(ErrorRecord.severity == severity)
        if category:
            query = query.filter(ErrorRecord.category == category)
        if source:
            query = query.filter(ErrorRecord.source == source)
        if resolved is not None:
            query = query.filter(ErrorRecord.resolved == resolved)
        
        # Apply pagination and ordering
        errors = query.order_by(desc(ErrorRecord.timestamp)).offset(offset).limit(limit).all()
        
        return [error.to_dict() for error in errors]
        
    except Exception as e:
        await error_manager.capture_error(e, request=request)
        raise HTTPException(status_code=500, detail="Failed to retrieve errors")


@router.get("/errors/{error_id}", response_model=Dict[str, Any])
async def get_error(
    error_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """Get detailed information about a specific error."""
    
    try:
        error = db.query(ErrorRecord).filter(ErrorRecord.id == uuid.UUID(error_id)).first()
        
        if not error:
            raise HTTPException(status_code=404, detail="Error not found")
        
        return error.to_dict()
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid error ID format")
    except Exception as e:
        await error_manager.capture_error(e, request=request)
        raise HTTPException(status_code=500, detail="Failed to retrieve error")


@router.post("/errors/{error_id}/resolve", response_model=Dict[str, Any])
async def resolve_error(
    error_id: str,
    resolve_request: ErrorResolveRequest,
    request: Request,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_user),  # Uncomment when auth is ready
):
    """Mark an error as resolved."""
    
    try:
        # current_user_id = str(current_user.id) if current_user else None
        current_user_id = None  # Temporary until auth is ready
        
        error = error_manager.resolve_error(
            db=db,
            error_id=error_id,
            resolved_by=current_user_id,
            notes=resolve_request.notes
        )
        
        if not error:
            raise HTTPException(status_code=404, detail="Error not found")
        
        return {
            "success": True,
            "message": "Error marked as resolved",
            "error": error.to_dict()
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid error ID format")
    except Exception as e:
        await error_manager.capture_error(e, request=request)
        raise HTTPException(status_code=500, detail="Failed to resolve error")


@router.get("/errors/summary", response_model=Dict[str, Any])
async def get_error_summary(
    request: Request,
    db: Session = Depends(get_db),
    days: int = Query(7, description="Number of days to analyze"),
):
    """Get error summary and statistics."""
    
    try:
        statistics = error_manager.get_error_statistics(db=db, days=days)
        return {
            "period_days": days,
            "generated_at": datetime.utcnow().isoformat(),
            "statistics": statistics
        }
        
    except Exception as e:
        await error_manager.capture_error(e, request=request)
        raise HTTPException(status_code=500, detail="Failed to generate error summary")


@router.get("/cleanup/history", response_model=List[Dict[str, Any]])
async def get_cleanup_history(
    request: Request,
    db: Session = Depends(get_db),
    days: int = Query(30, description="Number of days to look back"),
    limit: int = Query(50, description="Maximum number of results"),
    offset: int = Query(0, description="Offset for pagination"),
):
    """Get system cleanup operation history."""
    
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        cleanup_logs = db.query(SystemCleanupLog).filter(
            SystemCleanupLog.timestamp > cutoff_date
        ).order_by(desc(SystemCleanupLog.timestamp)).offset(offset).limit(limit).all()
        
        return [log.to_dict() for log in cleanup_logs]
        
    except Exception as e:
        await error_manager.capture_error(e, request=request)
        raise HTTPException(status_code=500, detail="Failed to retrieve cleanup history")


@router.post("/cleanup/run", response_model=Dict[str, Any])
async def run_cleanup(
    request: Request,
    cleanup_type: Optional[str] = Query(None, description="Specific cleanup type to run"),
    # current_user = Depends(get_current_user),  # Uncomment when auth is ready
):
    """Trigger system cleanup operations."""
    
    try:
        # Import cleanup functions
        from ...scripts.error_management.cleanup_system import run_all_cleanup, run_specific_cleanup
        
        if cleanup_type:
            result = await run_specific_cleanup(cleanup_type)
        else:
            result = await run_all_cleanup()
        
        return {
            "success": True,
            "message": "Cleanup operations completed",
            "results": result
        }
        
    except Exception as e:
        await error_manager.capture_error(e, request=request)
        raise HTTPException(status_code=500, detail="Failed to run cleanup operations")


@router.get("/health", response_model=Dict[str, Any])
async def error_management_health(
    request: Request,
    db: Session = Depends(get_db),
):
    """Check the health of the error management system."""
    
    try:
        # Check database connectivity
        recent_errors = db.query(ErrorRecord).filter(
            ErrorRecord.timestamp > datetime.utcnow() - timedelta(minutes=5)
        ).count()
        
        # Check for critical errors in the last hour
        critical_errors = db.query(ErrorRecord).filter(
            and_(
                ErrorRecord.severity == ErrorSeverity.CRITICAL,
                ErrorRecord.timestamp > datetime.utcnow() - timedelta(hours=1)
            )
        ).count()
        
        status = "healthy"
        if critical_errors > 0:
            status = "critical"
        elif recent_errors > 10:  # High error rate
            status = "warning"
        
        return {
            "status": status,
            "recent_errors_5min": recent_errors,
            "critical_errors_1hour": critical_errors,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
    except Exception as e:
        # Don't capture this error to avoid infinite recursion
        return {
            "status": "error",
            "message": f"Health check failed: {str(e)}",
            "timestamp": datetime.utcnow().isoformat(),
        }