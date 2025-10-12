import plotly.graph_objects as go
import dash 
from dash import dcc, Input, Output, callback, html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import threading
from collections import deque
from codeassets import graph_config, graph_backgrounds, create_loading_figure



dash.register_page(__name__, name='race', path='/race')


layout = dbc.Container([dbc.Container(id='RaceLayout')]),



@callback(
    Output("RaceLayout", "children"),
    Input("telemetry", "data")
)
def display_udp_status(store_data):
    if not store_data:
        return [html.Div("Load UDP data on IP Address '0.0.0.0', port 20777", className="text-center text-muted my-5")]
    
    else:
        return [dbc.Row(html.Div(id='ThrottleWarning', className='ThrottleNeutral'),),
                dbc.Row(html.Div(id='BrakeWarning', className='ThrottleNeutral'),),
                dbc.Row([
                    dbc.Col([
                        # dcc.Graph(id='vs_throttle', config=graph_config, style={"height": "300px"}),
                        html.Div(style={"height": "300px"}),
                        ], width=6, class_name='borders'),
                    dbc.Col([
                        html.Div(style={"height": "300px"}),
                        # dcc.Graph(id='vs_brake', config=graph_config, style={"height": "300px"}),
                        ], width=6, class_name='borders')
                    ])]



@callback(
    Output('ThrottleWarning', 'className'),
    Output('ThrottleWarning', 'children'),
    Input("telemetry", "data")  # <-- Must match the Store ID
)
def Wheel_Spin(store_data):
    
    player_data = store_data["player"]
    
    if player_data['throttle'] > 0.6 and (player_data['WheelSplipRatio'][0] > 0.15 or player_data['WheelSplipRatio'][1] > 0.15):
        # trigger_vibration("wheelspin")
        return "ThrottleWarning", 'Throttle Warning'
    
    else:
        return "ThrottleNeutral", ""



@callback(
    Output('BrakeWarning', 'className'),
    Output('BrakeWarning', 'children'),
    Input("telemetry", "data")  # <-- Must match the Store ID
)
def Lockup(store_data):

    player_data = store_data["player"]

    if player_data['brake'] > 0.5 and (player_data['WheelSplipRatio'][2] < -0.15 or player_data['WheelSplipRatio'][3] < -0.15):
        # trigger_vibration("lockup")
        return "ThrottleWarning", 'Brake Warning'
    
    else:
        return "ThrottleNeutral", ""