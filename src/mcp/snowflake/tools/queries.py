import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.normpath(os.path.join(os.path.abspath(__file__), "../..")), 'utils'))

import snowflake_connection

def execute_sf_query(query: str) -> List:
    """Executes Query in Snowflake and returns list of results"""
    with snowflake_connection() as conn:
        conn.execute(query)
        result = conn.fetchall()
    return result