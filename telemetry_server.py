from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from UDP_Speed import start_udp_background, get_latest_data
import threading


tel_app = FastAPI()
tel_app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


start_udp_background()

@tel_app.get("/telemetry")
def telemetry():
    return get_latest_data()


def run_listening():
    uvicorn.run(tel_app, host="localhost", port=8000)


# if __name__ == "__main__":  
#     run_listening()

