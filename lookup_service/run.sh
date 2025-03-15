opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    --logs_exporter console \
    --service_name lookup_service \
    uvicorn lookup_service.main:app --host 0.0.0.0 --port 8000  --no-access-log --log-level info