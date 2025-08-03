from src.utils.app_state import AppState
from dash import html, dcc
import dash_mantine_components as dmc

app_state = AppState()


nav_layout = [
    #stock select
    dmc.Center([
        dmc.Group(
            grow = True,
            children = [
                dmc.Select(
                    label = 'Select Stock',
                    id = 'stock-select',
                    data = app_state.list_of_all_stocks,
                    searchable=True,
                    mb = 20
                ),

                dmc.DateInput(
                    label = 'Select Date',
                    id = 'date-select',
                    disabledDates=[],
                    valueFormat="DD-MM-YYYY",
                    mb = 20
                )
            ] 
        ),
        dcc.Store('selected-date', data = None),
        dcc.Store('selected-stock', data = None),
    ]),

    
    dmc.Group(
        grow = True, 
        children = [
            dmc.Button('Start', variant = 'filled', id = 'start-button', fullWidth = True, n_clicks = 0, mb = 20),
            dmc.Button('Stop', variant = 'filled', id = 'stop-button', fullWidth = True,  n_clicks = 0, mb = 20),
        ], 
        justify = 'center'
    ),

    dmc.Select(
        label = 'Select speed',
        id = 'speed-select',
        data = app_state.speed_options, 
        value = '1000',
        mb = 20
    ),
    dmc.Button("Show Chart", id="show-chart-btn", variant="light", mt=10),



    


   

]