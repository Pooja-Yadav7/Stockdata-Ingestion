import yfinance as yf
import pandas as pd
import mysql.connector
from mysql.connector import Error
from django.core.management.base import BaseCommand


def create_database_and_table(user, password, host):
    try:
        connection = mysql.connector.connect(
            user=user,
            password=password,
            host=host
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS stock_data")
        cursor.execute("USE stock_data")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_stock_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                symbol VARCHAR(10),
                date DATE,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                volume INT,
                UNIQUE(symbol, date)
            )
        """)
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error creating database and table: {e}")

def fetch_daily_stock_data(symbol):
    stock = yf.Ticker(symbol)
    df = stock.history(period='1mo')
    df.reset_index(inplace=True)
    df['Symbol'] = symbol
    
    # Convert 'Date' to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'])
    
    # Format 'Date' column
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    return df

def store_stock_data(df, db_config):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        for _, row in df.iterrows():
            # Replace NaN with None for each column individually
            row_dict = row.where(pd.notnull(row), None)

            add_stock = ("INSERT INTO daily_stock_data "
                         "(symbol, date, open, high, low, close, volume) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s) "
                         "ON DUPLICATE KEY UPDATE "
                         "open=%s, high=%s, low=%s, close=%s, volume=%s")
            stock_data = (
                row_dict['Symbol'], row_dict['Date'], row_dict['Open'], row_dict['High'], row_dict['Low'], row_dict['Close'], row_dict['Volume'],
                row_dict['Open'], row_dict['High'], row_dict['Low'], row_dict['Close'], row_dict['Volume']
            )

            try:
                cursor.execute(add_stock, stock_data)
            except Error as e:
                print(f"Error inserting data into MySQL: {e}")

        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error connecting to MySQL: {e}")

def fetch_and_store_data(symbol, db_config):
    stock_data = fetch_daily_stock_data(symbol)
    store_stock_data(stock_data, db_config)

class Command(BaseCommand):
    help = 'Fetches and stores stock data'

    def handle(self, *args, **options):
        # Create database and table using the direct credentials
        create_database_and_table(db_config['user'], db_config['password'], db_config['host'])

        # Example usage
        symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
            'META', 'NVDA', 'NFLX', 'ADBE', 'INTC',
            'PYPL', 'PEP', 'AVGO', 'COST',
            'TM', 'NKE', 'V', 'MA']  # List of symbols to fetch and store
        
        for symbol in symbols:
            fetch_and_store_data(symbol, db_config)

        self.stdout.write(self.style.SUCCESS("Stock data fetched and stored in MySQL database."))