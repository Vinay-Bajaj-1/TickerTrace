from dash import Input, Output, State, callback

@callback(
    Output("appshell", "navbar"),
    Input("desktop-burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(desktop_opened, navbar):
    navbar["collapsed"] = {
        "desktop": not desktop_opened,
    }
    return navbar