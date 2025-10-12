
import plotly.graph_objects as go
import dash 
from dash import dcc, Input, Output, callback, html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import threading
from collections import deque
from codeassets import graph_config, graph_backgrounds, create_loading_figure

# Store telemetry data for only the current lap

dash.register_page(__name__, name='trial', path='/trial')

layout = dbc.Container([
    html.H1('TimeTrial Vs'),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='vs_throttle', config=graph_config, style={"height": "300px"}),
            ], width=6),
        dbc.Col([
            dcc.Graph(id='vs_brake', config=graph_config, style={"height": "300px"}),
            ], width=6),
        
        ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='speed_graph', config=graph_config, style={"height": "300px"}),
            ], width=12),
        ]),
    
    
    dbc.Row([
        dbc.Col(
            [html.Div(id='player_gear')], width=6),
         dbc.Col(
            [html.Div(id='rival_gear')], width=6),
])
    

    
    
    ]),


@callback(
    Output("speed_graph", "figure"),
    Output("vs_throttle", "figure"),
    Output("vs_brake", "figure"),
    Output("player_gear", 'children'),
    Output("rival_gear", 'children'),
    Input("telemetry", "data")  # <-- Must match the Store ID
)
def update_speed_graph(store_data):
    

    if not store_data or "player" not in store_data or "rival" not in store_data:
        return create_loading_figure(), create_loading_figure(), create_loading_figure()

    player_data = store_data["player"]
    rival_data = store_data["rival"]

    if not player_data or not rival_data:
        raise dash.exceptions.PreventUpdate

    # Extract lists
    player_distances = [p["DistanceLap"] for p in player_data]
    player_speeds = [p["speed"] for p in player_data]

    rival_distances = [r["DistanceLap"] for r in rival_data]
    rival_speeds = [r["speed"] for r in rival_data]

    # Use the latest point for total lap distance
    totalLapDistance = player_data[-1]["TotalDistance"]

    if player_distances[-1] < 0:
        raise dash.exceptions.PreventUpdate

    else:
        
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=player_distances,
            y=player_speeds,
            mode='lines',
            name='Player',
            line=dict(color='royalblue', width=4)
        ))

        fig.add_trace(go.Scatter(
            # x=rival_distances,
            x=player_distances,
            y=rival_speeds,
            mode='lines',
            name='Rival',
            line=dict(color='firebrick', width=4)
        ))

        # Dynamic y-axis for speed
        max_speed = max(max(player_speeds, default=0), max(rival_speeds, default=0))

        fig.update_layout(
            title="Player vs Rival Speed Trace",
            xaxis_title="Distance Around Lap (m)",
            xaxis_range=[0,totalLapDistance],
            yaxis_title="Speed (kph)",
            yaxis_range=[0, max_speed + 20],
            autosize=True, **graph_backgrounds,
                    ),
        
        
        
        trottlefig = go.Figure()
  
        
        trottlefig.add_bar(y=[rival_data[-1]['throttle']], 
                           x=['rival'], showlegend=False)
        
        
        trottlefig.add_bar(y=[player_data[-1]['throttle']], 
                           x=['you'], showlegend=False)
        
        trottlefig.update_layout(yaxis_range=[0,1],
                                 autosize=True, **graph_backgrounds,
                    ),
        
        brakefig = go.Figure()
        
        brakefig.add_bar(y=[rival_data[-1]['brake'], player_data[-1]['brake']], 
                           x=['rival', 'you'], showlegend=False)
        
        brakefig.update_layout(yaxis_range=[0,1],
                               autosize=True, **graph_backgrounds,
                    )
        
        player_gear = f"Your Gear: {player_data[-1]['gear']}"
        rival_gear = f"Rival Gear : {rival_data[-1]['gear']}"
        
        return fig, trottlefig, brakefig, player_gear, rival_gear
