import dash_mantine_components as dmc
import dash_ag_grid as dag
from dash import html

ranking_content = html.Div([
    dmc.Title("Ranking Table", mb  = 20),
    dag.AgGrid(
        id='ranking-table',
        columnDefs=[
            {"headerName": "Stock", "field": "stock"},
            {"headerName": "Rank", "field": "rank"},
            {"headerName": "Score", "field": "score"},
        ],
        rowData=[],
        className="ag-theme-alpine",
        style={"height": "400px", "width": "100%"},
    )
])
