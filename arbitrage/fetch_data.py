import ccxt
import logging
import requests

class DataFetcher:
    def __init__(self, exchanges, symbols):
        self.exchanges = exchanges
        self.symbols = symbols
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('data_fetcher')
        self.api_urls = {
            'binance': 'https://api.binance.com/api/v3/ticker/price',
            'huobi': 'https://api.huobi.pro/market/detail/merged',
            'okex': 'https://www.okx.com/api/spot/v3/instruments/ticker',
            'gateio': 'https://api.gateio.ws/api/v4/spot/tickers',
            'coinbase_pro': 'https://api.pro.coinbase.com/products/{symbol}/ticker',
            'kraken': 'https://api.kraken.com/0/public/Ticker',
            'bitfinex': 'https://api.bitfinex.com/v1/pubticker/{symbol}',
            'bittrex': 'https://api.bittrex.com/v3/markets/{symbol}/ticker',
            'poloniex': 'https://api.poloniex.com/public?command=returnTicker',
            'kucoin': 'https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}-USDT'
            # Add more exchanges and their API URLs as needed
        }

    def fetch_data_from_ccxt(self, exchange_name, symbol):
        try:
            exchange_class = getattr(ccxt, exchange_name)
            exchange = exchange_class()
            tickers = exchange.fetch_tickers()
            return tickers.get(symbol)
        except ccxt.BaseError as e:
            self.logger.error(f"Error fetching data for {symbol} on {exchange_name}: {str(e)}")
        except AttributeError:
            self.logger.error(f"Exchange {exchange_name} not found in ccxt library.")
        except Exception as e:
            self.logger.error(f"General error fetching data for {symbol} on {exchange_name}: {str(e)}")
        return None

    def fetch_data_from_api_url(self, exchange_name, symbol):
        try:
            response = requests.get(self.api_urls[exchange_name])
            response.raise_for_status()
            data = response.json()

            # Ensure data is a dictionary
            if isinstance(data, list):
                data = {item['symbol']: item for item in data}

            return data.get(symbol)
        except requests.RequestException as e:
            self.logger.error(f"Error fetching data for {symbol} on {exchange_name} via API URL: {str(e)}")
        return None


    def fetch_data(self):
        data = {}
        for symbol in self.symbols:
            data[symbol] = {}
            for exchange_name in self.exchanges:
                if exchange_name in self.api_urls:
                    ticker_data = self.fetch_data_from_api_url(exchange_name, symbol)
                else:
                    ticker_data = self.fetch_data_from_ccxt(exchange_name, symbol)

                if ticker_data:
                    data[symbol][exchange_name] = ticker_data
                    self.logger.info(f"Fetched data for {symbol} on {exchange_name}: {ticker_data}")
        return data
