import base64
import logging
import uuid
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Any
from contextvars import ContextVar

from cryptography.fernet import Fernet, InvalidToken
from fastapi import Depends, HTTPException, status, Request
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .config import get_settings
from .database import User, get_db, RefreshToken
from sqlalchemy import select

settings = get_settings()
logger = logging.getLogger("stitch.security")

# Context variable for request id to enrich logs even outside middleware scope
request_id_ctx: ContextVar[Optional[str]] = ContextVar("request_id", default=None)

# ===== Secret Masking Utility =====
SENSITIVE_KEY_SUBSTRINGS = [
    "api_key",
    "apikey",
    "secret",
    "token",
    "password",
    "key",
]

def mask_secret_value(value: Any) -> Any:
    if value in (None, ""):
        return value
    if isinstance(value, str):
        # Keep last 4 chars if long enough
        if len(value) <= 8:
            return "****"
        return f"****{value[-4:]}"
    return "****"

def mask_secrets(obj: Any, key_hint: Optional[str] = None) -> Any:
    """Recursively mask secret-looking values.

    Rules: if key contains any sensitive substring (case-insensitive) -> mask value.
    For lists we propagate key hint downward.
    """
    try:
        lowered = (key_hint or "").lower()
        should_mask = any(k in lowered for k in SENSITIVE_KEY_SUBSTRINGS)
        if isinstance(obj, dict):
            return {k: mask_secrets(v, k) for k, v in obj.items()}
        if isinstance(obj, list):
            return [mask_secrets(item, key_hint) for item in obj]
        if should_mask:
            return mask_secret_value(obj)
        return obj
    except Exception:  # pragma: no cover - defensive
        return obj

# ===== Encryption Utilities =====
# We derive or generate a Fernet key. If no persistent key provided, we warn (non-durable encryption).
if settings.encryption_key:
    # Expect base64 urlsafe 32 bytes; if a raw password-like string, derive simple padded base64 (not ideal for prod)
    try:
        _raw = settings.encryption_key.encode()
        # Accept either already valid Fernet key or derive one
        try:
            Fernet(settings.encryption_key)
            _fernet_key = settings.encryption_key  # already good
        except Exception:
            _fernet_key = base64.urlsafe_b64encode(_raw.ljust(32, b"0")[:32]).decode()
    except Exception as e:
        raise RuntimeError(f"Invalid ENCRYPTION_KEY provided: {e}")
else:
    _fernet_key = Fernet.generate_key().decode()
    logger.warning("No ENCRYPTION_KEY provided – using volatile key (secrets won't persist across restarts)")

fernet = Fernet(_fernet_key)

def encrypt_value(value: str) -> str:
    if value is None:
        return value
    return fernet.encrypt(value.encode()).decode()

def decrypt_value(token: str) -> str:
    if token is None:
        return token
    try:
        return fernet.decrypt(token.encode()).decode()
    except InvalidToken:
        logger.error("Failed to decrypt value – invalid token")
        raise HTTPException(status_code=400, detail="Corrupted encrypted value")

# ===== RBAC Dependency =====
from fastapi import Depends
from .auth import get_current_user

def requires_roles(*roles: str):
    def wrapper(user: User = Depends(get_current_user)):
        if roles and user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return user
    return wrapper

class RefreshTokenData:
    def __init__(self, token: str, user_id: int, family_id: str, expires_at: datetime):
        self.token = token
        self.user_id = user_id
        self.family_id = family_id
        self.expires_at = expires_at

def _generate_refresh_token() -> str:
    return secrets.token_urlsafe(48)

def _hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

async def create_refresh_token(db: AsyncSession, user_id: int) -> RefreshTokenData:
    token = _generate_refresh_token()
    family_id = uuid.uuid4().hex
    expires_at = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    db.add(RefreshToken(user_id=user_id, token_hash=_hash(token), family_id=family_id, expires_at=expires_at))
    await db.commit()
    return RefreshTokenData(token=token, user_id=user_id, family_id=family_id, expires_at=expires_at)

async def rotate_refresh_token(db: AsyncSession, token: str) -> Optional[RefreshTokenData]:
    hashed = _hash(token)
    res = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == hashed))
    rt: Optional[RefreshToken] = res.scalar_one_or_none()
    if not rt or rt.revoked_at is not None or rt.expires_at < datetime.utcnow():
        return None
    # Revoke old
    rt.revoked_at = datetime.utcnow()
    new_raw = _generate_refresh_token()
    expires_at = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    db.add(RefreshToken(user_id=rt.user_id, token_hash=_hash(new_raw), family_id=rt.family_id, expires_at=expires_at))
    await db.commit()
    return RefreshTokenData(token=new_raw, user_id=rt.user_id, family_id=rt.family_id, expires_at=expires_at)

async def revoke_refresh_token(db: AsyncSession, token: str) -> bool:
    hashed = _hash(token)
    res = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == hashed))
    rt: Optional[RefreshToken] = res.scalar_one_or_none()
    if not rt or rt.revoked_at is not None:
        return False
    rt.revoked_at = datetime.utcnow()
    await db.commit()
    return True

async def revoke_family(db: AsyncSession, family_id: str) -> int:
    res = await db.execute(select(RefreshToken).where(RefreshToken.family_id == family_id, RefreshToken.revoked_at.is_(None)))
    items = res.scalars().all()
    now = datetime.utcnow()
    for item in items:
        item.revoked_at = now
    if items:
        await db.commit()
    return len(items)

# ===== JWT Helpers (extended claims) =====

def create_access_token_claims(user: User):
    return {
        "sub": str(user.id),
        "uname": user.username,
        "role": user.role,
        "aud": settings.token_audience,
        "iss": settings.token_issuer,
        "iat": datetime.utcnow().timestamp()
    }

# ===== Request ID & Logging Middleware =====
from starlette.middleware.base import BaseHTTPMiddleware

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        # set context var for downstream logging
        token = request_id_ctx.set(request_id)
        try:
            response = await call_next(request)
        finally:
            # reset context var to previous value to avoid leaking across requests
            request_id_ctx.reset(token)
        response.headers["X-Request-ID"] = request_id
        return response

# ===== Metrics Middleware (basic stub) =====
import time

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = None
        try:
            response = await call_next(request)
            return response
        finally:
            duration = (time.perf_counter() - start) * 1000
            path = request.url.path
            status_code = getattr(response, "status_code", None)
            logger.info(
                "request_completed",
                extra={
                    "request_id": getattr(request.state, "request_id", None),
                    "path": path,
                    "method": request.method,
                    "status_code": status_code,
                    "duration_ms": round(duration, 2),
                },
            )

# ===== Global Error Handling Utilities =====
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

async def http_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "status": exc.status_code,
                "request_id": getattr(request.state, "request_id", None)
            }
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "message": "Validation failed",
                "details": exc.errors(),
                "request_id": getattr(request.state, "request_id", None)
            }
        },
    )

# Generic catch-all can be added in app startup if desired
