import sys
from src.window.utils import set_window_to_display_resolution
from src.window.gui import MainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
# Create a QApplication instance
app = QApplication(sys.argv)
window = MainWindow()

#set_window_to_display_resolution(window, app)


