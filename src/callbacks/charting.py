import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Output, Input, callback, State, no_update
from dash.exceptions import PreventUpdate
from datetime import timedelta, time

from src.utils.app_state import AppState
app_state = AppState()

@callback(
    Output('graph', 'figure'),
    Input('current-stock-ohlcv', 'data'),
    Input('candle-index', 'data'),
    Input('stock-select', 'value'),
    

    prevent_initial_call=True
)
def initialize_graph(data, idx, stock_name):
    if not data or idx > 0:
        raise PreventUpdate

    fig = go.Figure(
        make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            row_heights=[0.7, 0.3],
            vertical_spacing=0.05,
            specs=[[{"type": "candlestick"}], [{"type": "bar"}]]
        )
    )
    fig.add_trace(
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
    colors = ['#66CDAA' if c > o else '#F08080' for o, c in zip(data['open'], data['close'])]
    fig.add_trace(
        go.Bar(
            x=[],
            y=[],
            name='Volume',
            marker=dict(color=colors)
        ),
        row=2, col=1
    )
    start_timestamp = pd.to_datetime(data['timestamp'][0])
    end_timestamp = start_timestamp + timedelta(minutes=30)
    fig.update_layout(
        showlegend=False,
        title=dict(
            text=f"[{stock_name.upper()}]",
            x=0.5,
            xanchor='center',
            yanchor='top'
        ),
        xaxis_rangeslider_visible=False,
        margin=dict(t=80, b=50, l=10, r=10),  # increased bottom margin for xaxis2 title display
        height=700,
        hovermode='x unified',
        xaxis=dict(
            # Remove xaxis title here (or set to empty) to avoid duplicate titles
            title='',  
            range=[start_timestamp, end_timestamp],
            showgrid=True,
            zeroline=False,
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikethickness=1,
            spikecolor='gray',
            spikedash='dot'
        ),
        xaxis2=dict(
            title='Time',  # x-axis title shown below volume bars in row 2
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
            title='Price',   # y-axis title for price subplot (row 1)
            showgrid=True,
            zeroline=False,
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikethickness=1,
            spikecolor='gray',
            spikedash='dot'
        ),
        yaxis2=dict(
            autorange=True,
            title='Volume',  # y-axis title for volume subplot (row 2)
            showgrid=True,
            zeroline=False
        )
    )

    return fig


@callback(
    Output('graph', 'figure', allow_duplicate=True),
    State('current-stock-ohlcv', 'data'),
    Input('candle-index', 'data'),
    State('graph', 'figure'),
    State('resample', 'value'),
    prevent_initial_call=True
)
def update_xaxis(json_dict, idx, fig, resample):
    if idx is None or idx < 0 or not json_dict or not fig:
        raise PreventUpdate

    timestamps = json_dict.get('timestamp')
    if not timestamps or idx >= len(timestamps):
        raise PreventUpdate

    # Convert resample string to minutes
    minutes_per_bar = app_state.RESAMPLE_TO_MINUTES[resample]

    # Define how often to update and how much to zoom
    update_interval = 30 if minutes_per_bar == 1 else minutes_per_bar * 12
    zoom_window = update_interval  

    current_ts = pd.to_datetime(timestamps[idx])
    start_ts = pd.to_datetime(timestamps[0])

    if (current_ts.minute % update_interval == 0 and current_ts.second == 0) or idx == 0:
        end_ts = current_ts + timedelta(minutes=zoom_window)

        fig['layout']['xaxis'].update({
            'range': [start_ts, end_ts],
            'autorange': False
        })
        if 'xaxis2' in fig['layout']:
            fig['layout']['xaxis2'].update({
                'range': [start_ts, end_ts],
                'autorange': False
            })

        fig['layout']['yaxis']['autorange'] = True
        return fig

    raise PreventUpdate




@callback(
    Output('graph', 'extendData'),
    Input('candle-index', 'data'),
    State('current-stock-ohlcv', 'data'),
    prevent_initial_call=True
)
def extend_chart(idx, data):
    if not data or idx is None or idx < 0:
        raise PreventUpdate

    if idx >= len(data['timestamp']):
        return no_update

    # Extract data point at index
    ts = pd.to_datetime(data['timestamp'][idx])
    o = data['open'][idx]
    h = data['high'][idx]
    l = data['low'][idx]
    c = data['close'][idx]

    new_data = {
        'x': [[ts]],
        'open': [[o]],
        'high': [[h]],
        'low': [[l]],
        'close': [[c]]
    }

    return new_data, [0]

@callback(
    Output('graph', 'extendData', allow_duplicate=True),
    Input('candle-index', 'data'),
    State('current-stock-ohlcv', 'data'),
    prevent_initial_call=True
)
def extend_volume_bar(idx, data):
    if not data or idx is None or idx < 0:
        raise PreventUpdate

    if idx >= len(data['timestamp']):
        return no_update

    ts = pd.to_datetime(data['timestamp'][idx])
    v = data['volume'][idx]   
    new_data = {
        'x': [[ts]],  
        'y': [[v]] ,
        
    }
    return new_data, [1]


@callback(
    Output('ohlc-text', 'children'),
    Input('current-stock-ohlcv', 'data'),
    Input('candle-index', 'data')
)
def update_text(data, idx):
    if not data or idx < 0:
        return no_update

    
    timestamps = data['timestamp']
    if idx >= len(timestamps):
        return no_update
    

    ts = data["timestamp"][idx]
    o = data["open"][idx]
    h = data["high"][idx]
    l = data["low"][idx]
    c = data["close"][idx]
    vol = data['volume'][idx]
    
    return f"{ts} | O:{o} H:{h} L:{l} C:{c} VOL:{vol}"


