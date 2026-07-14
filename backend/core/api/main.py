from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from core.api.v1.api import api_router
from core.config import settings
from core.repositories.database import engine, Base
import structlog
import logging
import sys
import sentry_sdk
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

# Error Tracking (Sentry)
sentry_sdk.init(
    dsn="https://mock_dsn@o0.ingest.sentry.io/0",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

# Structured Logs
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
logger = structlog.get_logger()
logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)

# OpenTelemetry
resource = Resource(attributes={SERVICE_NAME: "agentix-backend"})
trace_provider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(trace_provider)

from core.schemas.api_schemas import BaseResponse

from core.repositories.database import engine, Base, init_db

import core.jobs.models
# Create DB tables with retry logic
init_db()
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

from fastapi.responses import JSONResponse
from fastapi import Request
import os

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    
    # Error Sanitization
    if os.getenv("ENVIRONMENT") == "production":
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred."}
        )
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

@app.get("/metrics")
async def metrics():
    # Prometheus Metrics endpoint
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

from core.middleware import SecurityMiddleware
from core.middleware.profiling import EnterpriseProfilerMiddleware
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(EnterpriseProfilerMiddleware, slow_threshold_ms=500.0)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(SecurityMiddleware, rate_limit=200)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "https://agentix.example.com"
    ], # Strictly restrict CORS to frontend domains
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", response_model=BaseResponse)
def health_check():
    logger.info("Health check endpoint accessed")
    return BaseResponse(
        status="success",
        message="OK",
        data={"status": "ok", "project": settings.PROJECT_NAME}
    )

# Trigger reload
