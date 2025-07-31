import dash
from src.layouts.main_layout import layout
app = dash.Dash(__name__)
app.layout = layout
app.run(debug=True, port=8050)