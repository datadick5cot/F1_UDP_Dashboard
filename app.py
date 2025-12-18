import sys
import os
import threading
# from UDP.fastapi_server import run_listening
from UDP.fastapi_server import TelemetryServer
from UDP.F1_2024 import start_udp_background
from UI.Browser import BorderlessBrowser
from PyQt6.QtWidgets import QApplication
from variables.settings_variables import ConfigureVariables
from PyQt6.QtGui import QPixmap
import sys
from PyQt6.QtWidgets import QSplashScreen
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parent

server = TelemetryServer(BASE_DIR)


# ------------------ MAIN ENTRY POINT ------------------
if __name__ == "__main__":
    #Load Config and save the Current IP Address
    c = ConfigureVariables()
    #Load Variables at prior to Start
    c.load_config()
    # Set current ip address and save to config file
    c.save_config()
    
    # Start UDP telemetry collection
    start_udp_background()

    # Start FastAPI server in background thread
    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()
         
    # Start PyQt application
    app = QApplication(sys.argv)
   
    current_path = os.path.dirname(os.path.realpath(__file__))
    
    pixmap = QPixmap(f"{BASE_DIR}/UI/DDD_Splash.png")
    
    if pixmap.isNull():
        print("Splash image not found!")

    splash = QSplashScreen(pixmap)
    splash.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
    splash.show()
    splash.showMessage("Loading Dashboard...", Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)
    app.processEvents()

    # Simulate loading work (e.g. configs, threads)
    time.sleep(2)  # keep splash visible for 2 seconds

    browser = BorderlessBrowser()

    # Get available screen geometry
    screen = QGuiApplication.primaryScreen()
    rect = screen.availableGeometry()

    browser.move(
        rect.center().x() - browser.width() // 2,
        rect.center().y() - browser.height() // 2
    )

    browser.show()
    splash.finish(browser)

    try:
        sys.exit(app.exec())
    except AttributeError:
        sys.exit(app.exec_())

