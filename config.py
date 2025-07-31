import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()

        # ClickHouse Config
        self.CLICKHOUSE_TABLE = os.getenv("CLICKHOUSE_TABLE")
        self.CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
        self.CLICKHOUSE_USERNAME = os.getenv("CLICKHOUSE_USERNAME")
        self.CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD")
        self.CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE")
        