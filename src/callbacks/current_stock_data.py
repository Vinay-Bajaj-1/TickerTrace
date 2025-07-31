from dash import Input, Output, callback, no_update, State

from src.utils.app_state import AppState

app_state = AppState()

@callback(
    Output('current-stock-ohlcv', 'data'),
    State('stock-select', 'value'),
    Input('date-select', 'value')

)
def load_stock_ohlcv(stock, date):
    if date is None or stock is None:
        return no_update
    json_data = app_state.load_ohlcv(date, stock)
    return json_data
