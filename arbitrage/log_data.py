import sqlite3
import logging

# Define the data structure for arbitrage opportunities
class ArbitrageOpportunity:
    def __init__(self, symbol, base_currency, quote_currency, source_exchange, target_exchange, source_price, target_price, source_fee, target_fee, volume, percentage):
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

# Class to handle database operations
class DatabaseLogger:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        # Create tables for storing ticker data and arbitrage opportunities
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tickers (
                                id INTEGER PRIMARY KEY,
                                exchange TEXT,
                                symbol TEXT,
                                price_usd REAL,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS opportunities (
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

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS errors (
                                id INTEGER PRIMARY KEY,
                                message TEXT,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

        self.connection.commit()

    def log_ticker(self, exchange, symbol, price_usd):
        # Log ticker data into the database
        self.cursor.execute('INSERT INTO tickers (exchange, symbol, price_usd) VALUES (?, ?, ?)', (exchange, symbol, price_usd))
        self.connection.commit()

    def log_opportunity(self, opportunity):
        # Log arbitrage opportunities into the database
        try:
            self.cursor.execute('''INSERT INTO opportunities (symbol, base_currency, quote_currency, source_exchange, target_exchange, source_price, target_price, source_fee, target_fee, volume, percentage) 
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                (opportunity.symbol, opportunity.base_currency, opportunity.quote_currency, opportunity.source_exchange, opportunity.target_exchange, opportunity.source_price, opportunity.target_price, opportunity.source_fee, opportunity.target_fee, opportunity.volume, opportunity.percentage))
            self.connection.commit()
            logging.info("Opportunity logged successfully.")
        except Exception as e:
            logging.error(f"Error logging opportunity: {e}")

    def log_error(self, message):
        # Log errors into the database
        self.cursor.execute('INSERT INTO errors (message) VALUES (?)', (message,))
        self.connection.commit()

    def close(self):
        self.connection.close()
