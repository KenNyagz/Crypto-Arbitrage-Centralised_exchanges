import sqlite3

class DataLogger:
    def __init__(self, db_name='arbitrage.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    def log_exchange(self, exchange_name):
        self.cursor.execute('INSERT INTO exchanges (name) VALUES (?)', (exchange_name,))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def log_ticker(self, exchange_id, ticker, price):
        self.cursor.execute('INSERT INTO tickers (exchange_id, ticker, price) VALUES (?, ?, ?)', (exchange_id, ticker, price))
        self.conn.commit()
    
    def log_arbitrage_opportunity(self, buy_exchange_id, sell_exchange_id, ticker, buy_price, sell_price, percentage_diff):
        self.cursor.execute('''
        INSERT INTO arbitrage_opportunities (buy_exchange_id, sell_exchange_id, ticker, buy_price, sell_price, percentage_diff)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (buy_exchange_id, sell_exchange_id, ticker, buy_price, sell_price, percentage_diff))
        self.conn.commit()
    
    def close(self):
        self.conn.close()
