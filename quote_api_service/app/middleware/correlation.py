# import uuid
# import logging
# from contextvars import ContextVar
# from fastapi import Request
# from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
# from starlette.responses import Response

# # Create a context variable to store the correlation ID
# correlation_id = ContextVar("correlation_id", default=None)


# def get_correlation_id() -> str:
#     """Get the current correlation ID from context."""
#     return correlation_id.get()


# class CorrelationMiddleware(BaseHTTPMiddleware):
#     """Middleware to handle correlation IDs for request tracing."""

#     def __init__(self, app, header_name: str = "X-Correlation-ID"):
#         super().__init__(app)
#         self.header_name = header_name

#     async def dispatch(
#         self, request: Request, call_next: RequestResponseEndpoint
#     ) -> Response:
#         # Get correlation ID from header or generate new one
#         request_id = request.headers.get(self.header_name)
#         if not request_id:
#             request_id = str(uuid.uuid4())

#         # Set correlation ID in context
#         token = correlation_id.set(request_id)

#         # Add headers to uvicorn access logger
#         logger = logging.getLogger("uvicorn.access")
#         logger.extra = {
#             "request_headers": {
#                 "X-Correlation-ID": request_id,
#                 **{k.lower(): v for k, v in request.headers.items()},
#             }
#         }

#         try:
#             # Add correlation ID to response headers
#             response = await call_next(request)
#             response.headers[self.header_name] = request_id
#             return response
#         finally:
#             # Reset context
#             correlation_id.reset(token)
