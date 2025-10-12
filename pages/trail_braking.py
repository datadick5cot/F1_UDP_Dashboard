
import plotly.graph_objects as go
import dash 
from dash import dcc, Input, Output, callback
import dash_bootstrap_components as dbc

import threading
from collections import deque
from codeassets import graph_config, graph_backgrounds, create_loading_figure

HISTORY_LIMIT = 100  # store N data points
telemetry_history = deque(maxlen=HISTORY_LIMIT)
history_lock = threading.Lock()


dash.register_page(__name__, name='trailbrake', path='/trailbrake')
# Dash.register_page(__name__, path='/')

layout = dbc.Container([


    dbc.Row([
        dbc.Col([
            dcc.Graph(id='x_y_graph', config=graph_config, style={"height": "300px"}),
         ], width=5),
        
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar_graph', config=graph_config, style={"height": "300px"}),
         ], width=4),
        
        dbc.Col([
            dcc.Graph(id='line_graph', config=graph_config, style={"height": "300px"}),
        ], width=8),
    ]),
])



# --- Dash Callback to Update Graph ---
@callback(
    Output('x_y_graph', 'figure'),
    Output('line_graph', 'figure'),
    Output('bar_graph', 'figure'),
    Input('interval_component', 'n_intervals')
)
def update_graph(n_intervals):
    """
    Plot the entire telemetry history instead of just the latest point.
    """
    with history_lock:
        if not telemetry_history:
            # raise PreventUpdate
            loading_figure = create_loading_figure()
            return loading_figure, loading_figure, loading_figure
        
        # Extract data
        y_vals = [item["acceleration_grip"] for item in telemetry_history]
        x_vals = [item["steer"] for item in telemetry_history]
        throttle_y = [item["throttle"] for item in telemetry_history]
        brake_y = [item["brake"] for item in telemetry_history]

    fig_b_a = go.Figure()

    fig_b_a.add_scatter(y=throttle_y, 
                        x=list(range(0,HISTORY_LIMIT)),
                        line=dict(color='green', width=4),
                        name='throttle')
    

    fig_b_a.add_scatter(y=brake_y, 
                        x=list(range(0,HISTORY_LIMIT)),
                        line=dict(color='red', width=4),
                        name='brakes')
    
    

    fig_b_a.update_layout(
                    # yaxis=dict(visible=False),
                    xaxis=dict(visible=False),
                    margin=dict(l=20, r=20, t=20, b=20), 
                    autosize=True, **graph_backgrounds,
                    )
    fig_b_a.update_yaxes(range=[0,1], title="Throttle - Brake)")
    
    fig_b_a.update_xaxes(range=[0,100], title="Time")

    fig = go.Figure()

    # Show full trail
    fig.add_scatter(
        x=x_vals,
        y=y_vals,
        mode='lines+markers',
        line=dict(color='blue', width=2),
        marker=dict(size=5, color='red'),
        name="Telemetry Trail"
    )

    # Add latest point highlighted
    fig.add_scatter(
        x=[x_vals[-1]],
        y=[y_vals[-1]],
        mode='markers',
        marker=dict(size=20, color='orange'),
        name="Latest Point"
    )

    # Keep ranges fixed for better visibility
    fig.update_yaxes(range=[-1, 1],)
    fig.update_xaxes(range=[-1, 1],)

    
    fig.update_layout(title="Real-Time Car Telemetry", 
                    autosize=True, **graph_backgrounds,
                    )
    
    
    fig_bar = go.Figure()
    
    xNamesvalue = ['Throttle', 'Brake']

    
    fig_bar = go.Figure(data=[
                go.Bar(name='Throttle', x=xNamesvalue, y=[throttle_y[-1]], marker_color='Green', showlegend=False),
                go.Bar(name='Brake', x=xNamesvalue, y=[brake_y[-1]], marker_color='Red', showlegend=False)
            ])
    
    fig_bar.update_yaxes(range=[0, 1])
    
    fig_bar.update_layout(
                    **graph_backgrounds,
                    )

    return fig, fig_b_a, fig_bar


