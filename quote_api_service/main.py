import uuid
from fastapi import FastAPI, Request
from fastapi.params import Header
import structlog
import logging
import sys
from opentelemetry.trace import get_current_span, SpanContext
from contextvars import ContextVar
from typing import Any, Optional

# Create context variable for correlation ID
correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(
    logging.Formatter("%(message)s")
)  # Just output the raw message (JSON from structlog)

logging.root.setLevel(logging.INFO)
logging.root.addHandler(handler)


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


structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,  # Merge context vars like correlation_id
        structlog.processors.add_log_level,
        add_correlation_id,
        add_otel_context,
        # Adds "level" to logs
        structlog.processors.TimeStamper(fmt="iso"),  # Timestamp logs
        structlog.processors.dict_tracebacks,  # Format exceptions as dicts
        structlog.processors.JSONRenderer(),  # Output as JSON
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


# Get a structlog-only logger
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
    logger.info("root_endpoint_called")
    return {
        "message": "Welcome to the Quote API Service",
        "correlation_id": x_correlation_id,
    }
