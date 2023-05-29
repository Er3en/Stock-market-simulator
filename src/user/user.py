class User:
    def __init__(self, id, username, password, budget):
        self.budget = budget
        self.stock_wallet = {}

    def add_to_wallet(self, stock_name, quantity):
        if stock_name in self.stock_wallet:
            self.stock_wallet[stock_name] += quantity
        else:
            self.stock_wallet[stock_name] = quantity

    def remove_from_wallet(self, stock_name, quantity):
        if stock_name in self.stock_wallet and self.stock_wallet[stock_name] >= quantity:
            self.stock_wallet[stock_name] -= quantity
            return True
        else:
            return False
