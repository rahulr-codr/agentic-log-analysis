opentelemetry-instrument \
    --traces_exporter none \
    --metrics_exporter none \
    --logs_exporter none \
    --service_name lookup_service \
    uvicorn lookup_service.main:app --host 0.0.0.0 --port 8000 --no-access-log --log-level info