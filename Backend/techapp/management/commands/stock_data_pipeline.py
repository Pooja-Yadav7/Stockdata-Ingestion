import yfinance as yf
import pandas as pd
from datetime import datetime
import mysql.connector
import json
from django.db import connection

# Load database configuration from the json file
with open('../db_config.json', 'r') as f:
    db_config = json.load(f)

def create_database_and_table(db_config):
    connection = mysql.connector.connect(
        user=db_config['user'],
        password=db_config['password'],
        host=db_config['host']
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

def fetch_daily_stock_data(symbol):
    stock = yf.Ticker(symbol)
    df = stock.history(period='1mo')
    df.reset_index(inplace=True)
    df['Symbol'] = symbol
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    return df




def store_stock_data(df, db_config):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    for _, row in df.iterrows():
        add_stock = ("INSERT INTO daily_stock_data "
                     "(symbol, date, open, high, low, close, volume) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s) "
                     "ON DUPLICATE KEY UPDATE "
                     "open=%s, high=%s, low=%s, close=%s, volume=%s")
        stock_data = (
            row['Symbol'], row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume'],
            row['Open'], row['High'], row['Low'], row['Close'], row['Volume']
        )
        cursor.execute(add_stock, stock_data)
    
    connection.commit()
    cursor.close()
    connection.close()

def fetch_and_store_data(symbol, db_config):
    stock_data = fetch_daily_stock_data(symbol)
    store_stock_data(stock_data, db_config)

# Create database and table
create_database_and_table(db_config)

# Example usage
symbols = [ 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
    'META', 'NVDA', 'NFLX', 'ADBE', 'INTC',
    'PYPL', 'CSCO', 'PEP', 'AVGO', 'COST',
    'TM', 'NKE', 'V', 'MA', 'JPM']  # List of symbols to fetch and store
for symbol in symbols:
    fetch_and_store_data(symbol, db_config)

print("Stock data fetched and stored in MySQL database.")