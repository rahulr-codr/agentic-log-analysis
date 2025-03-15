import structlog
import logging
import sys
from opentelemetry.trace import get_current_span
from contextvars import ContextVar

# Create context variable for correlation ID
correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")

# Configure standard logging
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


# Configure structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        add_correlation_id,
        add_otel_context,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Create logger instance
logger = structlog.get_logger()
