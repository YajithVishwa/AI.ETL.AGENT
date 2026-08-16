from typing import List
from mcp_servers.snowflake.utils import snowflake_connection, logger


def execute_sf_query(query: str) -> List:
    """Executes Query in Snowflake and returns list of results"""
    result = []
    conn = snowflake_connection()  # Don't use 'with'
    try:
        conn.execute(query)
        try:
            result = conn.fetchall()
        except Exception as e:
            logger.error(f"Error fetching Snowflake results: {e}")
    finally:
        conn.close()
    return result