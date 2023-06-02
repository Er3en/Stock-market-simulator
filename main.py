import sys
from PyQt5.QtWidgets import QApplication
from src.window.utils import set_window_to_display_resolution
from src.window.gui import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
set_window_to_display_resolution(window, app)