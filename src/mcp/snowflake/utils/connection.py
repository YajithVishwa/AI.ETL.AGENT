import snowflake.connector
from snowflake.connector import SnowflakeConnection
import os

SF_USER = os.getenv('SF_USER', '')
SF_PASSWORD = os.getenv('SF_PASSWORD', '')
SF_ACCOUNT = os.getenv('SF_ACCOUNT', '')
SF_WAREHOUSE = os.getenv('SF_WAREHOUSE', '')
SF_DATABASE = os.getenv('SF_DATABASE', '')
SF_SCHEMA = os.getenv('SF_SCHEMA', '')

assert all([SF_USER, SF_PASSWORD, SF_ACCOUNT, SF_WAREHOUSE, SF_DATABASE, SF_SCHEMA]), 'SF_USER, SF_PASSWORD, SF_ACCOUNT, SF_WAREHOUSE, SF_DATABASE, SF_SCHEMA need to be set in Environment Variable'

def snowflake_connection() -> SnowflakeConnection:
    return snowflake.connector.connect(
        user=SF_USER,
        password=SF_PASSWORD,
        account=SF_ACCOUNT,
        warehouse=SF_WAREHOUSE,
        database=SF_DATABASE,
        schema=SF_SCHEMA
    )