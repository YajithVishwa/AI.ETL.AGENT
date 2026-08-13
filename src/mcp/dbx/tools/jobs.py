import requests
from typing import List, Dict
import os

DBX_BASE_URL = os.getenv('DBX_BASE_URL', '')
assert DBX_BASE_URL != '', "DBX_BASE_URL need to be set in environment Variable"

DBX_TOKEN = os.getenv('DBX_TOKEN', '')
assert DBX_TOKEN != '', "DBX_TOKEN need to be set in environment Variable"

def list_dbx_jobs() -> List[Dict]:
    """
        This list all jobs in Databricks and returns list of json jobs
    """
    query_param = {'limit': 100}
    header = {"Authorization": f"Bearer {DBX_TOKEN}"}
    response = requests.get(url=f'{DBX_BASE_URL}/api/2.2/jobs/list', params=query_param, headers=header)
    return response.json()['jobs']

def get_dbx_job(job_name: str) -> Dict[str]:
    """
        This gets job in Databricks and returns list of json jobs
    """
    job_list = list_dbx_jobs()
    job_id = [job['job_id'] for job in job_list if job['settings']['name'] == job_name]
    if not job_id:
        raise ValueError('Incorrect Job Name or Job not present in Databricks')
    query_param = {'job_id': job_id[0]}
    header = {"Authorization": f"Bearer {DBX_TOKEN}"}
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
    header = {"Authorization": f"Bearer {DBX_TOKEN}"}
    response = requests.get(url=f'{DBX_BASE_URL}/api/2.2/jobs/run-now', params=query_param, headers=header)
    return response.json()