import sys
import os
import threading
from UDP.fastapi_server import run_listening
from UDP.UDP_Speed import start_udp_background
from UI.Browser import BorderlessBrowser
from PyQt6.QtWidgets import QApplication


from UDP.fastapi_server import ip


print(f"connect to {ip}")

# ------------------ MAIN ENTRY POINT ------------------
if __name__ == "__main__":
    # Start UDP telemetry collection
    start_udp_background()

    # Start FastAPI server in background thread
    server_thread = threading.Thread(target=run_listening, daemon=True)
    server_thread.start()

    # Start PyQt application
    app = QApplication(sys.argv)
    browser = BorderlessBrowser()
    browser.show()

    try:
        sys.exit(app.exec())
    except AttributeError:
        sys.exit(app.exec_())
