from typing import List, Optional
from ..utils import logger
from ..connection import sqlite_connect


def query_sqlite(query: str) -> Optional[List]:
    with sqlite_connect() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        logger.info(f'Executing Query in SQLite Database - {query}')
        try:
            result = cursor.fetchall()
            return result
        except Exception as e:
            logger.error(f"Error fetching SQLite results: {e}")
        return None