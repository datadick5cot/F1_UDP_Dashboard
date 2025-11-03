from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from UDP.UDP_Speed import get_latest_data


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


def run_listening():
    """Run the FastAPI (Uvicorn) server in a background thread."""
    uvicorn.run(tel_app, host="0.0.0.0", port=8000, log_level="info")

