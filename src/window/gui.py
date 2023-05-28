import sys
from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QDockWidget, QTextEdit, QWidget, QHBoxLayout, QVBoxLayout, QDialog, QLabel, QLineEdit, QDialogButtonBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPainter, QMouseEvent
from PyQt5.QtChart import QChart, QChartView
from .login import verify_login


from ..twelvedata_api.stocks_in_time import get_stock_information

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class ChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_chart(self, df):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(df['close'])
        ax.set_title("TITLE")
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        self.canvas.draw()


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 150)

        self.login_label = QLabel("Login:")
        self.login_edit = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.login_label)
        self.layout.addWidget(self.login_edit)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_edit)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_login(self):
        self.login_edit = self.login_edit.text()

    def get_password(self):
        self.password_edit = self.password_edit.text()

    def verify(self):
        print(self.login_edit, self.password_edit)
        verify_login(self.login_edit, self.password_edit)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = get_stock_information(symbol="AMD",start_date="04/28/2023", end_date="05/25/2023")
        self.init_apperance()
        self.create_menu()
        self.create_user_panel()
        self.create_central_widget()
        

    def init_apperance(self):
        self.setWindowTitle("Stock Market App")
        icon = QIcon("src/assets/icon_256x256.png")
        self.setWindowIcon(icon)

    def create_menu(self):
        menubar = self.menuBar()
        user_menu = QMenu("User", self)
        menubar.addMenu(user_menu)

        login_action = QAction("Login", self)
        login_action.triggered.connect(self.show_login_dialog)
        logout_action = QAction("Logout", self)
        logout_action.triggered.connect(self.logout)
        user_menu.addAction(login_action)
        user_menu.addAction(logout_action)

    def create_user_panel(self):
        self.user_panel = QDockWidget("User Panel", self)
        self.user_panel.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.user_panel)

        self.user_widget = QWidget()
        self.user_layout = QVBoxLayout(self.user_widget)
        self.user_label = QTextEdit("Welcome to the Stock Market App!")
        self.user_layout.addWidget(self.user_label)
        self.user_panel.setWidget(self.user_widget)

    def create_central_widget(self):
        central_widget = QWidget()
        central_layout = QHBoxLayout(central_widget)
        graph_label = QTextEdit("Stock graphs will be displayed here")
        central_layout.addWidget(graph_label)
        self.setCentralWidget(central_widget)

    # def show_login_dialog(self):
    #     dialog = LoginDialog()
    #     if dialog.exec_() == QDialog.Accepted:
    #         dialog.get_login()
    #         dialog.get_password()
    #         #self.open_new_window(login, password)
    #         dialog.verify()
    

    def open_new_window(self, login, password):
        new_window = QMainWindow()
        new_window.setWindowTitle("New Window")
        new_window.setCentralWidget(QTextEdit(f"Login: {login}\nPassword: {password}"))
        new_window.show()

    def logout(self):
        self.user_layout.removeWidget(self.user_label)
        self.user_label.deleteLater()
        self.user_label = QTextEdit("You have been logged out")
        self.user_layout.addWidget(self.user_label)

    def create_chart_widget(self):
        self.chart_widget = ChartWidget()
        self.chart_widget.update_chart(self.df)
        self.setCentralWidget(self.chart_widget)

    def create_central_widget(self):
        self.setCentralWidget(None)  # Remove previous central widget
        self.create_chart_widget()

    def show_login_dialog(self):
        dialog = LoginDialog()
        if dialog.exec_() == QDialog.Accepted:
            dialog.get_login()
            dialog.get_password()
            dialog.verify()
            if dialog.is_verified():  # Assuming you have a method to check if login is verified
                self.create_central_widget()  # Update the chart widget after successful login
