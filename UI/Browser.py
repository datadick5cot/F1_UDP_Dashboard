from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox, QApplication
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
        
        menu.setContentsMargins(20, 20, 20, 0)
        
        file_menu = menu.addMenu("&File")
        
        shutdown = QAction("Shutdown Pi", self)
        shutdown.triggered.connect(self.shutdown_pi)
        
        quit_app = QAction("Quit App", self)
        quit_app.triggered.connect(self.quit_app)
        file_menu.addAction(quit_app)
        
        file_menu.addAction(quit_app)
        file_menu.addAction(shutdown)
        

        #Dashboard Options
        option_menu = menu.addMenu("&Options")
        
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
        
        option_menu.addAction(Button1)
        option_menu.addAction(Button2)
        option_menu.addSeparator()
        option_menu.addAction(Telemetry)
        option_menu.addAction(Settings)
        option_menu.addAction(rivalsdashboard)
        

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
                                    "Are you sure you want to Shutdown?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
                subprocess.run(["sudo", "shutdown", "-h", "now"])
      

    def quit_app(self):
        reply = QMessageBox.question(
            self,
            "Quit",
            "Are you sure you want to quit the application?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            QApplication.instance().quit()

            


    def load_page(self, page_name):
        url = f"http://localhost:8000/dashboard/{page_name}.html"
        self.webview.load(QUrl(url))

