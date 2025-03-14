import logging
import sys
import os
from typing import Any, Dict
import json
from fastapi.logger import logger as fastapi_logger
from uvicorn.logging import AccessFormatter
from opentelemetry import trace
import contextvars
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from app.config.common import CorrelationIdFilter
from app.core.config import settings


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "path": record.pathname,
        }

        # Add correlation ID if available
        if hasattr(record, "correlation_id"):
            log_data["correlation_id"] = record.correlation_id

        # Add trace context if available
        if hasattr(record, "otelTraceID"):
            log_data["trace_id"] = record.otelTraceID
        if hasattr(record, "otelSpanID"):
            log_data["span_id"] = record.otelSpanID

        # Add any extra attributes
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


class JSONAccessFormatter(AccessFormatter):
    def format(self, record: logging.LogRecord) -> str:
        # Extract all attributes from the record
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add correlation ID if available
        if hasattr(record, "correlation_id"):
            log_data["correlation_id"] = record.correlation_id

        # Add trace context if available
        if hasattr(record, "otelTraceID"):
            log_data["trace_id"] = record.otelTraceID
        if hasattr(record, "otelSpanID"):
            log_data["span_id"] = record.otelSpanID

        # Parse access log message
        try:
            msg_parts = record.getMessage().split()
            log_data.update(
                {
                    "type": "access",
                    "client_host": msg_parts[0],
                    "method": msg_parts[3].strip('"'),
                    "path": msg_parts[4],
                    "protocol": msg_parts[5].rstrip('"'),
                    "status_code": msg_parts[6],
                }
            )
        except (IndexError, AttributeError):
            # If parsing fails, just include the raw message
            log_data["raw_access_log"] = record.getMessage()

        return json.dumps(log_data)


def setup_logging(resource):
    """Set up logging configuration with OTLP export to Loki."""
    # Set up logging with OTLP
    logger_provider = LoggerProvider(resource=resource)
    otlp_log_exporter = OTLPLogExporter(endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_log_exporter))

    # Create correlation ID filter
    correlation_filter = CorrelationIdFilter()

    # Create and configure the OTLP handler with our custom formatter
    otlp_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
    otlp_handler.setFormatter(JSONFormatter())
    otlp_handler.addFilter(correlation_filter)

    # Create console handlers with JSON formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    console_handler.addFilter(correlation_filter)

    # Create access log handlers
    otlp_access_handler = LoggingHandler(
        level=logging.INFO, logger_provider=logger_provider
    )
    otlp_access_handler.setFormatter(JSONAccessFormatter())
    otlp_access_handler.addFilter(correlation_filter)

    console_access_handler = logging.StreamHandler(sys.stdout)
    console_access_handler.setFormatter(JSONAccessFormatter())
    console_access_handler.addFilter(correlation_filter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    for h in root_logger.handlers[:]:  # Remove any existing handlers
        root_logger.removeHandler(h)
    root_logger.addHandler(otlp_handler)
    root_logger.addHandler(console_handler)
    root_logger.addFilter(correlation_filter)

    # Configure FastAPI logger
    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.setLevel(logging.INFO)
    fastapi_logger.addHandler(otlp_handler)
    fastapi_logger.addHandler(console_handler)
    fastapi_logger.addFilter(correlation_filter)

    # Configure uvicorn loggers
    for logger_name in ["uvicorn", "uvicorn.error"]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        logger.addHandler(otlp_handler)
        logger.addHandler(console_handler)
        logger.addFilter(correlation_filter)

    # Configure uvicorn access logger separately with access formatter
    access_logger = logging.getLogger("uvicorn.access")
    access_logger.setLevel(logging.INFO)
    access_logger.addHandler(otlp_access_handler)
    access_logger.addHandler(console_access_handler)

    # Log startup message
    root_logger.info(
        "Logging system initialized",
        extra={"service": "quote_api_service", "log_level": "INFO"},
    )

    return root_logger
