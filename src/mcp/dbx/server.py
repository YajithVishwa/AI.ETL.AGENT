from mcp.server import MCPServer
from typing import List, Dict, Any
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.normpath(os.path.join(os.path.abspath(__file__), "../../../..")), '.env'))

from .tools import list_dbx_jobs, get_dbx_job, trigger_dbx_job

mcp = MCPServer(name='Databricks MCP Server')

@mcp.tool()
def list_jobs() -> List[Dict[str, Any]]:
    """Returns List of jobs in Databricks"""
    return list_dbx_jobs()

@mcp.tool()
def get_job_details(job_name: str) -> Dict[str, Any]:
    """Returns job details by getting job_name as parameter"""
    return get_dbx_job(job_name=job_name)

@mcp.tool()
def trigger_job(job_name: str) -> Dict[str, Any]:
    """Returns job run id by triggering the job and by passing job_name as parameter"""
    return trigger_dbx_job(job_name=job_name)

if __name__ == '__main__':
    mcp.run(
        transport='stdio'
    )