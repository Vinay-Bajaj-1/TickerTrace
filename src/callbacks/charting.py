import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Output, Input, callback, State, no_update
from dash.exceptions import PreventUpdate
from datetime import timedelta

@callback(
    Output('graph', 'figure'),
    Input('chart-visible', 'data'),
    State('current-stock-ohlcv', 'data'),
    State('candle-index', 'data'),
    prevent_initial_call=True
)
def initialize_graph(currently_visible, data, idx):

    fig = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        subplot_titles=[""],
        specs=[[{"type": "candlestick"}]]
    )

    
    if not currently_visible:
        return fig  

    
    fig.add_trace(
        go.Candlestick(
            x=data['timestamp'][:idx],
            open=data['open'][:idx],
            high=data['high'][:idx],
            low=data['low'][:idx],
            close=data['close'][:idx],
            increasing_line_color='green',
            decreasing_line_color='red'
        ),
        row=1, col=1
    )

    # Setup x-axis range window from start to next 30-minute mark
    current_ts = pd.to_datetime(data['timestamp'][idx])
    start_timestamp = pd.to_datetime(data['timestamp'][0])
    remainder = current_ts.minute % 30
    end_timestamp = current_ts + timedelta(minutes=(30 - remainder))
    end_timestamp = end_timestamp.replace(second=0, microsecond=0)

    fig.update_layout(
        xaxis_rangeslider_visible=False,
        margin=dict(t=20, b=20, l=10, r=10),
        height=400,
        hovermode='x unified',
        xaxis=dict(
            range=[start_timestamp, end_timestamp],
            title='Time',
            showgrid=True,
            zeroline=False,
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikethickness=1,
            spikecolor='gray',
            spikedash='dot'
        ),
        yaxis=dict(
            autorange=True,
            title='Price',
            showgrid=True,
            zeroline=False,
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikethickness=1,
            spikecolor='gray',
            spikedash='dot'
        )
    )

    return fig

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
    
    idx-=1
    
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
    Output('graph', 'figure', allow_duplicate=True),
    State('current-stock-ohlcv', 'data'),
    Input('candle-index', 'data'),
    State('graph', 'figure'),
    prevent_initial_call=True
)
def update_xaxis(json_dict, idx, fig):

    if idx is None or json_dict is None or len(json_dict) == 0 or not fig:
        raise PreventUpdate
    
    if idx >= len(json_dict['timestamp']):
        raise PreventUpdate

    timestamps = json_dict['timestamp']
    start_datetime = pd.to_datetime(timestamps[0])
    current_ts = pd.to_datetime(timestamps[idx])

    if current_ts.minute % 30 == 0 and current_ts.second == 0 or idx == 1:
        end_datetime = current_ts + timedelta(minutes=30)
        
        fig['layout']['xaxis']['range'] = [start_datetime, end_datetime]
        fig['layout']['yaxis']['autorange'] = True

        return fig
    raise PreventUpdate

    

@callback(
    Output('candle-index', 'data', allow_duplicate = True),
    Input('interval-component', 'n_intervals'),
    prevent_initial_call = True
)
def update_candle_idx(n):
    return n

@callback(
    Output('chart-visible', 'data'),
    Input('show-chart-btn', 'n_clicks'),
    State('chart-visible', 'data'),
    prevent_initial_call=True
)
def toggle_chart_visibility(n_clicks, current_state):
    if current_state is None:
        return True  
    return not current_state 