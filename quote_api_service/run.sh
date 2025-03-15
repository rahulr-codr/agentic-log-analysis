export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --traces_exporter oltp \
    --metrics_exporter oltp \
    --logs_exporter oltp \
    --service_name quote-api-service \
    uvicorn main:app --host 0.0.0.0 --port 8000  --no-access-log --log-level info