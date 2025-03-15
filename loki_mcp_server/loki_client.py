from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
import httpx
from pydantic import BaseModel, Field


class LokiQuery(BaseModel):
    """Model for Loki query parameters."""

    query: str
    limit: Optional[int] = Field(default=100, ge=1, le=5000)
    start: Optional[int] = None  # Nanosecond Unix timestamp
    end: Optional[int] = None  # Nanosecond Unix timestamp
    direction: Optional[str] = Field(default="backward", pattern="^(forward|backward)$")
    regexp: Optional[str] = None


class LokiClient:
    """Client for making HTTP requests to Loki."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize the Loki client.

        Args:
            base_url: Base URL of the Loki server (e.g., "http://localhost:3100")
            timeout: Request timeout in seconds
            headers: Optional headers to include in requests
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = headers or {}
        self._client = httpx.Client(
            base_url=self.base_url, timeout=self.timeout, headers=self.headers
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def query_range(
        self,
        query: str,
        start: Optional[int] = None,  # Nanosecond Unix timestamp
        end: Optional[int] = None,  # Nanosecond Unix timestamp
        step: Optional[str] = None,
        limit: int = 100,
        direction: str = "backward",
    ) -> Dict:
        """
        Query Loki for logs within a time range.

        Args:
            query: LogQL query string
            start: Start time in nanosecond Unix timestamp
            end: End time in nanosecond Unix timestamp
            step: Query resolution step width (e.g., "5m")
            limit: Maximum number of entries to return
            direction: Sort direction ("forward" or "backward")

        Returns:
            Dict containing the query results
        """
        params = {
            "query": query,
            "start": str(start),
            "end": str(end),
            "limit": limit,
            "direction": direction,
        }
        if step:
            params["step"] = step

        response = self._client.get("/loki/api/v1/query_range", params=params)
        response.raise_for_status()
        return response.json()

    def query(
        self,
        query: str,
        limit: int = 100,
        time: Optional[int] = None,  # Nanosecond Unix timestamp
        direction: str = "backward",
    ) -> Dict:
        """
        Query Loki for logs at a specific time.

        Args:
            query: LogQL query string
            limit: Maximum number of entries to return
            time: Query time in nanosecond Unix timestamp
            direction: Sort direction ("forward" or "backward")

        Returns:
            Dict containing the query results
        """
        params = {"query": query, "limit": limit, "direction": direction}
        if time:
            params["time"] = str(time)

        response = self._client.get("/loki/api/v1/query", params=params)
        response.raise_for_status()
        return response.json()

    def labels(
        self,
        start: Optional[int] = None,  # Nanosecond Unix timestamp
        end: Optional[int] = None,  # Nanosecond Unix timestamp
    ) -> List[str]:
        """
        Get all label names.

        Args:
            start: Start time in nanosecond Unix timestamp
            end: End time in nanosecond Unix timestamp

        Returns:
            List of label names
        """
        params = {}
        if start:
            params["start"] = str(start)
        if end:
            params["end"] = str(end)

        response = self._client.get("/loki/api/v1/labels", params=params)
        response.raise_for_status()
        return response.json()["data"]

    def label_values(
        self,
        label: str,
        start: Optional[int] = None,  # Nanosecond Unix timestamp
        end: Optional[int] = None,  # Nanosecond Unix timestamp
    ) -> List[str]:
        """
        Get all values for a specific label.

        Args:
            label: Label name
            start: Start time in nanosecond Unix timestamp
            end: End time in nanosecond Unix timestamp

        Returns:
            List of label values
        """
        params = {}
        if start:
            params["start"] = str(start)
        if end:
            params["end"] = str(end)

        response = self._client.get(f"/loki/api/v1/label/{label}/values", params=params)
        response.raise_for_status()
        return response.json()["data"]

    def series(
        self,
        match: List[str],
        start: Optional[int] = None,  # Nanosecond Unix timestamp
        end: Optional[int] = None,  # Nanosecond Unix timestamp
    ) -> List[Dict[str, str]]:
        """
        Get series for the given matchers.

        Args:
            match: List of series matchers
            start: Start time in nanosecond Unix timestamp
            end: End time in nanosecond Unix timestamp

        Returns:
            List of series with their labels
        """
        params = {"match[]": match}
        if start:
            params["start"] = str(start)
        if end:
            params["end"] = str(end)

        response = self._client.get("/loki/api/v1/series", params=params)
        response.raise_for_status()
        return response.json()["data"]
