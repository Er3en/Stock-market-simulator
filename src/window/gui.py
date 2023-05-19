import sys
from PyQt5.QtWidgets import QApplication, QToolTip, QMainWindow, QMenuBar, QMenu, QAction, QDockWidget, QTextEdit, QWidget, QHBoxLayout, QVBoxLayout, QDialog, QLabel, QLineEdit, QDialogButtonBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPainter, QMouseEvent
from PyQt5.QtChart import QChart, QChartView


# class ChartView(QChartView):
#     def __init__(self, chart, parent=None):
#         super().__init__(chart, parent)
#         self.setMouseTracking(True)

#     def mouseMoveEvent(self, event: QMouseEvent):
#         pos = event.pos()
#         point = self.chart().mapToValue(pos)
#         x = point.x()
#         y = point.y()
#         if self.chart().series():
#             series = self.chart().series()[0]
#             for i in range(series.count()):
#                 if series.at(i).x() == x and series.at(i).y() == y:
#                     QToolTip.showText(event.globalPos(), f"Value: {y}")


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

    def show_login_dialog(self):
        dialog = LoginDialog()
        if dialog.exec_() == QDialog.Accepted:
            dialog.get_login()
            dialog.get_password()
            #self.open_new_window(login, password)
            dialog.verify()
    

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



import sqlite3
import hashlib
import os

# def verify_password(stored_password, provided_password, salt):
#     print(f'stored password {stored_password}, provided password {provided_password}, salt {salt}')
#     hashed_provided_password = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt.encode('utf-8'), 100000)
#     print(hashed_provided_password.hex(), stored_password)
#     return stored_password == hashed_provided_password.hex()

from passlib.hash import pbkdf2_sha256

import hashlib

def verify_password(stored_password, provided_password, salt):
    print(salt)
    password = provided_password.encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    # Hash the provided password with the given salt
    hashed_provided_password = pbkdf2_sha256.hash(password, salt=salt_bytes, rounds=100000)
    print(hashed_provided_password, stored_password)
    return stored_password == hashed_provided_password


def verify_login(username, password):
    conn = sqlite3.connect('src/database/users.db')
    cursor = conn.cursor()

    query = "SELECT password, salt FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    conn.close()

    if result:
        stored_password, salt = result
        return verify_password(stored_password, password, salt)

    return False


def print_users_table():
    conn = sqlite3.connect('src/database/users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()


username = "user1"
password = "password1"

login_result = verify_login(username, password)
print(login_result)
if login_result:
    print("Login successful")
else:
    print("Invalid username or password")

