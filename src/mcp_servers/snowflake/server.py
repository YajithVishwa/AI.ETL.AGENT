from mcp.server.fastmcp import FastMCP
from typing import List, Dict
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.normpath(os.path.join(os.path.abspath(__file__), "../../../..")), '.env'))

from .tools import execute_sf_query

mcp = FastMCP('Snowflake MCP Server')

@mcp.tool()
def execute_query(query: str) -> List:
    """Execute Query in Snowflake and return list of results"""
    return execute_sf_query(query)

if __name__ == '__main__':
    mcp.run(transport='stdio')