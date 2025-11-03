import plotly_express as px 
import pyautogui
import time


def calc_wheel_traction(data):
    car_data = data.get("Telemetry", {}).get("m_carTelemetryData", [])
    surface_type = car_data[data.get('PlayerIndex', 0)].get("m_surfaceType", [0, 0, 0, 0])

    motionex = data.get("MotionEx", {})
    slip_ratio = motionex.get("m_wheelSlipRatio", [0, 0, 0, 0])
    slip_angle = motionex.get("m_wheelSlipAngle", [0, 0, 0, 0])

    surface_penalty_map = {
        0: 0.0,  # tarmac
        1: 0.1,  # rumble strip
        2: 0.3,  # concrete
        3: 0.4,  # grass
        4: 0.5,  # gravel
        5: 0.7,  # mud/sand
        6: 0.5,  # cobbles
        7: 0.2,  # painted
    }

    traction = []
    for i in range(4):
        sr = abs(slip_ratio[i])
        sa = abs(slip_angle[i])
        penalty = surface_penalty_map.get(surface_type[i], 0.0)

        # Rear wheels have higher natural slip under throttle
        if i in (0, 1):  # RL, RR
            slip_ratio_limit = 0.20
            slip_angle_limit = 8.0
        else:  # FL, FR
            slip_ratio_limit = 0.10
            slip_angle_limit = 6.0

        t = 1.0 - (sr / slip_ratio_limit) - (sa / slip_angle_limit) - penalty
        t = max(0.0, min(1.0, t))
        traction.append(t)

    return traction  # [RL, RR, FL, FR]

def dont_lock():
        while True:
                time.sleep(60)
                pyautogui.moveTo(100, 100, duration = 0.1)
                time.sleep(60)
                pyautogui.moveTo(50, 50, duration = 0.1)

def format_lap_time(ms):
    total_seconds = ms / 1000
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:04.1f}"


def extract_temp(index, tel):
    brake = tel['m_brakesTemperature'][index]
    carcas = tel['m_tyresInnerTemperature'][index]
    surface = tel['m_tyresSurfaceTemperature'][index]

    return [brake, carcas, surface]




# Define the range and colors
heatrange = list(range(0, 600, 70))  # [0, 70, 140, ..., 560]
colors = px.colors.sequential.Rainbow

# Ensure the lengths match by trimming if necessary
if len(colors) > len(heatrange):
    colors = colors[:len(heatrange)]
elif len(heatrange) > len(colors):
    heatrange = heatrange[:len(colors)]


# Function to map an integer value to a color
def value_to_color(value: int) -> str:
    for i in range(len(heatrange) - 1):
        if heatrange[i] <= value < heatrange[i + 1]:
            return colors[i]
    return colors[-1]  # For values >= heatrange[-1]

def temp_colours_map(brakes, carcass, surface):
    carcastemp = {
        'width': '80px',
        'height': '80px',
        'border-radius': '50%',
        'position': 'absolute',
        'top': '10px',
        'left': '10px',
        'z-index': '1',
        'border' : '2px solid white'
    }

    surfacetemp = {
        'width': '60px',
        'height': '60px',
        'border-radius': '50%',
        'position': 'absolute',
        'top': '20px',
        'left': '20px',
        'z-index': '2',
        'border' : '2px solid white'
    }

    braketemps = {
        'width': '40px',
        'height': '40px',
        'border-radius': '50%',
        'position': 'absolute',
        'top': '30px',
        'left': '30px',
        'z-index': '3',
        'border' : '2px solid white'
    }


    braketemps['background'] = value_to_color(brakes)
    carcastemp['background'] = value_to_color(carcass)
    surfacetemp['background'] = value_to_color(surface)

    return braketemps, carcastemp, surfacetemp

import plotly.graph_objects as go

def create_loading_figure():    
    return go.Figure().update_layout(
        paper_bgcolor="black",
        plot_bgcolor="black",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[{
            "text": "Loading...",
            "x": 0.5,
            "y": 0.5,
            "xref": "paper",
            "yref": "paper",
            "showarrow": False,
            "font": {"size": 28, "color": "white"}
        }]
    )
