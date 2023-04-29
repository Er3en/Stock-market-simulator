import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QDockWidget, QTextEdit, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and icon
        self.setWindowTitle("Stock Market App")
        self.setWindowIcon(QIcon("icon.png"))

        # Create a menu bar and add menus
        menubar = self.menuBar()
        user_menu = QMenu("User", self)
        menubar.addMenu(user_menu)
        
        # Add actions to the menus
        login_action = QAction("Login", self)
        logout_action = QAction("Logout", self)
        user_menu.addAction(login_action)
        user_menu.addAction(logout_action)

        # Create a dock widget for the user panel
        user_panel = QDockWidget("User Panel", self)
        user_panel.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, user_panel)

        # Add a widget to the user panel
        user_widget = QWidget()
        user_layout = QVBoxLayout(user_widget)
        user_label = QTextEdit("Welcome to the Stock Market App!")
        user_layout.addWidget(user_label)
        user_panel.setWidget(user_widget)

        # Create a central widget for the stock graphs
        central_widget = QWidget()
        central_layout = QHBoxLayout(central_widget)
        graph_label = QTextEdit("Stock graphs will be displayed here")
        central_layout.addWidget(graph_label)
        self.setCentralWidget(central_widget)



# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QDockWidget, QTextEdit, QWidget, QHBoxLayout, QVBoxLayout
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QIcon

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Set window title and icon
#         self.setWindowTitle("Stock Market App")
#         self.setWindowIcon(QIcon("icon.png"))

#         # Create a menu bar and add menus
#         menubar = self.menuBar()
#         user_menu = QMenu("User", self)
#         menubar.addMenu(user_menu)
        
#         # Add actions to the menus
#         login_action = QAction("Login", self)
#         logout_action = QAction("Logout", self)
#         user_menu.addAction(login_action)
#         user_menu.addAction(logout_action)

#         # Create a dock widget for the user panel
#         user_panel = QDockWidget("User Panel", self)
#         user_panel.setFeatures(QDockWidget.NoDockWidgetFeatures)
#         self.addDockWidget(Qt.LeftDockWidgetArea, user_panel)

#         # Add a widget to the user panel
#         user_widget = QWidget()
#         user_layout = QVBoxLayout(user_widget)
#         user_label = QTextEdit("Welcome to the Stock Market App!")
#         user_layout.addWidget(user_label)
#         user_panel.setWidget(user_widget)

#         # Create a central widget for the stock graphs
#         central_widget = QWidget()
#         central_layout = QHBoxLayout(central_widget)
#         graph_label = QTextEdit("Stock graphs will be displayed here")
#         central_layout.addWidget(graph_label)
#         self.setCentralWidget(central_widget)
