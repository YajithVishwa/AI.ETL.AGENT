import sqlite3
import os
import sys

sys.path.append(os.path.normpath(os.path.join(os.path.abspath(__file__), '..')))

from utils import logger

def sqlite_connect():
    db_path = os.path.normpath(os.path.join(os.path.abspath(__file__), '../../db', 'sql.db'))
    if not os.path.isfile(db_path):
        logger.info('DB not found, so creating')
    return sqlite3.connect(db_path)