from stocks_in_time import get_stock_information
from datetime import date

today = date.today().strftime("%m/%d/%y")
print("Today's date:", today)
dict = {"AMD": "AMD",  "Intel":"INTC", "Nvidia":"NVDA"}


# for i in dict.values():
#    get_stock_information()
# # TODO Add here methods for pd data taken from api, then to create charts and display it in the app