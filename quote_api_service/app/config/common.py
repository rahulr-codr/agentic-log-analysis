import logging
import contextvars

correlation_id_ctx = contextvars.ContextVar("correlation_id", default="none")


# Define a custom logging filter to add the correlation id to each log record
class CorrelationIdFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = correlation_id_ctx.get()
        return True
