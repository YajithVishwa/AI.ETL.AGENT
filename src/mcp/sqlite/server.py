from mcp.server import MCPServer
from typing import List
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.normpath(os.path.join(os.path.abspath(__file__), "../../../..")), '.env'))

from .tools import query_sqlite

mcp = MCPServer('SQLite MCP Server')

@mcp.tool()
def execute_query(query: str) -> List:
    """Execute Query in SQLite and return list of results"""
    return query_sqlite(query)

if __name__ == '__main__':
    mcp.run(transport='stdio')