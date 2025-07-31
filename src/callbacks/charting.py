import pandas as pd
from io import StringIO
from dash import Output, Input, callback


MAX_CANDLES = 375
EXTEND_BY = 30
start_time = pd.Timestamp('09:15')

@callback(
    Output("echarts-candlestick", "option"),  # Update echarts option property
    Input("interval-component", "n_intervals"),
    Input("current-stock-ohlcv", "data"),
)
def update_candlestick_chart(n_intervals, ohlcv_json):
    if not ohlcv_json:
        # No data loaded yet, return empty option
        return {}

    try:
        # Wrap JSON string in StringIO for compatibility with read_json
        json_buffer = StringIO(ohlcv_json)
        df = pd.read_json(json_buffer, orient='split')
    except Exception as e:
        print("Failed to parse OHLCV JSON data:", e)
        return {}

    # Defensive: at least show 1 candle even if n_intervals is 0 or None
    if n_intervals is None or n_intervals < 1:
        current_index = 1
    else:
        current_index = min(n_intervals, len(df))

    # Slice the dataframe up to current_index
    df_partial = df.iloc[:current_index].copy()
    df_partial['timestamp'] = pd.to_datetime(df_partial['timestamp'])

    visible_len = ((len(df_partial) - 1) // EXTEND_BY + 1) * EXTEND_BY
    time_range = [(start_time + pd.Timedelta(minutes=i)).strftime('%H:%M') for i in range(visible_len)]
  
    prefill_dict = {t: [None, None, None, None] for t in time_range}

    for _, row in df_partial.iterrows():
        key = row['timestamp'].strftime('%H:%M')
        prefill_dict[key] = [
            float(row['open']), float(row['close']),
            float(row['low']), float(row['high'])
        ]

    x_data = list(prefill_dict.keys())
    kline_data = list(prefill_dict.values())

    option = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross"},
        },
        "xAxis": {
            "type": "category",
            "data": x_data ,
            "scale": True,
            "boundaryGap": False,
            "axisLine": {"onZero": False},
            "splitLine": {"show": False},
            "min": "dataMin",
            "max": "dataMax",
        },
        "yAxis": {
            "scale": True,
            "splitArea": {"show": True},
        },
        "dataZoom": [
            {
                "type": "inside",
                "start": 0,
                "end": 100,
            },
            {
                "show": True,
                "type": "slider",
                "top": "85%",
                "start": 0,
                "end": 100,
            },
        ],
        "series": [
            {
                "name": "Candlestick",
                "type": "candlestick",
                "data": kline_data,
                "itemStyle": {
                    "color": "#ec0000",      # rising candle color (red)
                    "color0": "#00da3c",     # falling candle color (green)
                    "borderColor": "#8A0000",
                    "borderColor0": "#008F28",
                },
            }
        ],
    }

    return option
