import dash
import dash_mantine_components as dmc
from src.layouts.navbar import nav_layout
from src.layouts.main_screen import left_side
from src.callbacks.collapse_navbar import toggle_navbar
from src.callbacks.show_date import create_date_children
from src.callbacks.current_stock_data import load_stock_ohlcv
from dash import dcc


final_layout = dmc.AppShell(
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
            'Main',
            left_side,
        ),
        dcc.Store('current-stock-ohlcv', data = {})

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
layout = dmc.MantineProvider(final_layout)