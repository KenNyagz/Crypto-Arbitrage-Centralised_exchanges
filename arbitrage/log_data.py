import sqlite3
import logging

class DataLogger:
    def __init__(self, db_name='arbitrage.db'):
        """
        Initialize the DataLogger with the path to the SQLite database.

        Parameters:
        db_name (str): Path to the SQLite database.
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._setup_database()

    def _setup_database(self):
        """
        Set up the SQLite database, create tables if they don't exist.
        """
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS exchanges (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tickers (
                    id INTEGER PRIMARY KEY,
                    exchange_id INTEGER,
                    ticker TEXT,
                    price REAL,
                    FOREIGN KEY(exchange_id) REFERENCES exchanges(id)
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS arbitrage_opportunities (
                    id INTEGER PRIMARY KEY,
                    buy_exchange_id INTEGER,
                    sell_exchange_id INTEGER,
                    ticker TEXT,
                    buy_price REAL,
                    sell_price REAL,
                    percentage_diff REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(buy_exchange_id) REFERENCES exchanges(id),
                    FOREIGN KEY(sell_exchange_id) REFERENCES exchanges(id)
                )
            ''')
            self.conn.commit()
            logging.info("Database setup completed.")
        except sqlite3.Error as e:
            logging.error(f"Error setting up database: {e}")

    def log_exchange(self, exchange_name):
        """
        Log an exchange to the SQLite database.

        Parameters:
        exchange_name (str): The name of the exchange.

        Returns:
        int: The ID of the logged exchange.
        """
        self.cursor.execute('INSERT INTO exchanges (name) VALUES (?) ON CONFLICT(name) DO NOTHING', (exchange_name,))
        self.conn.commit()
        self.cursor.execute('SELECT id FROM exchanges WHERE name = ?', (exchange_name,))
        return self.cursor.fetchone()[0]

    def log_ticker(self, exchange_id, ticker, price):
        """
        Log a ticker to the SQLite database.

        Parameters:
        exchange_id (int): The ID of the exchange.
        ticker (str): The ticker symbol.
        price (float): The price of the ticker.
        """
        self.cursor.execute('INSERT INTO tickers (exchange_id, ticker, price) VALUES (?, ?, ?)', (exchange_id, ticker, price))
        self.conn.commit()

    def log_arbitrage_opportunity(self, buy_exchange_id, sell_exchange_id, ticker, buy_price, sell_price, percentage_diff):
        """
        Log an arbitrage opportunity to the SQLite database.

        Parameters:
        buy_exchange_id (int): The ID of the exchange to buy from.
        sell_exchange_id (int): The ID of the exchange to sell to.
        ticker (str): The ticker symbol.
        buy_price (float): The buy price.
        sell_price (float): The sell price.
        percentage_diff (float): The percentage difference in price.
        """
        self.cursor.execute('''
            INSERT INTO arbitrage_opportunities (buy_exchange_id, sell_exchange_id, ticker, buy_price, sell_price, percentage_diff)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (buy_exchange_id, sell_exchange_id, ticker, buy_price, sell_price, percentage_diff))
        self.conn.commit()

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()
