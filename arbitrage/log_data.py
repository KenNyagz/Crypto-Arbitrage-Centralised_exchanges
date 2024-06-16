import sqlite3

class DatabaseLogger:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS arbitrage_opportunities (
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
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS ticker_data (
                id INTEGER PRIMARY KEY,
                exchange_name TEXT,
                symbol TEXT,
                last REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')

    def log_opportunity(self, opportunity):
        with self.conn:
            self.conn.execute('''INSERT INTO arbitrage_opportunities (
                symbol, base_currency, quote_currency, source_exchange,
                target_exchange, source_price, target_price, source_fee,
                target_fee, volume, percentage
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                opportunity.symbol, opportunity.base_currency, opportunity.quote_currency,
                opportunity.source_exchange, opportunity.target_exchange, opportunity.source_price,
                opportunity.target_price, opportunity.source_fee, opportunity.target_fee,
                opportunity.volume, opportunity.percentage
            ))

    def log_ticker(self, exchange_name, symbol, last):
        with self.conn:
            self.conn.execute('''INSERT INTO ticker_data (
                exchange_name, symbol, last
            ) VALUES (?, ?, ?)''', (
                exchange_name, symbol, last
            ))

    def warning(self, message):
        print(f"WARNING: {message}")

class ArbitrageOpportunity:
    def __init__(self, symbol, base_currency, quote_currency, source_exchange,
                 target_exchange, source_price, target_price, source_fee, target_fee, volume, percentage):
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
