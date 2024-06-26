import ccxt
import logging
import requests
import os
from dotenv import load_dotenv
from .log_data import DatabaseLogger

# Load environment variables from .env file
load_dotenv()

# Set up logging
logger = logging.getLogger('fetch_data')
logger.setLevel(logging.INFO)

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class DataFetcher:
    def __init__(self, exchanges, symbols, public_api_urls, db_logger):
        # Initialize the DataFetcher with provided exchanges, symbols, public API URLs, and a database logger
        self.exchanges = exchanges
        self.symbols = symbols
        self.public_api_urls = public_api_urls
        self.db_logger = db_logger

    def validate_symbol_format(self, symbol):
        # Validate that the symbol format is correct (contains a single '/')
        return '/' in symbol and symbol.count('/') == 1

    def fetch_ccxt_data(self, exchange_name):
        try:
            # Try to get the exchange class from ccxt library
            exchange_class = getattr(ccxt, exchange_name)
        except AttributeError:
            # Log an error if the exchange is not supported by ccxt
            logger.error(f"Exchange {exchange_name} is not supported by CCXT.")
            return {}

        exchange = exchange_class()
        data = {}
        # Fetch ticker data for each symbol from the exchange
        for symbol in self.symbols:
            if not self.validate_symbol_format(symbol):
                logger.error(f"Invalid symbol format: {symbol}")
                continue
            try:
                ticker = exchange.fetch_ticker(symbol)
                if 'last' in ticker:
                    if symbol not in data:
                        data[symbol] = {}
                    data[symbol]['last'] = ticker['last']
                    self.db_logger.log_ticker(exchange_name, symbol, ticker['last'])
                else:
                    logger.warning(f"'last' price not found for {symbol} on {exchange_name}.")
            except Exception as e:
                logger.error(f"Error fetching data from {exchange_name} for {symbol}: {e}")
        return data

    def fetch_api_key_data(self, exchange_name):
        # Get API key and secret from environment variables
        api_key = os.getenv(f'{exchange_name.upper()}_API_KEY')
        secret = os.getenv(f'{exchange_name.upper()}_SECRET')
        
        if not api_key or not secret:
            # Log an error if no API key/secret is found
            logger.error(f"No API key/secret found for {exchange_name}.")
            return {}

        exchange_class = getattr(ccxt, exchange_name)
        exchange = exchange_class({'apiKey': api_key, 'secret': secret})
        data = {}
        # Fetch ticker data for each symbol using the API key
        for symbol in self.symbols:
            if not self.validate_symbol_format(symbol):
                logger.error(f"Invalid symbol format: {symbol}")
                continue
            try:
                ticker = exchange.fetch_ticker(symbol)
                if 'last' in ticker:
                    if symbol not in data:
                        data[symbol] = {}
                    data[symbol]['last'] = ticker['last']
                    self.db_logger.log_ticker(exchange_name, symbol, ticker['last'])
                else:
                    logger.warning(f"'last' price not found for {symbol} on {exchange_name}.")
            except Exception as e:
                logger.error(f"Error fetching data from {exchange_name} with API key for {symbol}: {e}")
        return data

    def fetch_public_api_data(self, exchange_name, url):
        data = {}
        # Fetch ticker data for each symbol using the public API URL
        for symbol in self.symbols:
            if not self.validate_symbol_format(symbol):
                logger.error(f"Invalid symbol format: {symbol}")
                continue
            try:
                response = requests.get(url, params={'symbol': symbol.replace('/', '')})
                ticker = response.json()
                if 'last' in ticker:
                    if symbol not in data:
                        data[symbol] = {}
                    data[symbol]['last'] = ticker['last']
                    self.db_logger.log_ticker(exchange_name, symbol, ticker['last'])
                else:
                    logger.warning(f"'last' price not found for {symbol} on {exchange_name} public API.")
            except Exception as e:
                logger.error(f"Error fetching data from {exchange_name} public API for {symbol}: {e}")
        return data

    def fetch_data(self):
        all_data = {}
        # Iterate over each exchange to fetch data using different methods
        for exchange in self.exchanges:
            logger.info(f"Fetching data from {exchange} using CCXT.")
            data = self.fetch_ccxt_data(exchange)
            if not data:
                logger.info(f"Fetching data from {exchange} using API keys.")
                data = self.fetch_api_key_data(exchange)
            if not data and exchange in self.public_api_urls:
                logger.info(f"Fetching data from {exchange} using public API URL.")
                data = self.fetch_public_api_data(exchange, self.public_api_urls[exchange])
            if data:
                logger.info(f"Fetched data from {exchange}: {data}")
                all_data[exchange] = data
            else:
                logger.warning(f"No data fetched from {exchange} using any method.")
        return all_data
