"""
Health Check Endpoints
Implements TASK-008: Create Health Check Endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from pydantic import BaseModel
from typing import Dict, Any, Optional
import asyncio
import psutil
import time
import httpx
import logging
from datetime import datetime, timezone

from ..database import get_db, engine
from ..config import get_settings
from ..logging_config import get_logger, log_performance, PerformanceContext

logger = get_logger("stitch.health")
router = APIRouter()

class HealthStatus(BaseModel):
    status: str  # "healthy", "degraded", "unhealthy"
    timestamp: datetime
    version: str
    uptime: Optional[float] = None
    checks: Dict[str, Any]

class DatabaseHealth(BaseModel):
    status: str
    response_time_ms: Optional[float] = None
    error: Optional[str] = None

class ExternalServiceHealth(BaseModel):
    name: str
    status: str
    response_time_ms: Optional[float] = None
    error: Optional[str] = None

class ResourceUsage(BaseModel):
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_total_mb: float

# Track application start time for uptime calculation
_app_start_time = time.time()

@log_performance("database_health_check", threshold_ms=50.0)
async def check_database_health(db: AsyncSession) -> DatabaseHealth:
    """Check database connectivity and response time"""
    try:
        start_time = time.time()
        # Simple query to test database connectivity
        result = await db.execute(text("SELECT 1 as health_check"))
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        result.fetchone()  # Remove await - fetchone() is synchronous
        return DatabaseHealth(
            status="healthy",
            response_time_ms=round(response_time, 2)
        )
    except Exception as e:
        logger.error("database_health_check_failed", error=str(e), duration_ms=round((time.time() - start_time) * 1000, 2))
        return DatabaseHealth(
            status="unhealthy",
            error=str(e)
        )

async def check_external_services() -> list[ExternalServiceHealth]:
    """Check external service dependencies"""
    settings = get_settings()
    services = []
    timeout = httpx.Timeout(10.0)  # 10 second timeout
    
    # Check AI providers if configured
    external_checks = []
    
    if settings.openai_api_key:
        external_checks.append(("OpenAI", "https://api.openai.com/v1/models"))
    
    if settings.openrouter_api_key:
        external_checks.append(("OpenRouter", "https://openrouter.ai/api/v1/models"))
    
    async def check_service(name: str, url: str) -> ExternalServiceHealth:
        try:
            start_time = time.time()
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url)
                response_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    logger.debug("external_service_healthy", service=name, response_time_ms=round(response_time, 2))
                    return ExternalServiceHealth(
                        name=name,
                        status="healthy",
                        response_time_ms=round(response_time, 2)
                    )
                else:
                    logger.warning("external_service_degraded", service=name, status_code=response.status_code, response_time_ms=round(response_time, 2))
                    return ExternalServiceHealth(
                        name=name,
                        status="degraded",
                        response_time_ms=round(response_time, 2),
                        error=f"HTTP {response.status_code}"
                    )
        except asyncio.TimeoutError:
            return ExternalServiceHealth(
                name=name,
                status="unhealthy",
                error="Timeout"
            )
        except Exception as e:
            return ExternalServiceHealth(
                name=name,
                status="unhealthy",
                error=str(e)
            )
    
    # Run all external service checks concurrently
    if external_checks:
        tasks = [check_service(name, url) for name, url in external_checks]
        services = await asyncio.gather(*tasks, return_exceptions=False)
    
    return services

def get_resource_usage() -> ResourceUsage:
    """Get current CPU and memory usage"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        return ResourceUsage(
            cpu_percent=round(cpu_percent, 1),
            memory_percent=round(memory.percent, 1),
            memory_used_mb=round(memory.used / (1024 * 1024), 1),
            memory_total_mb=round(memory.total / (1024 * 1024), 1)
        )
    except Exception as e:
        logger.error("resource_usage_check_failed", error=str(e))
        # Return default values if psutil fails
        return ResourceUsage(
            cpu_percent=0.0,
            memory_percent=0.0,
            memory_used_mb=0.0,
            memory_total_mb=0.0
        )

@router.get("/health", response_model=HealthStatus)
async def comprehensive_health_check(db: AsyncSession = Depends(get_db)):
    """
    Comprehensive health check endpoint
    Returns detailed system health including database, external services, and resources
    """
    start_time = time.time()
    uptime = time.time() - _app_start_time
    
    # Perform all health checks
    db_health = await check_database_health(db)
    external_services = await check_external_services()
    resources = get_resource_usage()
    
    # Determine overall system status
    overall_status = "healthy"
    
    # Check database status
    if db_health.status == "unhealthy":
        overall_status = "unhealthy"
    elif db_health.status == "degraded" and overall_status != "unhealthy":
        overall_status = "degraded"
    
    # Check external services
    for service in external_services:
        if service.status == "unhealthy":
            overall_status = "unhealthy"
        elif service.status == "degraded" and overall_status != "unhealthy":
            overall_status = "degraded"
    
    # Check resource usage thresholds
    if resources.memory_percent > 90 or resources.cpu_percent > 90:
        if overall_status == "healthy":
            overall_status = "degraded"
    
    checks = {
        "database": db_health.dict(),
        "external_services": [service.dict() for service in external_services],
        "resources": resources.dict(),
        "response_time_ms": round((time.time() - start_time) * 1000, 2)
    }
    
    health_status = HealthStatus(
        status=overall_status,
        timestamp=datetime.now(timezone.utc),
        version="1.0.0",
        uptime=round(uptime, 1),
        checks=checks
    )
    
    # Return appropriate HTTP status code based on health
    if overall_status == "unhealthy":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=health_status.dict()
        )
    elif overall_status == "degraded":
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=health_status.dict()
        )
    
    return health_status

@router.get("/health/quick")
async def quick_health_check():
    """
    Quick health check endpoint for load balancers
    Returns minimal response for basic availability check
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc),
        "version": "1.0.0"
    }

@router.get("/health/database")
async def database_health_check(db: AsyncSession = Depends(get_db)):
    """
    Database-specific health check
    """
    db_health = await check_database_health(db)
    
    if db_health.status == "unhealthy":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=db_health.dict()
        )
    
    return db_health

@router.get("/health/resources")
async def resources_health_check():
    """
    System resources health check
    """
    resources = get_resource_usage()
    
    # Determine status based on resource usage
    status_value = "healthy"
    if resources.memory_percent > 90 or resources.cpu_percent > 90:
        status_value = "critical"
    elif resources.memory_percent > 80 or resources.cpu_percent > 80:
        status_value = "warning"
    
    response = {
        "status": status_value,
        "resources": resources.dict(),
        "timestamp": datetime.now(timezone.utc)
    }
    
    if status_value == "critical":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=response
        )
    
    return response