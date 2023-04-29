import sys
import unittest
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtTest import QTest
from src.window.utils import resize_window_to_screen_size, show_window_and_run_event_loop, set_window_to_display_resolution
from src.window.gui import MainWindow
class TestResizeWindowToScreenSize(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()

    def tearDown(self):
        del self.window
        del self.app

    def test_window_is_resized_to_screen_size(self):
        resize_window_to_screen_size(self.window)
        screen = QDesktopWidget().screenGeometry()
        self.assertEqual(self.window.width(), screen.width())
        self.assertEqual(self.window.height(), screen.height())


if __name__ == '__main__':
    unittest.main()
