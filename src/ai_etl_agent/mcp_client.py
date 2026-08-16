from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool
from typing import List

class MCPClient:
    def __init__(self):
        self.client = MultiServerMCPClient(
            connections={
                "databricks": {
                    "transport": "stdio",
                    "command": "uv",
                    "args": ['run', 'python', '-m' , 'mcp_servers.dbx.server']
                },
                "snowflake": {
                    "transport": "stdio",
                    "command": "uv",
                    "args": ['run', 'python', '-m' , 'mcp_servers.snowflake.server']
                },
                "sqlite": {
                    "transport": "stdio",
                    "command": "uv",
                    "args": ['run', 'python', '-m' , 'mcp_servers.sqlite.server']
                }
            }
        )

    async def get_tools(self) -> List[BaseTool]:
        return await self.client.get_tools()