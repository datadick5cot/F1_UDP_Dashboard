from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QAction
import subprocess



class BorderlessBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Remove window frame and make it full screen
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showMaximized()
        
        menu = self.menuBar()

        file_menu = menu.addMenu("&Options")
        
        Button1 = QAction("Dashboard 1", self)
        Button1.triggered.connect(lambda: self.load_page("index"))
        
        
        Button2 = QAction("Dashboard 2", self)
        Button2.triggered.connect(lambda: self.load_page("centre_display"))
        
        
        Telemetry = QAction("Telemetry", self)
        Telemetry.triggered.connect(lambda: self.load_page("telemetry"))
        
        Settings = QAction("Settings", self)
        Settings.triggered.connect(lambda: self.load_page("settings"))
        
        
        rivalsdashboard = QAction("Rival Dashboard", self)
        rivalsdashboard.triggered.connect(lambda: self.load_page("rival"))
        
        shutdown = QAction("Shutdown", self)
        shutdown.triggered.connect(self.shutdown_pi())
        
        openterminal = QAction("Terminal Window", self)
        
        
        file_menu.addAction(Button1)
        file_menu.addAction(Button2)
        file_menu.addSeparator()
        file_menu.addAction(Telemetry)
        file_menu.addAction(Settings)
        file_menu.addAction(rivalsdashboard)
        
        file_menu.addSeparator()
        file_menu.addAction(openterminal)
        file_menu.addAction(shutdown)
        

        # Central widget and layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Web view
        self.webview = QWebEngineView()
        layout.addWidget(self.webview)
        self.setCentralWidget(central_widget)

        # Load HTML served from FastAPI
        self.webview.load(QUrl("http://localhost:8000/dashboard"))
        
            
        
    def shutdown_pi(self):
        reply = QMessageBox.question(self, 
                                    "Shutdown", 
                                    "Are you shure you want to Shutdown?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
                subprocess.run(["sudo", "shutdown", "-h", "now"])
                
    def open_terminal(self):
        subprocess.Popen(['lxterminal'])
            


    def load_page(self, page_name):
        url = f"http://localhost:8000/dashboard/{page_name}.html"
        self.webview.load(QUrl(url))

