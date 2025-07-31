from dash import Input, Output, callback, no_update

from src.utils.app_state import AppState
app_state = AppState()

@callback(
    Output('date-select', 'disabledDates'),
    Output('date-select', 'minDate'),
    Output('date-select', 'maxDate'),
    
    
    Input('stock-select', 'value'),
)
def create_date_children(stock):
    if stock is None:
        return no_update, no_update, no_update
    
    disabled_dates, min_date, max_date = app_state.get_disabled_dates(stock)
    
    return disabled_dates, min_date, max_date