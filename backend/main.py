from fastapi import FastAPI, HTTPException, Depends
from fastapi import FastAPI, HTTPException, Depends
from .security import (
    RequestIDMiddleware,
    MetricsMiddleware,
    http_error_handler,
    validation_exception_handler,
)
import logging
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException as FastAPIHTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from .database import init_db
from .database import init_db
from .routers import auth, content, dashboard, modules, settings, ai_assistant, events, notifications, portfolio, health
from .config import get_settings
from .logging_config import configure_logging

load_dotenv()
configure_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup
    await init_db()
    yield

app = FastAPI(
    title="Stitch CMS API",
    description="A modular, AI-powered Content Management System",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(content.router, prefix="/api/content", tags=["Content Management"])
app.include_router(modules.router, prefix="/api/modules", tags=["Module Management"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])
app.include_router(ai_assistant.router, prefix="/api/ai", tags=["AI Assistant"])
app.include_router(events.router, prefix="/api/events", tags=["Event Management"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(portfolio.router, tags=["Portfolio"])
app.include_router(health.router, tags=["Health Monitoring"])

# Middleware registration
app.add_middleware(RequestIDMiddleware)
app.add_middleware(MetricsMiddleware)

# Exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(FastAPIHTTPException, http_error_handler)

logger = logging.getLogger("stitch.api")

@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc: Exception):
    logger.error(
        "unhandled_exception",
        exc_info=exc,
        extra={
            "request_id": getattr(request.state, "request_id", None),
            "path": request.url.path,
            "method": request.method,
        },
    )
    return {
        "error": {
            "message": "Internal server error",
            "status": 500,
            "request_id": getattr(request.state, "request_id", None),
        }
    }

@app.get("/")
async def root():
    return {"message": "Stitch CMS API is running"}


