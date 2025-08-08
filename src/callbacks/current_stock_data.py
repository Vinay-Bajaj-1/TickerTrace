from dash import Input, Output, callback, no_update, State

from src.utils.app_state import AppState

app_state = AppState()

@callback(
    Output('current-stock-ohlcv', 'data'),
    Output('interval-component', 'n_intervals'),
    Output('candle-index', 'data', allow_duplicate=True),
    Input('stock-select', 'value'),
    Input('date-select', 'value'),
    Input('resample', 'value'),
    prevent_initial_call = True

)
def load_stock_ohlcv(stock, date, resample):
    if date is None or stock is None:
        return no_update, no_update, no_update
    json_data = app_state.load_ohlcv(date, stock, resample)
    return json_data, 0,0
