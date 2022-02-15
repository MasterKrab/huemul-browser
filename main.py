from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase
from components.tool_bar import ToolBar
from components.main import Main
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Browser")

        self.setWindowState(Qt.WindowState.WindowMaximized)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #282a36;
                color: #fff;
                border: none;
            }
        """)

        self.main = Main(self)

        self.tool_bar = ToolBar(self)
        self.addToolBar(self.tool_bar)

        self.setCentralWidget(self.main)

        self.main.add_tab()


app = QApplication(sys.argv)
QFontDatabase.addApplicationFont("assets/fonts/Poppins.ttf")
window = MainWindow()
window.show()

sys.exit(app.exec())
