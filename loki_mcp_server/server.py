from typing import List
from loki_client import LokiClient
from mcp.server.fastmcp import FastMCP
import time
from datetime import datetime, timedelta

mcp = FastMCP("loki")

LOKI_URL = "http://localhost:3100"
USER_AGENT = "loki/1.0"


def get_time_window() -> tuple[int, int]:
    """
    Get start and end times in nanosecond precision for a 3-hour window.
    Returns:
        Tuple of (start_time, end_time) in nanoseconds
    """
    end_time = int(time.time() * 1_000_000_000)  # Current time in nanoseconds
    start_time = end_time - (3 * 60 * 60 * 1_000_000_000)  # 3 hours ago in nanoseconds
    return start_time, end_time


loki_client = LokiClient(base_url=LOKI_URL)


@mcp.tool()
async def get_logs_by_service_name_and_correlation_id(
    service_name: str, correlation_id: str
) -> List[str]:
    """
    Get logs by service name and correlation id

    Args:
        service_name: The name of the service to search for
        correlation_id: The correlation id to search for

    Returns:
        A list of logs
    """
    query = (
        '{service_name="'
        + service_name
        + '"} | json | correlation_id="'
        + correlation_id
        + '"'
    )

    start_time, end_time = get_time_window()
    result = loki_client.query_range(query=query, start=start_time, end=end_time)
    return result


if __name__ == "__main__":
    mcp.run(transport="stdio")
