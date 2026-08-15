import requests
from typing import List, Dict, Any
import os

DBX_BASE_URL = os.getenv('DBX_BASE_URL')
DBX_API_TOKEN = os.getenv('DBX_API_TOKEN')

if not DBX_BASE_URL:
    raise ValueError("DBX_BASE_URL must be set in environment variables")
if not DBX_API_TOKEN:
    raise ValueError("DBX_API_TOKEN must be set in environment variables")

def list_dbx_jobs() -> List[Dict[str, Any]]:
    """
        This list all jobs in Databricks and returns list of json jobs
    """
    query_param = {'limit': 100}
    header = {"Authorization": f"Bearer {DBX_API_TOKEN}"}
    response = requests.get(url=f'{DBX_BASE_URL}/api/2.2/jobs/list', params=query_param, headers=header)
    return response.json()['jobs']

def get_dbx_job(job_name: str) -> Dict[str, Any]:
    """
        This gets job in Databricks and returns list of json jobs
    """
    job_list = list_dbx_jobs()
    job_id = [job['job_id'] for job in job_list if job['settings']['name'] == job_name]
    if not job_id:
        raise ValueError('Incorrect Job Name or Job not present in Databricks')
    query_param = {'job_id': job_id[0]}
    header = {"Authorization": f"Bearer {DBX_API_TOKEN}"}
    response = requests.get(url=f'{DBX_BASE_URL}/api/2.2/jobs/get', params=query_param, headers=header)
    return response.json()

def trigger_dbx_job(job_name: str) -> int:
    """
        Trigger Databricks job and returns run_id
    """
    job_list = list_dbx_jobs()
    job_id = [job['job_id'] for job in job_list if job['settings']['name'] == job_name]
    if not job_id:
        raise ValueError('Incorrect Job Name or Job not present in Databricks')
    query_param = {'job_id': job_id[0]}
    header = {"Authorization": f"Bearer {DBX_API_TOKEN}"}
    response = requests.get(url=f'{DBX_BASE_URL}/api/2.2/jobs/run-now', params=query_param, headers=header)
    return response.json()