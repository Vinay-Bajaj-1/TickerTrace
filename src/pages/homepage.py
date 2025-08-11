import dash
from dash import html, Output, Input, callback
import dash_mantine_components as dmc
from src.layouts.navbar import nav_layout


from src.layouts.main_screen import right_side 
from src.pages.table_ranking import ranking_content  


dash.register_page(__name__, path='/')

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(
                        id="desktop-burger",
                        size="sm",
                        visibleFrom="sm",
                        opened=True,
                        style={"marginLeft": "16px"},
                    ),
                    dmc.Box(style={"flexGrow": 1}),
                    dmc.Title(
                        "TickerTrace",
                        c="blue",
                        style={
                            "textAlign": "center",
                            "flexGrow": 0,
                            "marginTop": "0",
                            "marginBottom": "0",
                        }
                    ),
                    dmc.Box(style={"flexGrow": 1}),
                ],
                align="center",
                justify="center",
                style={
                    "width": "100%",
                    "height": "100%",
                    "paddingTop": "16px",
                    "paddingBottom": "16px",
                },
            )
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=nav_layout,
            p='md',
        ),
        dmc.AppShellMain(
            id="main-content",  # make this a container to update dynamically
            children=right_side,  # default content (homepage)
        ),
    ],
    header={'height': 75},
    navbar={
        'width': 300,
        "breakpoint": "sm",
        "collapsed": {"desktop": False},
    },
    padding="md",
    id="appshell",
)

@callback(
    Output('main-content', 'children'),
    Input('page-selector', 'value')
)
def switch_main_content(selected_page):
    if selected_page == "ranking":
        return ranking_content  
    else:
        return right_side 
