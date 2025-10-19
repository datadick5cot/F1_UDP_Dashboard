import plotly.graph_objects as go
import dash 
# from dash import dcc, Input, Output, callback, html
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import DashProxy, dcc, html, Input, Output, ClientsideFunction, clientside_callback
import dash_bootstrap_components as dbc
from collections import deque
from codeassets import graph_config, graph_backgrounds
from dash import callback
from dash.dependencies import Input, Output



# Placeholder gauge
def placeholder_figure(title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=0,
        title={"text": title},
        gauge={"axis": {"range": [0.0, 5.0]}}
    ))
    fig.update_layout(margin=dict(t=30, b=0, l=0, r=0), **graph_backgrounds)
    return fig


dash.register_page(__name__, name='trailbrake', path='/trailbrake')


layout = dbc.Container([
    
    
    dbc.Row([dbc.Col([html.Div(id='speed', style={'font-size': '30px', 
                                                  'text-align': 'center'})])]),
    dbc.Row([

        dbc.Col([dcc.Graph(id='FL_Slip', figure=placeholder_figure("Front Left"), config=graph_config, style={"height": "250px"})], width=6, class_name='borders'),
        dbc.Col([dcc.Graph(id='FR_Slip', figure=placeholder_figure("Front Right"), config=graph_config, style={"height": "250px"})], width=6, class_name='borders')
    ]),
    dbc.Row([

        dbc.Col([dcc.Graph(id='RL_Slip', figure=placeholder_figure("Rear Left"), config=graph_config, style={"height": "250px"})], width=6, class_name='borders'),
        dbc.Col([dcc.Graph(id='RR_Slip', figure=placeholder_figure("Rear Right"), config=graph_config, style={"height": "250px"})], width=6, class_name='borders')
    ]),
   
])


@callback(
    Output('RL_Slip', 'figure'),
    Output('RR_Slip', 'figure'),
    Output('FL_Slip', 'figure'),
    Output('FR_Slip', 'figure'),
    Output('speed', 'children'),
    Input("telemetry", "data")
)
def Wheel_Spin(store_data):
    
    if not store_data or "MotionEx" not in store_data:
        raise PreventUpdate

    try:
        telemetry = store_data.get("Telemetry", {})
        car_data = telemetry.get("m_carTelemetryData", [])
        player_index = store_data.get('PlayerIndex', 0)
        player_data = car_data[player_index]
            
        motionex = store_data.get("MotionEx", {})
        
        # Ratio of slip (difference between tyre linear speed & car speed)
        wheelslipratio = motionex.get("m_wheelSlipRatio", [0.0, 0.0, 0.0, 0.0])
        
        # Lateral slip angle
        slipAngle = motionex.get("m_wheelSlipAngle", [0.0, 0.0, 0.0, 0.0])
        
        wheelspeed = motionex.get("m_wheelSpeed", [0.0, 0.0, 0.0, 0.0])
   
        def wheelGraph(title, value, wheelspeed): 
            
            if wheelspeed < 0:
                wheelspeed = 0
            else:
                wheelspeed = round(wheelspeed, 2)
            
            title = f'{title} = {wheelspeed} KPH'
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=value,
                title={"text": title},
                gauge={"axis": {"range": [0.0, 1.0]}}
            ))
            fig.update_layout(margin=dict(t=30, b=0, l=0, r=0), **graph_backgrounds)
            
            return fig


        RL = wheelGraph('Rear Left', slipAngle[0], wheelspeed[0])
        RR = wheelGraph('Rear Right', slipAngle[1], wheelspeed[1])
        FL = wheelGraph('Front Left', slipAngle[2], wheelspeed[2])
        FR = wheelGraph('Front Left', slipAngle[3], wheelspeed[3])
        
    except Exception as e:
        print(f"[ERROR] Failed to build telemetry graphs: {e}")

    return RL, RR, FL, FR, f'{player_data.get('m_speed', 0)} KPH'

