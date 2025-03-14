import logging
import sys
import os
from typing import Any, Dict
import json
from fastapi.logger import logger as fastapi_logger
from uvicorn.logging import AccessFormatter
from opentelemetry import trace
import contextvars

from app.config.common import CorrelationIdFilter


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "correlation_id": record.correlation_id
            if hasattr(record, "correlation_id")
            else None,
        }

        # Add OpenTelemetry attributes with correct names
        if hasattr(record, "otelTraceID"):
            trace_id = getattr(record, "otelTraceID")
            if trace_id != "0":  # Only add if there's a valid trace
                log_data["trace_id"] = trace_id
        if hasattr(record, "otelSpanID"):
            span_id = getattr(record, "otelSpanID")
            if span_id != "0":  # Only add if there's a valid span
                log_data["span_id"] = span_id
        if hasattr(record, "otelTraceSampled"):
            log_data["sampled"] = getattr(record, "otelTraceSampled")

        if hasattr(record, "extra"):
            log_data.update(record.extra)

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


class JSONAccessFormatter(AccessFormatter):
    def format(self, record: logging.LogRecord) -> str:
        # Parse the original access log message
        original_message = record.getMessage()
        # Example message: "127.0.0.1:58363 - "GET /api/v1/quotes/?skip=0&limit=100 HTTP/1.1" 200 OK"

        # Split the message into parts
        parts = original_message.split(" - ")
        client_addr = parts[0] if len(parts) > 1 else "unknown"

        # Parse the request part
        request_part = parts[1] if len(parts) > 1 else ""
        # Remove quotes from the request part
        request_part = request_part.strip('"')
        request_parts = request_part.split(" ")

        log_data: Dict[str, Any] = {
            "timestamp": self.formatTime(record),
            "level": "INFO",
            "type": "access",
            "client_host": client_addr,
            "method": request_parts[0],
            "path": request_parts[1],
            "protocol": request_parts[2].replace('"', ""),
            "status_code": request_parts[3],
            "correlation_id": record.correlation_id,
        }

        # Add OpenTelemetry attributes with correct names
        if hasattr(record, "otelTraceID"):
            trace_id = getattr(record, "otelTraceID")
            if trace_id != "0":  # Only add if there's a valid trace
                log_data["trace_id"] = trace_id
        if hasattr(record, "otelSpanID"):
            span_id = getattr(record, "otelSpanID")
            if span_id != "0":  # Only add if there's a valid span
                log_data["span_id"] = span_id
        if hasattr(record, "otelTraceSampled"):
            log_data["sampled"] = getattr(record, "otelTraceSampled")

        return json.dumps(log_data)


def setup_logging(level: str = None) -> logging.Logger:
    """Configure logging with JSON formatting and OpenTelemetry trace and span IDs."""
    # Get log level from environment variable or use default
    log_level = level or os.getenv("LOG_LEVEL", "INFO")
    correlation_id_filter = CorrelationIdFilter()
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers = []
    # root_logger.addFilter(correlation_id_filter)

    # Create console handler with JSON formatter
    console_handler = logging.StreamHandler()
    console_handler.addFilter(correlation_id_filter)
    formatter = JSONFormatter()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    # Configure FastAPI logger
    fastapi_logger.setLevel(log_level)
    fastapi_logger.handlers = []
    # fastapi_logger.addFilter(CorrelationIdFilter())
    fastapi_logger.addHandler(console_handler)

    # Configure uvicorn access logger
    access_logger = logging.getLogger("uvicorn.access")
    access_logger.setLevel(log_level)
    # access_logger.addFilter(CorrelationIdFilter())
    access_logger.handlers = []
    access_handler = logging.StreamHandler(sys.stdout)
    access_handler.setFormatter(JSONAccessFormatter())
    access_handler.addFilter(correlation_id_filter)
    access_logger.addHandler(access_handler)

    # Log startup message
    root_logger.info(
        "Logging system initialized",
        extra={"service": "quote_api_service", "log_level": log_level},
    )

    return root_logger
