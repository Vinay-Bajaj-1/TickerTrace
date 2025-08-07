import dash
from dash import html, dcc
import dash_mantine_components as dmc
from src.layouts.navbar import nav_layout
from src.layouts.main_screen import right_side

from src.callbacks import charting
from src.callbacks import collapse_navbar
from src.callbacks import current_stock_data
from src.callbacks import interval_speed
from src.callbacks import play_pause
from src.callbacks import show_date



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
            right_side,  
        ),
        dcc.Store(id='candle-index', data=0),
        dcc.Store('current-stock-ohlcv', data = None),
        dcc.Store('is-running', data = False),
        dcc.Interval(id='interval-component',interval=1000, n_intervals=0),


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