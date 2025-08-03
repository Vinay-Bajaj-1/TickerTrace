import pandas as pd
import plotly.graph_objects as go
from dash import Output, Input, callback, State, no_update


@callback(
    Output('graph', 'figure'),
    Output('graph', 'style'),
    Output('chart-visible', 'data'),
    Input('show-chart-btn', 'n_clicks'),
    State('current-stock-ohlcv', 'data'),
    State('candle-index', 'data'),
    State('chart-visible', 'data'),  # current visibility state
    prevent_initial_call=True
)
def initialize_graph(n_clicks, data, idx, currently_visible):
    # Toggle logic: if currently visible, hide it
    if currently_visible:
        return go.Figure(), {'display': 'none'}, False

    # If data is invalid or index out of bounds, still hide the chart
    if not data or 'timestamp' not in data or idx is None or idx >= len(data['timestamp']):
        return go.Figure(), {'display': 'none'}, False

    # Chart is currently hidden → build and show it
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data['timestamp'][:idx+1],
        open=data['open'][:idx+1],
        high=data['high'][:idx+1],
        low=data['low'][:idx+1],
        close=data['close'][:idx+1],
        increasing_line_color='green',
        decreasing_line_color='red'
    ))
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        margin=dict(t=20, b=20, l=10, r=10),
        height=400
    )

    return fig, {'display': 'block'}, True




@callback(
    Output('graph', 'extendData'),
    Output('candle-index', 'data'),
    Input('interval-component', 'n_intervals'),
    State('chart-visible', 'data'),
    State('current-stock-ohlcv', 'data'),
    State('candle-index', 'data')
)
def extend_chart(n_intervals, visible, data, idx):
    if not visible or not data or idx is None:
        return no_update, idx

    idx += 1
    timestamps = data['timestamp']
    opens = data['open']
    highs = data['high']
    lows = data['low']
    closes = data['close']

    if idx >= len(timestamps):
        return no_update, idx

    new_data = {
        'x': [[timestamps[idx]]],
        'open': [[opens[idx]]],
        'high': [[highs[idx]]],
        'low': [[lows[idx]]],
        'close': [[closes[idx]]],
    }

    return [new_data, [0]], idx + 1



@callback(
    Output('ohlc-text', 'children'),
    Input('current-stock-ohlcv', 'data'),
    Input('candle-index', 'data')
)
def update_text(data, idx):
    if not data:
        return no_update
    
    timestamps = data['timestamp']
    if idx >= len(timestamps):
        return no_update, idx
    

    ts = data["timestamp"][idx]
    o = data["open"][idx]
    h = data["high"][idx]
    l = data["low"][idx]
    c = data["close"][idx]
    
    return f"{ts} | O:{o} H:{h} L:{l} C:{c}"


@callback(
    Output('candle-index', 'data', allow_duplicate = True),
    Input('interval-component', 'n_intervals'),
    prevent_initial_call = True
)
def update_candle_idx(n):
    return n