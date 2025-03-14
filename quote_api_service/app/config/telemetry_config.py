import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.propagate import set_global_textmap
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from fastapi import FastAPI
from sqlalchemy.engine import Engine
from app.core.config import settings
from app.config.logging_config import setup_logging


def setup_telemetry(app: FastAPI, engine: Engine = None) -> None:
    """Set up OpenTelemetry with automatic instrumentation."""
    # Set up W3C TraceContext propagator for distributed tracing
    set_global_textmap(TraceContextTextMapPropagator())

    # Create a resource with service name
    resource = Resource.create({"service.name": settings.PROJECT_NAME})

    # Set up the trace provider with the resource
    provider = TracerProvider(resource=resource)

    # Create and register OTLP exporter
    otlp_exporter = OTLPSpanExporter(endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT)
    span_processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(span_processor)

    # Set the tracer provider
    trace.set_tracer_provider(provider)

    # Set up logging with OTLP
    setup_logging(resource)

    # Set up automatic instrumentation
    FastAPIInstrumentor.instrument_app(
        app,
        tracer_provider=provider,
        excluded_urls="health,metrics",  # Exclude health check endpoints
    )

    if engine is not None:
        SQLAlchemyInstrumentor().instrument(
            engine=engine,
            tracer_provider=provider,
        )

    LoggingInstrumentor().instrument(
        tracer_provider=provider,
        set_logging_format=True,
        log_level=settings.LOG_LEVEL,
    )

    # Create a tracer for manual instrumentation if needed
    tracer = trace.get_tracer(__name__)
    return tracer
