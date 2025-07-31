import dash
from src.layouts.layout import layout
app = dash.Dash(__name__)
app.layout = layout
app.run(debug=True, port=8050)