"""
Error models for the error management system.
Defines database models for error tracking and management.
"""

from sqlalchemy import Column, String, DateTime, Text, Boolean, Enum as SQLEnum, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum
from datetime import datetime
from typing import Optional, Dict, Any

from ..database import Base


class ErrorSeverity(enum.Enum):
    """Error severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ErrorCategory(enum.Enum):
    """Error category classifications."""
    SYSTEM = "system"
    BUSINESS_LOGIC = "business_logic"
    USER_INPUT = "user_input"
    EXTERNAL_SERVICE = "external_service"
    SECURITY = "security"


class ErrorSource(enum.Enum):
    """Error source locations."""
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATABASE = "database"
    EXTERNAL_API = "external_api"
    SYSTEM = "system"


class ErrorRecord(Base):
    """Database model for error records."""
    
    __tablename__ = "error_records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Error classification
    severity = Column(SQLEnum(ErrorSeverity), nullable=False)
    category = Column(SQLEnum(ErrorCategory), nullable=False)
    source = Column(SQLEnum(ErrorSource), nullable=False)
    
    # Error details
    message = Column(Text, nullable=False)
    error_type = Column(String(255), nullable=True)
    stack_trace = Column(Text, nullable=True)
    
    # Context information
    context = Column(JSON, nullable=True)
    request_id = Column(String(255), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    session_id = Column(String(255), nullable=True)
    
    # Request details
    url = Column(String(2048), nullable=True)
    method = Column(String(10), nullable=True)
    status_code = Column(Integer, nullable=True)
    
    # Management
    resolved = Column(Boolean, default=False, nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolved_by = Column(UUID(as_uuid=True), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    
    # Metadata
    occurrence_count = Column(Integer, default=1, nullable=False)
    first_occurrence = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_occurrence = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<ErrorRecord {self.id}: {self.severity.value} - {self.message[:50]}...>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error record to dictionary."""
        return {
            "id": str(self.id),
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "severity": self.severity.value,
            "category": self.category.value,
            "source": self.source.value,
            "message": self.message,
            "error_type": self.error_type,
            "stack_trace": self.stack_trace,
            "context": self.context,
            "request_id": self.request_id,
            "user_id": str(self.user_id) if self.user_id else None,
            "session_id": self.session_id,
            "url": self.url,
            "method": self.method,
            "status_code": self.status_code,
            "resolved": self.resolved,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "resolved_by": str(self.resolved_by) if self.resolved_by else None,
            "resolution_notes": self.resolution_notes,
            "occurrence_count": self.occurrence_count,
            "first_occurrence": self.first_occurrence.isoformat() if self.first_occurrence else None,
            "last_occurrence": self.last_occurrence.isoformat() if self.last_occurrence else None,
        }


class SystemCleanupLog(Base):
    """Database model for tracking system cleanup operations."""
    
    __tablename__ = "system_cleanup_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    cleanup_type = Column(String(100), nullable=False)  # logs, temp_files, error_artifacts, etc.
    operation = Column(String(100), nullable=False)  # archive, delete, move, organize
    
    files_processed = Column(Integer, default=0, nullable=False)
    files_affected = Column(Integer, default=0, nullable=False)
    bytes_processed = Column(Integer, default=0, nullable=False)
    
    success = Column(Boolean, default=True, nullable=False)
    error_message = Column(Text, nullable=True)
    
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    
    details = Column(JSON, nullable=True)  # Additional cleanup details
    
    def __repr__(self):
        return f"<SystemCleanupLog {self.id}: {self.cleanup_type}/{self.operation}>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert cleanup log to dictionary."""
        return {
            "id": str(self.id),
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "cleanup_type": self.cleanup_type,
            "operation": self.operation,
            "files_processed": self.files_processed,
            "files_affected": self.files_affected,
            "bytes_processed": self.bytes_processed,
            "success": self.success,
            "error_message": self.error_message,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": self.duration_seconds,
            "details": self.details,
        }