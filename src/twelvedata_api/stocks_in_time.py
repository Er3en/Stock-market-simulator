import os
from twelvedata import TDClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

def calculate_days(start_date, end_date):
    date_format = "%m/%d/%Y"
    start_date_obj = datetime.strptime(start_date, date_format)
    end_date_obj = datetime.strptime(end_date, date_format)
    delta = end_date_obj - start_date_obj
    return delta.days


def get_stock_information(symbol=None, start_date=None, end_date=None):
    # Initialize client - apikey parameter is requiered
    td = TDClient(apikey=API_KEY)
    try:
        # Construct the necessary time series
        ts = td.time_series(
            symbol=symbol,
            interval="1day",
            outputsize=f"{calculate_days(start_date, end_date)}",
            type="stock",
            timezone="Europe/Warsaw",
            start_date=start_date,
            end_date=end_date
        )

        df = ts.as_pandas() 
    except Exception as e:
         print("An error occurred while retrieving the time series:", str(e))

    return df, symbol

