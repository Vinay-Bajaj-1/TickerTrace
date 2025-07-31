from dash import html, dcc
import dash_echarts
import dash_mantine_components as dmc



left_side = [
    dmc.Alert(
        id="alert-warning",
        title="Alert!",
        color="red",
        duration=3000,
        style={"display": "none"},  # initially hidden
    ),
    html.Div([
        dash_echarts.DashECharts(
            id="echarts-candlestick",
            option = {},
            style={"height": "400px", "width": "100%"}
        )
    ])
]