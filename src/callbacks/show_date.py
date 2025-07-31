from dash import Input, Output, callback, no_update

from src.utils.app_state import AppState
app_state = AppState()

@callback(
    Output('date-select', 'data'),
    Input('stock-select', 'value'),
)
def create_date_children(stock):
    if stock is None:
        return no_update
    
    return app_state.get_all_date_for_stock(stock)