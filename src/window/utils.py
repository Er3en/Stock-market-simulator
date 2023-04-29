import sys
from PyQt5.QtWidgets import QDesktopWidget


def set_window_to_display_resolution(window, app):
   
    # Get the size of the primary screen
    screen = QDesktopWidget().screenGeometry()

    # Set the window size to match the screen size
    window.resize(screen.width(), screen.height())

    # Move the window to the top left corner of the screen
    window.move(0, 0)

    # Show the window
    window.show()

    # Start the event loop
    sys.exit(app.exec_())