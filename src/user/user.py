from passlib.hash import pbkdf2_sha256
import hashlib
import sqlite3


class User:
    def __init__(self, username, password, balance=None):
        self.username = username
        #self.password = self.set_password(password)
        self.balance = self.load_balance()
        self.wallet_id = None  # Will be set after creating the wallet



    def set_password(self, password):
        salt = hashlib.sha256().hexdigest()
        hashed_password = pbkdf2_sha256.hash(password, salt=salt, rounds=100000)
        return hashed_password

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)
    
    def load_balance(self):
        conn = sqlite3.connect('src/database/users.db')
        cursor = conn.cursor()

        query = "SELECT balance FROM users WHERE username = ?" 
        cursor.execute(query, (self.username,))
        result = cursor.fetchone()
        conn.close()
        return  result[0]
       
  

    def create_wallet(self):
        conn = sqlite3.connect('src/database/users.db')
        cursor = conn.cursor()

        # Insert wallet entry and get the assigned wallet ID
        cursor.execute("INSERT INTO wallets DEFAULT VALUES")
        self.wallet_id = cursor.lastrowid

        conn.commit()
        conn.close()

    def add_to_wallet(self, stock_name, quantity):
        if self.wallet_id is None:
            self.create_wallet()

        conn = sqlite3.connect('src/database/users.db')
        cursor = conn.cursor()

        # Check if the stock already exists in the wallet
        cursor.execute("SELECT quantity FROM purchases WHERE wallet_id = ? AND stock_name = ?", (self.wallet_id, stock_name))
        result = cursor.fetchone()

        if result:
            # Stock already exists, update the quantity
            current_quantity = result[0]
            new_quantity = current_quantity + quantity
            cursor.execute("UPDATE purchases SET quantity = ? WHERE wallet_id = ? AND stock_name = ?",
                           (new_quantity, self.wallet_id, stock_name))
        else:
            # Stock doesn't exist, insert a new record
            cursor.execute("INSERT INTO purchases (wallet_id, stock_name, quantity) VALUES (?, ?, ?)",
                           (self.wallet_id, stock_name, quantity))

        conn.commit()
        conn.close()

    def remove_from_wallet(self, stock_name, quantity):
        if self.wallet_id is None:
            return False

        conn = sqlite3.connect('src/database/users.db')
        cursor = conn.cursor()

        # Check if the stock exists in the wallet
        cursor.execute("SELECT quantity FROM purchases WHERE wallet_id = ? AND stock_name = ?", (self.wallet_id, stock_name))
        result = cursor.fetchone()

        if result:
            current_quantity = result[0]
            if current_quantity >= quantity:
                # Sufficient quantity exists, update the quantity
                new_quantity = current_quantity - quantity
                cursor.execute("UPDATE purchases SET quantity = ? WHERE wallet_id = ? AND stock_name = ?",
                               (new_quantity, self.wallet_id, stock_name))
                conn.commit()
                conn.close()
                return True

        conn.close()
        return False