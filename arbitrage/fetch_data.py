import ccxt
import logging
from arbitrage.log_data import DataLogger

class DataFetcher:
    def __init__(self, exchange_name, api_key, api_secret):
        """
        Initialize the DataFetcher with exchange credentials.

        Parameters:
        exchange_name (str): The name of the exchange.
        api_key (str): The API key for the exchange.
        api_secret (str): The API secret for the exchange.
        """
        self.exchange_name = exchange_name
        self.api_key = api_key
        self.api_secret = api_secret
        self.exchange = getattr(ccxt, exchange_name)({
            'apiKey': api_key,
            'secret': api_secret
        })
        self.data_logger = DataLogger()

    def fetch_data(self):
        """
        Fetch ticker data from the exchange and log it.

        Returns:
        dict: A dictionary of ticker data.
        """
        tickers = self.exchange.fetch_tickers()
        exchange_id = self.data_logger.log_exchange(self.exchange_name)
        for ticker, data in tickers.items():
            self.data_logger.log_ticker(exchange_id, ticker, data['last'])
        return tickers

    def close(self):
        """
        Close the data logger.
        """
        self.data_logger.close()
