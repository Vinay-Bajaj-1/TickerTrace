
from dash import dcc

global_stores = [
    dcc.Store(id='candle-index', data=0),
    dcc.Store(id='current-stock-ohlcv', data=None),
    dcc.Store(id='is-running', data=False),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0),
    dcc.Store(id='selected-date', data=None),
    dcc.Store(id='selected-stock', data=None),
]
