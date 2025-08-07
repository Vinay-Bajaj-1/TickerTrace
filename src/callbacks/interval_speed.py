
from dash import Input, Output, callback

@callback(
    Output('interval-component', 'interval'),
    Input('speed-select', 'value')
)
def update_interval_speed(selected_speed):
    if selected_speed is None:
        return 1000 
    return int(selected_speed)