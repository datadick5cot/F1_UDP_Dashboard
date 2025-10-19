import plotly.graph_objects as go
import dash 
# from dash import dcc, Input, Output, callback, html
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import DashProxy, dcc, html, Input, Output, ClientsideFunction, clientside_callback

import dash_bootstrap_components as dbc

from collections import deque
from codeassets import graph_config, graph_backgrounds, create_loading_figure


from dash import callback
from dash.dependencies import Input, Output


# Placeholder gauge
def create_placeholder_figure(title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=0,
        title={"text": title},
        gauge={"axis": {"range": [0, 100]}}
    ))
    fig.update_layout(margin=dict(t=30, b=0, l=0, r=0), **graph_backgrounds)
    return fig


dash.register_page(__name__, name='race', path='/race')


layout = dbc.Container([
    dbc.Row(dbc.Col(dcc.Graph(id="rev_lights", style={"height": "80px", "width": "100%"}), width=12, class_name='borders')),
    
    dbc.Row([
        dbc.Col([html.Div(id='BrakeWarning', className='ThrottleNeutral')], width=4, class_name='borders_no_top_no_bottom'),
        dbc.Col([html.Div(id='blankspace')], width=4, class_name='borders_no_top_no_bottom'),
        dbc.Col([html.Div(id='ThrottleWarning', className='ThrottleNeutral')], width=4, class_name='borders_no_top_no_bottom')
    ]),
    dbc.Row([
        
        dbc.Col([dcc.Graph(id='brakeGraph', figure=create_placeholder_figure("Brake (%)"), config=graph_config, style={"height": "180px"})], width=4, class_name='borders'),
        dbc.Col([html.H4('Gear'), html.Div(id='GearDisplay', style={"height": "180px"}, className='gear_display')], width=4, class_name='borders'),
        dbc.Col([dcc.Graph(id='throttleGraph', figure=create_placeholder_figure("Brake (%)"), config=graph_config, style={"height": "180px"})], width=4, class_name='borders')
    ]),
   
])




@callback(
    Output('GearDisplay', 'children'),
    Input("telemetry", "data")  
)

def gear_update(store_data):
    gear = "N"  
    try:
        player_index = store_data.get('PlayerIndex', 0)
        telemetry = store_data.get("Telemetry", {})
        car_data = telemetry.get("m_carTelemetryData", [])
        gear = car_data[player_index].get("m_gear", "N")
        
        if gear == "-1":
            gear = 'R'
    except:
        pass
    
    return f"{gear}"



@callback(
    Output('throttleGraph', 'figure'),
    Output('brakeGraph', 'figure'),
    Input("telemetry", "data")  
)

def main(store_data):
    # ✅ Guard against missing data
    if not store_data or "Telemetry" not in store_data:
        raise PreventUpdate

    # ✅ Default fallback visuals
    throttle_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=0,
        title={"text": "Throttle (%)"},
        gauge={"axis": {"range": [0, 100]}}
    ))
    
    

    brake_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=0,  # Invert value for right-to-left effect
        title={"text": "Brake (%)"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "red"},
            "steps": [
                {"range": [0, 100 - brake_value], "color": "black"},
                {"range": [100 - brake_value, 100], "color": "red"}
            ]
        }
    ))



    # ✅ Apply layout polish
    throttle_fig.update_layout(margin=dict(t=30, b=0, l=0, r=0))
    brake_fig.update_layout(margin=dict(t=30, b=0, l=0, r=0))

    try:
        # ✅ Extract player index
        player_index = store_data.get('PlayerIndex', 0)
        telemetry = store_data.get("Telemetry", {})
        car_data = telemetry.get("m_carTelemetryData", [])

        # ✅ Validate and extract telemetry
        if isinstance(car_data, list) and len(car_data) > player_index:
            throttle = car_data[player_index].get("m_throttle", 0.0)
            brake = car_data[player_index].get("m_brake", 0.0)
       

            # ✅ Update figures with live data
            throttle_fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=throttle * 100,
                title={"text": "Throttle (%)"},
                gauge={"axis": {"range": [0, 100]}}
            ))
            throttle_fig.update_layout(margin=dict(t=30, b=0, l=0, r=0))
            
            throttle_fig.update_layout(
                            **graph_backgrounds,
                            )


            brake_value = max(0, min(100, brake * 100))  # Clamp to [0, 100]

            brake_fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=100 - brake_value,  # Invert value for right-to-left effect
                title={"text": "Brake (%)"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "red"},
                    "steps": [
                        {"range": [0, 100 - brake_value], "color": "black"},
                        {"range": [100 - brake_value, 100], "color": "red"}
                    ]
                }
            ))


            
            brake_fig.update_layout(margin=dict(t=30, b=0, l=0, r=0))

            
            
            brake_fig.update_layout(
                            **graph_backgrounds,
                            )

    except Exception as e:
        print(f"[ERROR] Failed to build telemetry graphs: {e}")

    return throttle_fig, brake_fig


@callback(
    Output('ThrottleWarning', 'className'),
    Output('ThrottleWarning', 'children'),
    Output('BrakeWarning', 'className'),
    Output('BrakeWarning', 'children'),
    Input("telemetry", "data")
)
def Wheel_Spin(store_data):
    throttleclass = "ThrottleNeutral"
    throttlewords = ""
    brakeclass = "ThrottleNeutral"
    brakewords = ""

    try:
        player_index = store_data.get('PlayerIndex', 0)
        telemetry = store_data.get("Telemetry", {})
        car_data = telemetry.get("m_carTelemetryData", [])
        motionex = store_data.get("MotionEx", {})

        if not car_data or player_index >= len(car_data):
            return throttleclass, throttlewords, brakeclass, brakewords

        car = car_data[player_index]
        throttle = car.get("m_throttle", 0.0)
        brake = car.get("m_brake", 0.0)
        carspeed = max(car.get("m_speed", 0.0), 1)
        gear = car.get("m_gear", 0)

        wheelspeed = motionex.get("m_wheelSpeed", [0, 0, 0, 0])
        slipratiolist = motionex.get("m_wheelSlipRatio", [0, 0, 0, 0])
        slipanglelist = motionex.get("m_wheelSlipAngle", [0, 0, 0, 0])

        # --- Thresholds ---
        slip_angle_tolerance = 0.10
        slip_ratio_tolerance = 0.15
        slip_ratio_warning = 0.30
        speed_threshold = 20  # ignore below this

        # --- Derivatives ---
        rear_slip_ratio = max(slipratiolist[0], slipratiolist[1])
        front_slip_ratio = min(slipratiolist[2], slipratiolist[3])
        rear_slip_angle = max(abs(slipanglelist[0]), abs(slipanglelist[1]))
        front_slip_angle = max(abs(slipanglelist[2]), abs(slipanglelist[3]))
        rear_overspeed = max(wheelspeed[0], wheelspeed[1]) / carspeed

        # --- Driving phase detection ---
        if brake > 0.4 and carspeed > speed_threshold:
            phase = "Entry"
        elif throttle < 0.2 and brake < 0.2 and carspeed > speed_threshold:
            phase = "Mid"
        elif throttle > 0.4 and carspeed > speed_threshold:
            phase = "Exit"
        else:
            phase = "Cruise"

        # --- Phase-based Coaching ---
        if phase == "Entry":
            # too much brake or front slip
            if front_slip_ratio < -slip_ratio_warning or front_slip_angle > slip_angle_tolerance * 1.5:
                brakeclass = "ThrottleWarning"
                brakewords = f"Lockup Detected — Ease brake earlier next corner."
            elif brake > 0.8:
                brakeclass = "ThrottleWarning"
                brakewords = f"Heavy braking — consider smoother trail braking for rotation."

        elif phase == "Mid":
            # if under-rotating
            if abs(front_slip_angle) < slip_angle_tolerance * 0.6:
                throttleclass = "ThrottleWarning"
                throttlewords = "Car not rotating — release brake earlier or carry more entry speed."

        elif phase == "Exit":
            if rear_slip_angle > slip_angle_tolerance * 1.2 and rear_slip_ratio > slip_ratio_tolerance:
                throttleclass = "ThrottleWarning"
                throttlewords = f"Rear sliding — reduce throttle to increase traction."
            elif rear_slip_ratio > slip_ratio_warning or rear_overspeed > 1.12:
                throttleclass = "ThrottleWarning"
                throttlewords = f"Wheelspin Detected — ease throttle earlier next corner."

    except Exception as e:
        print(f"[ERROR] WheelSpin detection failed: {e}")

    return throttleclass, throttlewords, brakeclass, brakewords


@callback(
    Output('rev_lights', 'figure'),
    Input("telemetry", "data")
)
def rev_lights(store_data):
    revgraph = go.Figure()
    # 15 LEDs
    leds = 15
    yaxis = [0] * leds
    xaxis = list(range(1, leds + 1))
    size = [20] * leds

    # Color zones (left/center/right)
    colors_rgb = [
        (235, 168, 61),  # amber (low rev zone)
        (235, 64, 52),   # red   (mid rev zone)
        (61, 87, 235)    # blue  (top rev zone)
    ]

    # default: all dim (no data)
    active_mask = 0
    active_count = 0
    use_bitmask = False
    rev_percent = None

    try:
        player_index = store_data.get('PlayerIndex', 0)
        telemetry = store_data.get("Telemetry", {})
        car_data = telemetry.get("m_carTelemetryData", [])

        if not car_data or player_index >= len(car_data):
            # no telemetry — render dim LEDs
            active_mask = 0
            active_count = 0
        else:
            cd = car_data[player_index]
            # Prefer bitmask if available
            rev_bitvalue = cd.get("m_revLightsBitValue", None)
            rev_percent = cd.get("m_revLightsPercent", None)  # optional fallback

            if isinstance(rev_bitvalue, int) and rev_bitvalue >= 0:
                use_bitmask = True
                active_mask = rev_bitvalue
                # count bits set (for information)
                active_count = bin(active_mask).count("1")
            elif isinstance(rev_percent, (int, float)):
                # fallback: percent -> number of LEDs to show
                active_count = int(max(0, min(100, rev_percent)) / 100.0 * leds + 0.5)
                # create mask: activate lowest N leds (left->right)
                active_mask = 0
                for i in range(active_count):
                    active_mask |= (1 << i)
            else:
                # nothing available
                active_mask = 0
                active_count = 0

    except Exception as e:
        # don't let revlights crash the app
        print(f"[ERROR] rev_lights build failed: {e}")
        active_mask = 0
        active_count = 0

    # Build color/opacity for each LED
    color_list = []
    for i in range(leds):
        # choose color zone
        if i < 4:                           # left 4 = amber
            rgb = colors_rgb[0]
        elif i >= leds - 4:                 # right 4 = blue
            rgb = colors_rgb[2]
        else:                               # middle = red
            rgb = colors_rgb[1]

        # check if this LED is active via bitmask (bit 0 = leftmost)
        led_on = bool((active_mask >> i) & 1)

        # opacity: active = 1.0, inactive = 0.18 (a nice dim)
        alpha = 1.0 if led_on else 0.18

        rgba = f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})'
        color_list.append(rgba)

    # Add marker trace
    revgraph.add_trace(go.Scatter(
        x=xaxis,
        y=yaxis,
        mode='markers',
        marker=dict(size=size, color=color_list),
        hoverinfo='skip',
    ))

    # Layout: compact, no axis
    revgraph.update_layout(
        height=50,
        autosize=True,
        margin=dict(t=0, b=0, l=0, r=0),
        xaxis=dict(showline=False, showticklabels=False, showgrid=False, zeroline=False, fixedrange=True),
        yaxis=dict(showline=False, showticklabels=False, showgrid=False, zeroline=False, fixedrange=True),
        **graph_backgrounds,
    )

    return revgraph

