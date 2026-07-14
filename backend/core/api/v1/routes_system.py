from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.repositories.database import get_db, engine
import psutil
import time
import os

router = APIRouter()
START_TIME = time.time()

@router.get("/health")
def health_check():
    """General API health check"""
    return {"status": "ok", "message": "Agentix API is healthy"}

@router.get("/liveness")
def liveness_check():
    """Kubernetes liveness probe"""
    return {"status": "alive"}

@router.get("/readiness")
def readiness_check(db: Session = Depends(get_db)):
    """Kubernetes readiness probe checking database & redis"""
    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"

    redis_status = "ok"
    try:
        import redis
        r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"), socket_timeout=1)
        r.ping()
    except Exception:
        redis_status = "error"
        
    status = "ready" if db_status == "ok" and redis_status == "ok" else "not_ready"
    return {
        "status": status,
        "database": db_status,
        "redis": redis_status
    }

@router.get("/system")
def system_info():
    """Detailed system performance metrics"""
    uptime = time.time() - START_TIME
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        "uptime_seconds": uptime,
        "cpu_usage_percent": cpu_percent,
        "memory_usage_percent": memory.percent,
        "memory_available_mb": memory.available / (1024 * 1024),
        "disk_usage_percent": disk.percent,
        "status": "healthy" if cpu_percent < 90 and memory.percent < 90 else "degraded"
    }
