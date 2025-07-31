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
                    mb = 10
                ),
                dmc.Select(
                    label = 'Select Date',
                    id = 'date-select',
                    data = [],
                    searchable=True,
                    mb = 10
                ),
            ] 
        ),
        dcc.Store('selected-date', data = None),
        dcc.Store('selected-stock', data = None),
    ])



]