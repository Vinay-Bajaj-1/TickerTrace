from dash import Input, Output, State, callback, no_update
import dash
from src.utils.app_state import AppState
import plotly.graph_objects as go
app_state = AppState()

@callback(
    Output('is-running', 'data'),
    Output('alert-warning', 'style'),
    Output('alert-warning', 'children'),
    Input('start-button', 'n_clicks'),
    Input('stop-button', 'n_clicks'),
    State('is-running', 'data'),
    State('stock-select', 'value'),
    State('date-select', 'value'),
)
def is_running(start_btn, stop_btn, is_running_state, stock, date):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return is_running_state, {"display": "none"}, ""

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'start-button':
        if stock is None or date is None:
            return False, {"display": "block"}, 'Please select a stock and a date before starting.'
        # Hide alert and start running
        return True, {"display": "none"}, ""

    elif button_id == 'stop-button':
        # Hide alert and stop running
        return False, {"display": "none"}, ""

    return no_update, no_update, no_update

    

@callback(
    Output('interval-component', 'disabled'),
    Input('is-running', 'data'),
)
def toggle_interval(is_running):
    return not is_running


@callback(
    Output('graph', 'figure', allow_duplicate=True),
    Output('interval-component', 'n_intervals', allow_duplicate=True),
    Output('candle-index', 'data', allow_duplicate=True),
    Output('is-running', 'data', allow_duplicate=True),
    Output('ohlc-text', 'children', allow_duplicate=True),
    Input('reset-button', 'n_clicks'),
    prevent_initial_call = True
)
def rest_simulation(n_clicks):
    return go.Figure(), 0, 0, False, 'No data to show...'


@callback(
    Output('candle-index', 'data'),
    Input('interval-component', 'n_intervals')
)
def update_candle_index(n):
    return n-1