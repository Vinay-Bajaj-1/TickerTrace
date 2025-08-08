from dash import dcc
import dash_mantine_components as dmc

right_side = [
    dmc.Alert(
        id="alert-warning",
        title="Alert!",
        color="red",
        duration=3000,
        style={"display": "none"},
    ),
    
    dmc.Stack(
        children = [
            dmc.Text("No data to show...", id = 'ohlc-text'),
            dcc.Graph(id='graph')  
        ] 
    )     
]
