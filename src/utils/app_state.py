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
        self.list_of_all_stocks = clickhouse_obj.get_all_stocks()