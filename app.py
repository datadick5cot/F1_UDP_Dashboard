import sys
import os
import threading
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from UDP_Speed import start_udp_background, get_latest_data
from PyQt6.QtWidgets import QToolBar
from PyQt6.QtGui import QAction


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
html_dir = os.path.abspath("F1_Dashboard/page")

# print("Serving HTML from:", html_dir)

tel_app.mount("/dashboard", StaticFiles(directory=html_dir, html=True), name="dashboard")

@tel_app.get("/telemetry")
def telemetry():
    """Return the latest telemetry data."""
    return get_latest_data()


def run_listening():
    """Run the FastAPI (Uvicorn) server in a background thread."""
    uvicorn.run(tel_app, host="0.0.0.0", port=8000, log_level="info")


# ------------------ PYQT SETUP ------------------

class BorderlessBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Remove window frame and make it full screen
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showMaximized()
        
        toolbar = QToolBar("--Toolbar--")
        toolbar.setOrientation(Qt.Orientation.Vertical)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, toolbar)

        # Toolbar button
        Button1 = QAction("Dashboard", self)
        Button1.triggered.connect(lambda: self.load_page("index"))
        toolbar.addAction(Button1)
        
        
        # Toolbar button
        Button2 = QAction("Telemetry", self)
        Button2.triggered.connect(lambda: self.load_page("telemetry"))
        toolbar.addAction(Button2)
        
        # Toolbar button
        Button3 = QAction("Vs Rival", self)
        Button3.triggered.connect(lambda: self.load_page("rival"))
        toolbar.addAction(Button3)
        
        # Toolbar button
        Button4 = QAction("Settings", self)
        Button4.triggered.connect(lambda: self.load_page("settings"))
        toolbar.addAction(Button4)
        
        toolbar.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        toolbar.addAction(exit_action)


        # Central widget and layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Web view
        self.webview = QWebEngineView()
        layout.addWidget(self.webview)
        self.setCentralWidget(central_widget)

        # Load HTML served from FastAPI instead of file://
        self.webview.load(QUrl("http://localhost:8000/dashboard"))


    def load_page(self, page_name):
        url = f"http://localhost:8000/dashboard/{page_name}.html"
        self.webview.load(QUrl(url))


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
