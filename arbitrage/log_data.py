# log_data.py

import sqlite3
import threading
import logging

# Define ArbitrageOpportunity class
class ArbitrageOpportunity:
    def __init__(self, symbol, base_currency, quote_currency, source_exchange, target_exchange, source_price, target_price, source_fee, target_fee, volume, percentage):
        """
        Initialize ArbitrageOpportunity object with required attributes.
        """
        self.symbol = symbol
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.source_exchange = source_exchange
        self.target_exchange = target_exchange
        self.source_price = source_price
        self.target_price = target_price
        self.source_fee = source_fee
        self.target_fee = target_fee
        self.volume = volume
        self.percentage = percentage

    def __repr__(self):
        """
        Return a string representation of the ArbitrageOpportunity object.
        """
        return (f"ArbitrageOpportunity(symbol={self.symbol}, base_currency={self.base_currency}, "
                f"quote_currency={self.quote_currency}, source_exchange={self.source_exchange}, "
                f"target_exchange={self.target_exchange}, source_price={self.source_price}, "
                f"target_price={self.target_price}, source_fee={self.source_fee}, "
                f"target_fee={self.target_fee}, volume={self.volume}, percentage={self.percentage})")

class DatabaseLogger:
    def __init__(self, db_name):
        self.db_name = db_name
        self._local = threading.local()
        self._create_tables()  # Ensure tables are created on initialization

    def _get_connection(self):
        if not hasattr(self._local, "connection"):
            self._local.connection = sqlite3.connect(self.db_name)
        return self._local.connection

    def _get_cursor(self):
        if not hasattr(self._local, "cursor"):
            self._local.cursor = self._get_connection().cursor()
        return self._local.cursor

    def _commit(self):
        self._get_connection().commit()

    def _close(self):
        if hasattr(self._local, "cursor"):
            self._local.cursor.close()
            del self._local.cursor
        if hasattr(self._local, "connection"):
            self._local.connection.close()
            del self._local.connection

    def _create_tables(self):
        cursor = self._get_cursor()

        # Drop the balances table if it exists to ensure the correct schema
        cursor.execute('''DROP TABLE IF EXISTS balances''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS tickers (
                            id INTEGER PRIMARY KEY,
                            exchange TEXT,
                            symbol TEXT,
                            price_usd REAL,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS opportunities (
                            id INTEGER PRIMARY KEY,
                            symbol TEXT,
                            base_currency TEXT,
                            quote_currency TEXT,
                            source_exchange TEXT,
                            target_exchange TEXT,
                            source_price REAL,
                            target_price REAL,
                            source_fee REAL,
                            target_fee REAL,
                            volume REAL,
                            percentage REAL,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS outliers (
                            id INTEGER PRIMARY KEY,
                            symbol TEXT,
                            base_currency TEXT,
                            quote_currency TEXT,
                            source_exchange TEXT,
                            target_exchange TEXT,
                            source_price REAL,
                            target_price REAL,
                            percentage REAL,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS errors (
                            id INTEGER PRIMARY KEY,
                            message TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS balances (
                            id INTEGER PRIMARY KEY,
                            exchange TEXT,
                            currency TEXT,
                            free REAL,
                            locked REAL,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

        self._commit()
        
        

    def log_ticker(self, exchange, symbol, price_usd):
        """
        Log ticker data into the 'tickers' table in the database.

        Parameters:
        exchange (str): The exchange name.
        symbol (str): The trading symbol.
        price_usd (float): The price in USD.
        """
        cursor = self._get_cursor()
        try:
            cursor.execute('INSERT INTO tickers (exchange, symbol, price_usd) VALUES (?, ?, ?)', 
                           (exchange, symbol, price_usd))
            self._commit()
            logging.info(f"Ticker data logged successfully for {symbol} on {exchange}.")
        except Exception as e:
            logging.error(f"Error logging ticker data for {symbol} on {exchange}: {e}")

    def log_opportunity(self, opportunity):
        """
        Log arbitrage opportunity into the 'opportunities' table in the database.

        Parameters:
        opportunity (ArbitrageOpportunity): The arbitrage opportunity object.
        """
        cursor = self._get_cursor()
        try:
            cursor.execute('''INSERT INTO opportunities (symbol, base_currency, quote_currency, source_exchange, target_exchange, source_price, target_price, source_fee, target_fee, volume, percentage) 
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (opportunity.symbol, opportunity.base_currency, opportunity.quote_currency, 
                            opportunity.source_exchange, opportunity.target_exchange, opportunity.source_price, 
                            opportunity.target_price, opportunity.source_fee, opportunity.target_fee, 
                            opportunity.volume, opportunity.percentage))
            self._commit()
            logging.info("Opportunity logged successfully.")
        except Exception as e:
            logging.error(f"Error logging opportunity: {e}")

    def log_outlier(self, outlier):
        """
        Log outlier into the 'outliers' table in the database.

        Parameters:
        outlier (dict): The outlier data.
        """
        cursor = self._get_cursor()
        try:
            cursor.execute('''INSERT INTO outliers (symbol, base_currency, quote_currency, source_exchange, target_exchange, source_price, target_price, percentage) 
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (outlier['symbol'], outlier['base_currency'], outlier['quote_currency'], 
                            outlier['source_exchange'], outlier['target_exchange'], outlier['source_price'], 
                            outlier['target_price'], outlier['percentage']))
            self._commit()
            logging.info("Outlier logged successfully.")
        except Exception as e:
            logging.error(f"Error logging outlier: {e}")

    def log_error(self, message):
        """
        Log error message into the 'errors' table in the database.

        Parameters:
        message (str): The error message.
        """
        cursor = self._get_cursor()
        try:
            cursor.execute('INSERT INTO errors (message) VALUES (?)', (message,))
            self._commit()
            logging.error(f"Error logged: {message}")
        except Exception as e:
            logging.error(f"Error logging error message: {e}")

    def log_balance(self, exchange, currency, free, locked=0):
        """
        Log balances into the 'balances' table in the database.

        Parameters:
        exchange (str): The exchange name.
        balances (dict): A dictionary of balances with currency as key and balance details as value.
        """
        cursor = self._get_cursor()
        try:
            cursor.execute('INSERT INTO balances (exchange, currency, free, locked) VALUES (?, ?, ?, ?)', 
                           (exchange, currency, free, locked))
            self._commit()
            logging.info(f"Balance logged successfully for {currency} on {exchange}.")
        except Exception as e:
            logging.error(f"Error logging balance for {currency} on {exchange}: {e}")

    def close(self):
        """
        Close the cursor and connection for the current thread.
        """
        self._close()
