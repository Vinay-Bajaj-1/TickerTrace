import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import clickhouse_connect
from config import Config 
import pandas as pd
from src.utils.logger import AppLogger

logger = AppLogger.get_logger(__name__)

class ClickHouseDataFetcher(Config):
    def __init__(self):
        super().__init__()  # Loacld environment variables using Config class
        try:
            # Initialize ClickHouse client with values from .env
            self.client = clickhouse_connect.get_client(
                host=self.CLICKHOUSE_HOST,
                port=8123,  
                username=self.CLICKHOUSE_USERNAME,
                password=self.CLICKHOUSE_PASSWORD,
                database=self.CLICKHOUSE_DATABASE
            )
            logger.info(f"Successfully connected to ClickHouse at {self.CLICKHOUSE_HOST}:8123")
        except Exception as e:
            logger.error(f'Error connecting to database at {self.CLICKHOUSE_HOST}:8123', exc_info=True)


    
    def parse_interval(self, interval_str):
        unit_map = {
            'min': 'minute',
            'h': 'hour',
            'd': 'day'
        }

        import re
        match = re.match(r'(\d+)([a-zA-Z]+)', interval_str)
        if not match:
            raise ValueError("Invalid interval format. Use like '5min', '1h', '1d'.")

        value, unit = match.groups()
        unit = unit_map.get(unit.lower(), unit.lower())
        return int(value), unit

    def fetch_data(self, entry_date, exit_date, ticker, interval=None):
        start_ts = f"{entry_date} 09:15:00"
        end_ts = f"{exit_date} 15:29:00"

        if interval:
            value, unit = self.parse_interval(interval)

            if value == 1 and unit == "day":
                interval_clause = f"toDate(timestamp) AS ts_bucket"
            else:
                interval_clause = f"toStartOfInterval(timestamp, INTERVAL {value} {unit.upper()}) AS ts_bucket"

            query = f"""
            SELECT
                {interval_clause},
                any(open) AS open,
                max(high) AS high,
                min(low) AS low,
                anyLast(close) AS close,
                sum(volume) AS volume
            FROM {self.CLICKHOUSE_TABLE}
            WHERE ticker = %(ticker)s
            AND timestamp >= %(start_ts)s
            AND timestamp <= %(end_ts)s
            GROUP BY ts_bucket
            ORDER BY ts_bucket
            """
        else:
            query = f"""
            SELECT timestamp, open, high, low, close, volume
            FROM {self.CLICKHOUSE_TABLE}
            WHERE ticker = %(ticker)s
            AND timestamp >= %(start_ts)s
            AND timestamp <= %(end_ts)s
            ORDER BY timestamp
            """

        params = {
            'ticker': ticker.lower(),
            'start_ts': start_ts,
            'end_ts': end_ts
        }

        df = self.client.query_df(query, parameters=params)
        
        if interval:
            df = df.rename(columns={"ts_bucket": "timestamp"})
        return df

    def get_all_stocks(self):
        query = 'SELECT DISTINCT ticker FROM stock_ohlcv'
        try:
            df = self.client.query_df(query)
            if df.empty:
                logger.warning("No tickers found in the stock_ohlcv table.")
                return []
            tickers = df['ticker'].str.upper().to_list()
            logger.info(f"Fetched {len(tickers)} unique tickers from stock_ohlcv.")
            return tickers
        except Exception as e:
            logger.error(f"Error while fetching all stocks: {e}", exc_info=True)
            return []

    def get_unique_dates_for_ticker(self, ticker):
        query = """
            SELECT DISTINCT toDate(timestamp) AS date
            FROM stock_ohlcv
            WHERE ticker = %(ticker)s
            ORDER BY date
        """
        try:
            df = self.client.query_df(query, parameters={'ticker': ticker.lower()})
            return df['date'].to_list() if not df.empty else []
        except Exception as e:
            logger.error(f"Failed to fetch unique dates for ticker '{ticker}': {e}", exc_info=True)
            return []

