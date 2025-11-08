from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from UDP.UDP_Speed import get_latest_data
import json
import socket



def get_local_ip():    
    try:
        # Connect to a public server (Google DNS, for example)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # We never actually send data
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        pass

# ------------------ FASTAPI SETUP ------------------

tel_app = FastAPI()

# Allow CORS (still good practice)
tel_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static HTML dashboard files
html_dir = os.path.abspath("F1_Dashboard/Sim_Dashboard/page")

# print("Serving HTML from:", html_dir)

tel_app.mount("/dashboard", StaticFiles(directory=html_dir, html=True), name="dashboard")

@tel_app.get("/telemetry")
def telemetry():
    """Return the latest telemetry data."""
    return get_latest_data()


@tel_app.get("/config")
def get_config():
    """Serve the sim_racing_dash.json config file."""
    config_path = os.path.expanduser("~/.config/sim_racing_dash.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return {'IPaddress' : get_local_ip()}


def run_listening():
    """Run the FastAPI (Uvicorn) server in a background thread."""
    uvicorn.run(tel_app, host="0.0.0.0", port=8000, log_level="info")

