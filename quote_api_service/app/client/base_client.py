from typing import Any, Dict, Optional
import httpx
import structlog

logger = structlog.get_logger()


class BaseHttpClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        """
        Make an HTTP request with logging

        Args:
            method: HTTP method (GET, POST, etc.)
            path: URL path
            params: Query parameters
            json: JSON body
            headers: HTTP headers

        Returns:
            httpx.Response

        Raises:
            httpx.HTTPError: If the request fails
        """
        url = f"{self.base_url}{path}"

        logger.info(
            "http_request", url=url, method=method, params=params, headers=headers
        )

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    headers=headers or {},
                )
                response.raise_for_status()

                logger.info(
                    "http_response",
                    url=url,
                    body=response.json(),
                    method=method,
                    status_code=response.status_code,
                    response_time_ms=response.elapsed.total_seconds() * 1000,
                )

                return response

            except httpx.HTTPError as e:
                logger.error(
                    "http_request_failed",
                    url=url,
                    method=method,
                    error=str(e),
                    status_code=getattr(e.response, "status_code", None)
                    if hasattr(e, "response")
                    else None,
                )
                raise
