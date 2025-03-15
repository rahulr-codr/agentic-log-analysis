export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    --logs_exporter console \
    --service_name quote-api-service \
    uvicorn main:app --host 0.0.0.0 --port 8000  --no-access-log