import dash
from dash import html, dcc
import os
from src.layouts.global_stores import global_stores  
import dash_mantine_components as dmc


app = dash.Dash(__name__, use_pages=True, pages_folder=os.path.join("src", "pages"))


app.layout = dmc.MantineProvider(html.Div([
    dcc.Location(id="url"),      
    *global_stores,              
    dash.page_container          
]))


app.run(debug=True, port=8050)
