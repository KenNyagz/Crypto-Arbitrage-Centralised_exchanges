import ccxt
import logging
import requests
from dotenv import load_dotenv

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
    def __init__(self, exchanges, symbols, public_api_urls):
        self.exchanges = exchanges
        self.symbols = symbols
        self.public_api_urls = public_api_urls

    def fetch_ccxt_data(self, exchange_name):
        try:
            exchange_class = getattr(ccxt, exchange_name)
        except AttributeError:
            logger.error(f"Exchange {exchange_name} is not supported by CCXT.")
            return {}

        exchange = exchange_class()
        data = {}
        for symbol in self.symbols:
            try:
                ticker = exchange.fetch_ticker(symbol)
                if 'last' in ticker:
                    data[symbol] = {'last': ticker['last']}
                else:
                    logger.warning(f"'last' price not found for {symbol} on {exchange_name}.")
            except Exception as e:
                logger.error(f"Error fetching data from {exchange_name} for {symbol}: {e}")
        return data


    def fetch_api_key_data(self, exchange_name):
        api_info = api_keys.get(exchange_name)
        if not api_info:
            logger.error(f"No API key/secret found for {exchange_name}.")
            return {}

        exchange_class = getattr(ccxt, exchange_name)
        exchange = exchange_class({'apiKey': api_info['api_key'], 'secret': api_info['secret']})
        data = {}
        for symbol in self.symbols:
            try:
                ticker = exchange.fetch_ticker(symbol)
                if 'last' in ticker:
                    data[symbol] = {'last': ticker['last']}
                else:
                    logger.warning(f"'last' price not found for {symbol} on {exchange_name}.")
            except Exception as e:
                logger.error(f"Error fetching data from {exchange_name} with API key for {symbol}: {e}")
        return data

    def fetch_public_api_data(self, exchange_name, url):
        data = {}
        for symbol in self.symbols:
            try:
                response = requests.get(url, params={'symbol': symbol.replace('/', '')})
                ticker = response.json()
                if 'last' in ticker:
                    data[symbol] = {'last': ticker['last']}
                else:
                    logger.warning(f"'last' price not found for {symbol} on {exchange_name} public API.")
            except Exception as e:
                logger.error(f"Error fetching data from {exchange_name} public API for {symbol}: {e}")
        return data

    def fetch_data(self):
        all_data = {}
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
                # Log the fetched data for inspection
                logger.info(f"Fetched data from {exchange}: {data}")
                all_data[exchange] = data
            else:
                logger.warning(f"No data fetched from {exchange} using any method.")
        return all_data
