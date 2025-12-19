from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import json
import socket
from pathlib import Path

from UDP.F1_2024 import get_latest_data


class TelemetryServer:
    def __init__(self, base_dir):
        # self.base_dir = Path(__file__).resolve().parent
        self.base_dir = base_dir
        self.app = FastAPI()

        self._setup_cors()
        self._setup_static_files()
        self._setup_routes()

    # ------------------ SETUP METHODS ------------------

    def _setup_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_static_files(self):
        html_dir = self.base_dir / "page"
        self.app.mount(
            "/dashboard",
            StaticFiles(directory=str(html_dir), html=True),
            name="dashboard"
        )

    def _setup_routes(self):
        @self.app.get("/telemetry")
        def telemetry():
            return get_latest_data()

        @self.app.get("/config")
        def get_config():
            config_path = os.path.expanduser("~/.config/sim_racing_dash.json")
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    return json.load(f)

            return {"IPaddress": self.get_local_ip()}

    # ------------------ UTILITY METHODS ------------------

    @staticmethod
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return None

    # ------------------ RUN SERVER ------------------

    def run(self, host="0.0.0.0", port=8000):
        uvicorn.run(self.app, host=host, port=port, log_level="info")
        
        
