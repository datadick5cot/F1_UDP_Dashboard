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
        
        file_menu = menu.addMenu("&File")
        
        shutdown = QAction("Shutdown Pi", self)
        shutdown.triggered.connect(self.shutdown_pi)
        
        quit_app = QAction("Quit App", self)
        quit_app.triggered.connect(self.quit_app)

        file_menu.addAction(quit_app)
        file_menu.addSeparator()
        file_menu.addAction(shutdown)

        #Dashboard Options
        option_menu = menu.addMenu("&Options")
        
        Button1 = QAction("Dashboard 1", self)
        Button1.triggered.connect(lambda: self.load_page("dashboard-1"))
        
        
        Button2 = QAction("Dashboard 2", self)
        Button2.triggered.connect(lambda: self.load_page("dashboard-2"))
        
        
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

        self.apply_touch_styles()
        

        # Central widget and layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Web view
        self.webview = QWebEngineView()
        layout.addWidget(self.webview)
        self.setCentralWidget(central_widget)

        # Load HTML served from FastAPI
        self.webview.load(QUrl("http://localhost:8000/dashboard/dashboard-1.html"))

    def apply_touch_styles(self):
        # Scale sizes from screen height so it works on any display
        screen_h = QApplication.primaryScreen().availableGeometry().height()
        bar_h = max(70, int(screen_h * 0.10))     # menu bar height
        font_px = int(bar_h * 0.40)               # text size
        pad_v = int(bar_h * 0.20)
        pad_h = int(bar_h * 0.60)
    
        self.menuBar().setFixedHeight(bar_h)
        self.setStyleSheet(f"""
            QMenuBar {{
                background-color: #1e1e1e;
                color: white;
                font-size: {font_px}px;
                spacing: 12px;
            }}
            QMenuBar::item {{
                padding: {pad_v}px {pad_h}px;
                margin: 4px;
                border-radius: 8px;
                background: #333333;
            }}
            QMenuBar::item:selected,
            QMenuBar::item:pressed {{
                background-color: #e10600;
            }}
    
            QMenu {{
                background-color: #1e1e1e;
                color: white;
                font-size: {font_px}px;
                border: 2px solid #555555;
            }}
            QMenu::item {{
                padding: {pad_v}px {pad_h * 2}px {pad_v}px {pad_h}px;
                min-height: {int(bar_h * 0.6)}px;
            }}
            QMenu::item:selected {{
                background-color: #e10600;
            }}
            QMenu::separator {{
                height: 3px;
                background: #555555;
                margin: 6px 10px;
            }}
    
            /* Shutdown / Quit confirmation dialogs */
            QMessageBox {{
                font-size: {font_px}px;
            }}
            QMessageBox QLabel {{
                font-size: {font_px}px;
            }}
            QMessageBox QPushButton {{
                font-size: {font_px}px;
                min-width: {bar_h * 2}px;
                min-height: {bar_h}px;
            }}
        """)
        
            
        
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

