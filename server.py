
from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc

dashapp = Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE], use_pages=True)

# Add a simple top-level layout that includes the page container required for multipage apps
dashapp.layout = html.Div([
    dcc.Interval(id='interval_component', interval=500, n_intervals=0),
    dcc.Store(id='telemetry', storage_type='memory'),
    html.Div(page_container)   # <-- REQUIRED when use_pages=True
])

