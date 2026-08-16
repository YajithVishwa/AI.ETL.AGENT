import sqlite3
import os
from mcp_servers.sqlite.utils import logger

def sqlite_connect():
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.normpath(os.path.join(base_path, '../../db', 'sql.db'))
    if not os.path.isfile(db_path):
        logger.info('DB not found, so creating')
    return sqlite3.connect(db_path)