import dash
from dash import html, callback, Output, Input
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='intro', path='/')

layout = dbc.Container([dbc.Container(id='IntroLayout')]),



@callback(
    Output("IntroLayout", "children"),
    Input("telemetry", "data")
)
def display_udp_status(store_data):
    if not store_data:
        return [html.Div("Load UDP data on IP Address '0.0.0.0', port 20777", className="text-center text-muted my-5")]
    
    else:
        return[html.Div([
                    html.H1('Welcome'),
                    html.Div('Use the menu buttons on the left to select a dashboard'),
                    ])]