import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict

from .config import get_settings


class JSONLogFormatter(logging.Formatter):
    """Formats logs as single-line JSON objects.

    Standard fields: timestamp, level, logger, message.
    Optional dynamic fields if present on the LogRecord: request_id, path, method,
    status_code, duration_ms.
    Includes exception info when available.
    """

    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        log: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Attach selected extra attributes if they exist
        for attr in [
            "request_id",
            "path",
            "method",
            "status_code",
            "duration_ms",
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


_CONFIGURED = False


def configure_logging(force: bool = False) -> None:
    """Configure root + uvicorn loggers for JSON structured output.

    Idempotent unless force=True.
    """
    global _CONFIGURED
    if _CONFIGURED and not force:
        return

    settings = get_settings()
    level_name = getattr(settings, "log_level", "INFO")
    level = getattr(logging, level_name.upper(), logging.INFO)

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

    _CONFIGURED = True
