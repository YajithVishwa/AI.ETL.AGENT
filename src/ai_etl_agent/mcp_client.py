from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool
from typing import List
import os
import sys

class MCPClient:
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        mcp_path = os.path.join(base_path, 'src', 'mcp')
        self.client = MultiServerMCPClient(
            connections={
                "databricks": {
                    "transport": "stdio",
                    "command": "python",
                    "args": [os.path.join(mcp_path, "dbx", "server.py")]
                },
                "snowflake": {
                    "transport": "stdio",
                    "command": "python",
                    "args": [os.path.join(mcp_path, "snowflake", "server.py")]
                },
                "sqlite": {
                    "transport": "stdio",
                    "command": "python",
                    "args": [os.path.join(mcp_path, "sqlite", "server.py")]
                }
            }
        )

    async def get_tools(self) -> List[BaseTool]:
        return await self.client.get_tools()