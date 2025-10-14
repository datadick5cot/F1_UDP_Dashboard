import sys
import threading
from PyQt6.QtWidgets import QMainWindow, QApplication, QToolBar
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QAction
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from codeassets import dont_lock, create_loading_figure
from UDP import udp_listener, get_latest_data
from server import dashapp
from dash.dependencies import Input, Output
import dash.exceptions
from collections import deque


# from UDP import ( 
#     history_lock,
#     motion_history,
#     motion_ex_history,
#     session_data,
#     lap_data_history,
#     event_data_history,
#     participants_data,
#     car_setups_data,
#     car_telemetry_history,
#     car_status_history,
#     classification_data,
#     lobby_info_data,
#     car_damage_history,
#     session_history_data,
#     tyre_sets_data,
#     time_trial_data
# )

udp_thread = threading.Thread(target=udp_listener, daemon=True)
udp_thread.start()


@dashapp.callback(
    Output("telemetry", "data"), 
    Input("interval_component", "n_intervals")
    )

def update_telemetry(n):
    data = get_latest_data()
    if not data:
        raise dash.exceptions.PreventUpdate
    return data

    
    # with history_lock:
    #     if not player_history or not rival_history:
    #         raise dash.exceptions.PreventUpdate  # nothing to show yet

    #     # Convert to regular lists for JSON serialization
    #     player_data = list(player_history)
    #     rival_data = list(rival_history)

    # # Return as dict for Dash
    # return {
    #     "player": player_data,
    #     "rival": rival_data
    # }


def run_dash():
    dashapp.run_server(port=8050, debug=False, use_reloader=False)

# --- Main Window ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("F1 Dashboard")

        toolbar = QToolBar("Main Toolbar")
        toolbar.setOrientation(Qt.Orientation.Vertical)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, toolbar)

        # Toolbar buttons
        Button1 = QAction("Race", self)
        Button1.triggered.connect(lambda: self.load_page("race"))
        toolbar.addAction(Button1)

        toolbar.addSeparator()

        Button2 = QAction("Trail Braking Training", self)
        Button2.triggered.connect(lambda: self.load_page("trailbrake"))
        toolbar.addAction(Button2)

        Button3 = QAction("Time Trial Vs", self)
        Button3.triggered.connect(lambda: self.load_page("trial"))
        toolbar.addAction(Button3)

        toolbar.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        toolbar.addAction(exit_action)

        self.view = QWebEngineView()
        self.view.load(QUrl("http://127.0.0.1:8050"))  # Default page
        self.setCentralWidget(self.view)

    def load_page(self, page):
        self.view.load(QUrl(f"http://127.0.0.1:8050/{page}"))

# --- Start Background Threads ---
threading.Thread(target=run_dash, daemon=True).start()
threading.Thread(target=dont_lock, daemon=True).start()

# --- Start Qt App ---
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())