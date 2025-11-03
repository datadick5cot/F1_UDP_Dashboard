from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView

from PyQt6.QtWidgets import QToolBar
from PyQt6.QtGui import QAction



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

