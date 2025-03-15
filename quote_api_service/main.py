from fastapi import FastAPI
import structlog
import logging
import sys
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.trace import get_current_span, SpanContext

# Configure standard logging
logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)

# Initialize logging instrumentation
LoggingInstrumentor().instrument(
    set_logging_format=True,
    log_level=logging.INFO,
)


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
        structlog.processors.TimeStamper(fmt="iso"),
        add_otel_context,  # Add our custom processor
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


@app.get("/")
async def root():
    logger.info("root_endpoint_called", path="/")
    return {"message": "Welcome to the Quote API Service"}


# Add startup and shutdown event handlers
@app.on_event("startup")
async def startup_event():
    logger.info("application_startup", status="Application starting up")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("application_shutdown", status="Application shutting down")
