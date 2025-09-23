import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from contextvars import ContextVar

import structlog
from structlog.typing import FilteringBoundLogger

from .config import get_settings

# Context variable for request ID to be accessible throughout the request lifecycle
request_id_ctx: ContextVar[Optional[str]] = ContextVar("request_id", default=None)

# Context variable for performance tracking
request_start_time_ctx: ContextVar[Optional[float]] = ContextVar("request_start_time", default=None)

class JSONLogFormatter(logging.Formatter):
    """Formats logs as single-line JSON objects.

    Standard fields: timestamp, level, logger, message.
    Optional dynamic fields if present on the LogRecord: request_id, path, method,
    status_code, duration_ms, performance metrics.
    Includes exception info when available.
    """

    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        log: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Attach request context if available
        request_id = request_id_ctx.get()
        if request_id:
            log["request_id"] = request_id

        # Attach selected extra attributes if they exist
        for attr in [
            "request_id",
            "path", 
            "method",
            "status_code",
            "duration_ms",
            "performance_metrics",
            "operation",
            "user_id",
            "module",
            "external_service",
            "db_query_time",
            "cache_hit",
        ]:
            value = getattr(record, attr, None)
            if value is not None:
                log[attr] = value

        if record.exc_info:
            # Exception tuple -> formatted string via built-in formatter
            log["exception"] = self.formatException(record.exc_info)
        if record.stack_info:
            log["stack"] = self.formatStack(record.stack_info)

        return json.dumps(log, ensure_ascii=False)

def add_request_id(logger: FilteringBoundLogger, method_name: str, event_dict: dict) -> dict:
    """Add request ID from context to all log messages"""
    request_id = request_id_ctx.get()
    if request_id:
        event_dict["request_id"] = request_id
    return event_dict

def add_performance_context(logger: FilteringBoundLogger, method_name: str, event_dict: dict) -> dict:
    """Add performance tracking context to logs"""
    start_time = request_start_time_ctx.get()
    if start_time:
        current_time = time.perf_counter()
        event_dict["request_duration_ms"] = round((current_time - start_time) * 1000, 2)
    return event_dict

def slow_operation_processor(logger: FilteringBoundLogger, method_name: str, event_dict: dict) -> dict:
    """Highlight slow operations in logs"""
    duration = event_dict.get("duration_ms")
    if duration and isinstance(duration, (int, float)):
        if duration > 1000:  # More than 1 second
            event_dict["slow_operation"] = True
            event_dict["alert_level"] = "warning"
        elif duration > 5000:  # More than 5 seconds
            event_dict["alert_level"] = "critical" 
    
    # Mark slow database queries
    db_time = event_dict.get("db_query_time")
    if db_time and isinstance(db_time, (int, float)) and db_time > 500:  # More than 500ms
        event_dict["slow_db_query"] = True
        
    return event_dict

def configure_structlog() -> None:
    """Configure structlog with enhanced processors"""
    timestamper = structlog.processors.TimeStamper(fmt="iso")
    
    shared_processors = [
        # Add context processors
        add_request_id,
        add_performance_context,
        slow_operation_processor,
        
        # Standard processors
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        timestamper,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    # Configure structlog
    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

_CONFIGURED = False

def configure_logging(force: bool = False) -> None:
    """Configure root + uvicorn loggers for JSON structured output with structlog enhancements.

    Idempotent unless force=True.
    """
    global _CONFIGURED
    if _CONFIGURED and not force:
        return

    settings = get_settings()
    level_name = getattr(settings, "log_level", "INFO")
    level = getattr(logging, level_name.upper(), logging.INFO)

    # Configure structlog first
    configure_structlog()

    # Root logger
    root = logging.getLogger()
    root.setLevel(level)
    # Remove any existing handlers (avoid duplicate lines)
    for h in list(root.handlers):
        root.removeHandler(h)

    handler = logging.StreamHandler()
    handler.setFormatter(JSONLogFormatter())
    root.addHandler(handler)

    # Align common FastAPI/Uvicorn loggers
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(name)
        logger.handlers = []
        logger.propagate = True  # let root handle formatting
        logger.setLevel(level)

    # Set specific log levels for development vs production
    environment = getattr(settings, "environment", "development")
    if environment == "development":
        # More verbose logging in development
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)  # Reduce SQL noise
    else:
        # Production logging - reduce noise
        logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
        logging.getLogger("asyncio").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)

    _CONFIGURED = True

# Convenience functions for getting structured loggers
def get_logger(name: str) -> FilteringBoundLogger:
    """Get a structlog logger with the given name"""
    return structlog.get_logger(name)

def get_request_logger(operation: str = "") -> FilteringBoundLogger:
    """Get a structlog logger with request context"""
    logger = structlog.get_logger("stitch.request")
    if operation:
        logger = logger.bind(operation=operation)
    return logger

def get_db_logger() -> FilteringBoundLogger:
    """Get a structlog logger for database operations"""
    return structlog.get_logger("stitch.database")

def get_performance_logger() -> FilteringBoundLogger:
    """Get a structlog logger for performance monitoring"""
    return structlog.get_logger("stitch.performance")

def get_security_logger() -> FilteringBoundLogger:
    """Get a structlog logger for security events"""
    return structlog.get_logger("stitch.security")

# Performance tracking decorators and context managers
import functools
import asyncio

def log_performance(operation: str, threshold_ms: float = 100.0):
    """Decorator to log performance metrics for functions"""
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            logger = get_performance_logger()
            start_time = time.perf_counter()
            
            try:
                result = await func(*args, **kwargs)
                duration = (time.perf_counter() - start_time) * 1000
                
                if duration > threshold_ms:
                    logger.warning(
                        "slow_operation_detected",
                        operation=operation,
                        duration_ms=round(duration, 2),
                        threshold_ms=threshold_ms
                    )
                else:
                    logger.info(
                        "operation_completed",
                        operation=operation,
                        duration_ms=round(duration, 2)
                    )
                
                return result
            except Exception as e:
                duration = (time.perf_counter() - start_time) * 1000
                logger.error(
                    "operation_failed",
                    operation=operation,
                    duration_ms=round(duration, 2),
                    error=str(e)
                )
                raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            logger = get_performance_logger()
            start_time = time.perf_counter()
            
            try:
                result = func(*args, **kwargs)
                duration = (time.perf_counter() - start_time) * 1000
                
                if duration > threshold_ms:
                    logger.warning(
                        "slow_operation_detected",
                        operation=operation,
                        duration_ms=round(duration, 2),
                        threshold_ms=threshold_ms
                    )
                else:
                    logger.info(
                        "operation_completed",
                        operation=operation,
                        duration_ms=round(duration, 2)
                    )
                
                return result
            except Exception as e:
                duration = (time.perf_counter() - start_time) * 1000
                logger.error(
                    "operation_failed",
                    operation=operation,
                    duration_ms=round(duration, 2),
                    error=str(e)
                )
                raise
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

class PerformanceContext:
    """Context manager for tracking operation performance"""
    
    def __init__(self, operation: str, logger: Optional[FilteringBoundLogger] = None, threshold_ms: float = 100.0):
        self.operation = operation
        self.logger = logger or get_performance_logger()
        self.threshold_ms = threshold_ms
        self.start_time = None
        
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = (time.perf_counter() - self.start_time) * 1000
            
            if exc_type:
                self.logger.error(
                    "operation_failed",
                    operation=self.operation,
                    duration_ms=round(duration, 2),
                    error=str(exc_val) if exc_val else "Unknown error"
                )
            elif duration > self.threshold_ms:
                self.logger.warning(
                    "slow_operation_detected", 
                    operation=self.operation,
                    duration_ms=round(duration, 2),
                    threshold_ms=self.threshold_ms
                )
            else:
                self.logger.info(
                    "operation_completed",
                    operation=self.operation,
                    duration_ms=round(duration, 2)
                )
