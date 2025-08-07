from src.database.clickhouse import ClickHouseDataFetcher
import pandas as pd
from datetime import timedelta
class AppState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.list_of_all_stocks = self.prepare_stock_list()
        self.speed_options = [
            {"label": "1 second", "value": '1000'},
            {"label": "0.75 seconds", "value": '750'},
            {"label": "0.5 seconds", "value": '500'},
            {"label": "0.25 seconds", "value": '250'}
        ]


    def prepare_stock_list(self):
        clickhouse_obj  = ClickHouseDataFetcher()

        list_of_all_stocks = clickhouse_obj.get_all_stocks()
        data = [{'value' : stock.lower() , 'label' : stock} for stock in list_of_all_stocks]
        clickhouse_obj.client.close()
        return data
    


    def get_disabled_dates(self, stock):
        clickhouse_obj  = ClickHouseDataFetcher()
        list_of_all_dates = clickhouse_obj.get_unique_dates_for_ticker(stock)

        # Ensure list_of_all_dates are datetime objects (if not convert)
        valid_dates = set(list_of_all_dates)  # valid trading dates as datetime objects

        min_date = min(valid_dates)
        max_date = max(valid_dates)


        total_days = (max_date - min_date).days + 1
        all_dates_range = {min_date + timedelta(days=x) for x in range(total_days)}

        disabled_dates_set = all_dates_range - valid_dates
        disabled_dates = sorted(disabled_dates_set)
        clickhouse_obj.client.close()
       
        disabled_dates_str = [d.strftime("%Y-%m-%d") for d in disabled_dates]
        return disabled_dates_str, min_date, max_date

    

    def load_ohlcv(self, date, ticker):
        clickhouse_obj  = ClickHouseDataFetcher()

        df = clickhouse_obj.fetch_data(date, date, ticker, interval='1min')
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')  
        clickhouse_obj.client.close()

        return df.to_dict(orient='list')
