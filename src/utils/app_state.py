from src.database.clickhouse import ClickHouseDataFetcher
clickhouse_obj  = ClickHouseDataFetcher()


class AppState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.list_of_all_stocks = self.prepare_stock_list()


    def prepare_stock_list(self):
        list_of_all_stocks = clickhouse_obj.get_all_stocks()
        data = [{'value' : stock.lower() , 'label' : stock} for stock in list_of_all_stocks]
        return data
    
    def get_all_date_for_stock(self, stock):
        list_of_all_dates = clickhouse_obj.get_unique_dates_for_ticker(stock)
        data = [{'value' : date.strftime('%Y-%m-%d') , 'label' : date.strftime('%Y-%m-%d')} for date in list_of_all_dates]
        return data
    

    def load_ohlcv(self, date, ticker):
        df = clickhouse_obj.fetch_data(date, date, ticker, interval='1min')
        json_data = df.to_json(orient='split') 
        return json_data
