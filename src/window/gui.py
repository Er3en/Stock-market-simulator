import datetime
from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QDockWidget, QWidget, QHBoxLayout, QVBoxLayout, QDialog, QLabel, QLineEdit, QDialogButtonBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton
from .login import verify_login
from ..twelvedata_api.stocks_in_time import get_stock_information, get_real_time_price
from ..user.user import *
from datetime import date, datetime, timedelta
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.figure import Figure
from matplotlib.widgets import Button


class ChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)


    def update_chart(self, df, symbol):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(df['close'])
        ax.set_title(f"{symbol}")
        ax.set_xlabel('Time')
        ax.set_ylabel('Price USD')
        self.canvas.draw_idle()


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
        return self.login_edit


    def get_password(self):
        self.password_edit = self.password_edit.text()


    def is_verified(self):
        return verify_login(self.login_edit, self.password_edit)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.time = None
        self.date_format = "%m/%d/%Y"
        self.date = date.today()
        self.date = self.date.strftime("%m/%d/%y")
        self.df, self.symbol = None, None
        self.user_logged = False
        self.user = None
        self.real_price_timer = QTimer()
        self.real_price = None
        self.balance_label = None
        self.stocks_label = None

        timer = QTimer(self)
        timer.timeout.connect(self.update_time_and_date)
        timer.start(300000)  

        self.init_apperance()
        self.create_menu()
        self.create_user_panel()


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
        if not self.user_logged:
            self.user_panel = QDockWidget("User Panel", self)
            self.user_panel.setFeatures(QDockWidget.NoDockWidgetFeatures)
            self.addDockWidget(Qt.LeftDockWidgetArea, self.user_panel)

            self.user_widget = QWidget()
            self.user_layout = QVBoxLayout(self.user_widget)
            self.user_label = QLabel("Welcome to the Stock Market App!")
            self.user_label.setStyleSheet("font-size: 18px;")  
            self.user_layout.addWidget(self.user_label)
        if self.user_logged and (self.balance_label is None and self.stocks_label is None):
            # Create QLabel widgets to display user balance and owned stocks
            self.balance_label = QLabel("Balance: $0.00")
            self.balance_label.setStyleSheet("font-size: 18px;")  
            self.stocks_label = QLabel("Owned Stocks: 0")
            self.stocks_label.setStyleSheet("font-size: 18px;")  
            # Add the QLabel widgets to the user layout
            self.user_layout.addWidget(self.balance_label)
            self.user_layout.addWidget(self.stocks_label)

        self.user_panel.setWidget(self.user_widget)



    def create_central_widget(self):
        self.setCentralWidget(None)  # Remove previous central widget
        if self.user_logged:
            self.create_chart_widget()
            self.create_button()


    def create_chart_widget(self):
        self.chart_widget = ChartWidget()
        if self.symbol is not None:
            self.chart_widget.update_chart(self.df, self.symbol)
            self.setCentralWidget(self.chart_widget)


    def logout(self):
        if self.user_logged:
            self.user_layout.removeWidget(self.user_label)
            self.user_label.deleteLater()
            self.user_label = QLabel("You have been logged out")
            self.user_label.setStyleSheet("font-size: 18px;")  
            self.user_layout.addWidget(self.user_label)
            self.user_logged = False
            self.setCentralWidget(None) 
            self.df, self.symbol = None, None
            self.user = None
            self.balance_label.deleteLater()
            self.stocks_label.deleteLater()
            self.balance_label = None
            self.stocks_label = None
            self.real_price_timer.stop()
            self.real_price_timer.timeout.disconnect()
            

    def show_login_dialog(self):
        dialog = LoginDialog()
        if dialog.exec_() == QDialog.Accepted:
            login = dialog.get_login()
            dialog.get_password()
            ver, self.user = dialog.is_verified()
            if ver:
                self.user_logged = True
                self.user_label.setText(f"Welcome, {login}!")  
                self.create_central_widget()
                self.create_user_panel()
                self.balance_label.setText(f"Balance: ${str( self.user.load_balance())}")


    def update_time_and_date(self):
        current_datetime = datetime.now()
        current_time = current_datetime.strftime("%H:%M:%S")
        current_date = current_datetime.strftime("%m/%d/%Y")  # Format the date as "%m/%d/%Y"
        self.time = current_time
        self.date = current_date


    def switch_to_previous_chart(self):
        if self.symbol is not None:
            self.chart_widget.update_chart(self.df_prev, self.symbol_prev)
            self.setCentralWidget(self.chart_widget)
            self.create_button()


    def update_price(self, symbol):
        if symbol:
            self.real_price = get_real_time_price(symbol)
            self.stock_price_label.setText("Stock Price: $" + str(self.real_price))


    def update_chart_data(self):
        text = self.text_input.text()
        if text:
            try: 
                end_date = datetime.strptime(self.date, "%m/%d/%y")
                end_date_str = end_date.strftime("%m/%d/%Y") 
                start_date = end_date - timedelta(days=30)  
                start_date_str = start_date.strftime("%m/%d/%Y")
                self.df, self.symbol = get_stock_information(symbol=f"{text}", 
                                                            start_date=start_date_str,
                                                            end_date=end_date_str)
            except Exception as e:
                self.user_label.setText(f"{str(e)}")  
            self.symbol = text
            try:
                self.create_chart_widget()
                self.create_button()

                if self.real_price_timer.isActive():
                    self.update_price(symbol=text)
                    self.real_price_timer.stop()
                    self.real_price_timer.timeout.disconnect()
                else:
                    self.update_price(symbol=text)

                # Start the timer with a new connection
                self.real_price_timer.timeout.connect(lambda: self.update_price(symbol=text))
                self.real_price_timer.start(30000)  # Start the timer with a timeout of 30s
            except Exception as e:
                self.user_label.setText(str(e))


    def create_button(self):
        button_widget = QWidget(self)
        button_layout = QVBoxLayout(button_widget)

        text_input = QLineEdit()
        text_input.setMaximumWidth(300)  # Set the maximum width of the text input box
        text_input.setAlignment(Qt.AlignCenter)  # Center-align the text input box
        text_input.setStyleSheet("font-size: 18px;")  # Set a larger font size for the text input box
        self.text_input = text_input
        button_layout.addWidget(text_input, alignment=Qt.AlignCenter)  # Align the text input box to the center

        other_button = QPushButton('Search and display', self)
        other_button.setMaximumWidth(200)  # Set the maximum width of the other button
        other_button.clicked.connect(self.update_chart_data)
        other_button.setStyleSheet("font-size: 20px;")  # Set a larger font size for the other button
        button_layout.addWidget(other_button, alignment=Qt.AlignCenter)  # Align the button to the center


        button_widget_2 = QWidget()
        button_layout_2 = QHBoxLayout(button_widget_2)

        buy_button = QPushButton('Buy', self)
        buy_button.setMaximumWidth(200)  # Set the maximum width of the buy button
        buy_button.clicked.connect(self.buy_stock)  # Connect the button to the buy_stock method
        buy_button.setStyleSheet("font-size: 20px;")  # Set a larger font size for the buy button
        button_layout_2.addWidget(buy_button, alignment=Qt.AlignCenter)  # Align the button to the center

        sell_button = QPushButton('Sell', self)
        sell_button.setMaximumWidth(200)  # Set the maximum width of the sell button
        sell_button.clicked.connect(self.sell_stock)  # Connect the button to the sell_stock method
        sell_button.setStyleSheet("font-size: 20px;")  # Set a larger font size for the sell button
        button_layout_2.addWidget(sell_button, alignment=Qt.AlignCenter)  # Align the button to the center

        button_layout.addStretch(1)  # Add stretch to the vertical layout to center-align the buttons
        button_layout.addWidget(button_widget_2, alignment=Qt.AlignCenter)  # Align the button widget to the center

    
        quantity_label = QLabel("Quantity:")
        quantity_label.setStyleSheet("font-size: 18px;")  # Set a larger font size for the quantity label
        quantity_input = QLineEdit()
        quantity_input.setMaximumWidth(300)  # Set the maximum width of the quantity input box
        quantity_input.setAlignment(Qt.AlignCenter)  # Center-align the quantity input box
        quantity_input.setStyleSheet("font-size: 18px;")  # Set a larger font size for the quantity input box
        self.quantity_input = quantity_input

        button_layout.addWidget(quantity_label, alignment=Qt.AlignRight)  # Align the quantity label to the right
        button_layout.addWidget(quantity_input, alignment=Qt.AlignRight)  # Align the quantity input to the right
        stock_price_label = QLabel("Stock Price: $0.00")  # Label to display the current stock price
        stock_price_label.setStyleSheet("font-size: 18px;")  # Set a larger font size for the stock price label
        self.stock_price_label = stock_price_label
        button_layout.addWidget(stock_price_label, alignment=Qt.AlignCenter)  # Align the stock price label to the center

        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.chart_widget)
        central_layout.addWidget(button_widget, alignment=Qt.AlignCenter)  # Align the button widget to the center

        self.setCentralWidget(central_widget)


    def buy_stock(self):
        quantity = self.quantity_input.text()
        if self.symbol and quantity is not None:
            stock = self.symbol
            ammount = int(quantity) * float(self.real_price)
            balance = self.user.load_balance() - ammount
            self.user.insert_new_balance(balance)
            self.balance_label.setText(f"Balance: {float(self.user.load_balance())}$")    
            #self.user.add_to_wallet(stock_name=stock,quantity=quantity)
  
        
    def sell_stock(self):
        quantity = self.quantity_input.text()
        if self.symbol and quantity is not None:
            stock = self.symbol
            ammount = int(quantity) * float(self.real_price)
            balance = self.user.load_balance() + ammount
            self.user.insert_new_balance(balance)
            self.balance_label.setText(f"Balance: {float(self.user.load_balance())}$")
            #self.user.remove_from_wallet()
      
 
