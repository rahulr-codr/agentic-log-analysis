import uuid
from fastapi import FastAPI, Request
from fastapi.params import Header
import structlog
import logging
import sys
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.trace import get_current_span, SpanContext
from contextvars import ContextVar
from typing import Any, Optional

# Create context variable for correlation ID
correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")
# Configure standard logging
logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)


# Add correlation ID processor
def add_correlation_id(logger, method_name, event_dict):
    corr_id = correlation_id.get()
    if corr_id:
        event_dict["correlation_id"] = corr_id
    return event_dict


# Add OpenTelemetry context processor
def add_otel_context(logger, method_name, event_dict):
    span = get_current_span()
    if span and span.get_span_context().is_valid:
        ctx = span.get_span_context()
        event_dict["trace_id"] = format(ctx.trace_id, "032x")
        event_dict["span_id"] = format(ctx.span_id, "016x")
    return event_dict


# Configure structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        add_otel_context,
        add_correlation_id,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

# Create a logger instance
logger = structlog.get_logger()

app = FastAPI(
    title="Quote API Service",
    description="A service for managing and retrieving quotes",
    version="1.0.0",
)


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    # Get correlation ID from header or generate new one
    corr_id = request.headers.get("X-Correlation-ID")
    if not corr_id:
        corr_id = str(uuid.uuid4())

    # Set correlation ID in context
    correlation_id.set(corr_id)

    # Process request
    response = await call_next(request)

    # Add correlation ID to response header
    response.headers["X-Correlation-ID"] = corr_id

    return response


@app.get("/")
async def root(
    x_correlation_id: Optional[str] = Header(None, alias="X-Correlation-ID"),
):
    logger.info("root_endpoint_called", path="/")
    return {
        "message": "Welcome to the Quote API Service",
        "correlation_id": x_correlation_id,
    }


# Add startup and shutdown event handlers
@app.on_event("startup")
async def startup_event():
    logger.info("application_startup", status="Application starting up")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("application_shutdown", status="Application shutting down")
