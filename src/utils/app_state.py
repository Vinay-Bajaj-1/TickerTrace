from src.database.clickhouse import ClickHouseDataFetcher

from datetime import timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class AppState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.list_of_all_stocks = self.prepare_stock_list()

        self.pages_options = [
            {"label": "Homepage", "value": "homepage"},
            {"label": "Ranking Table", "value": "ranking"}
        ]
        
        self.speed_options = [
            {"label": "1 second", "value": '1000'},
            {"label": "0.75 seconds", "value": '750'},
            {"label": "0.5 seconds", "value": '500'},
            {"label": "0.25 seconds", "value": '250'}
        ]

        self.resample = [
            {"label": "1 min", "value": '1min'},
            {"label": "5 min", "value": '5min'},
            {"label": "10 min", "value": '10min'},
            {"label": "15 min", "value": '15min'},
            {"label": "30 min", "value": '30min'},
            {"label": "1 hour", "value": '1h'},

        ]
        self.initial_chart = go.Figure(
                make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    row_heights=[0.7, 0.3],
                    vertical_spacing=0.05,
                    specs=[[{"type": "candlestick"}], [{"type": "bar"}]]
                )
            )
        
        self.RESAMPLE_TO_MINUTES = {
                "1min": 1,
                "5min": 5,
                "10min": 10,
                "15min": 15,
                "30min": 30,
                "1h": 60
            }
        
        self.initial_chart.add_trace(
            go.Candlestick(
                x=[],
                open=[],
                high=[],
                low=[],
                close=[],
                increasing_line_color='green',
                decreasing_line_color='red'
            ),
            row=1, col=1
        )
        self.initial_chart.add_trace(
            go.Bar(
                x=[],
                y=[],
                name='Volume',
            ),
            row=2, col=1
        )


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

    

    def load_ohlcv(self, date, ticker, interval = '1min'):
        clickhouse_obj  = ClickHouseDataFetcher()
        df = clickhouse_obj.fetch_data(date, date, ticker, interval=interval)
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')  
        clickhouse_obj.client.close()

        return df.to_dict(orient='list')
