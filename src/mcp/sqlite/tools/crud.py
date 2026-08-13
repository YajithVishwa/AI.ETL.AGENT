import os
import sys
from typing import List, Optional

base_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.append(base_dir)

from utils import logger
from connection import sqlite_connect


def query_sqlite(query: str) -> Optional[List]:
    with sqlite_connect() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        logger.info(f'Executing Query in SQLite Database - {query}')
        conn.commit()
        try:
            result = cursor.fetchall()
            conn.commit()
            return result
        except:
            pass