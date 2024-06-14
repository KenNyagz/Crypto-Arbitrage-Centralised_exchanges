import ccxt
import os

class Exchange:
    def __init__(self, exchange_name, api_key_file):
        self.exchange_name = exchange_name
        self.api_key_file = api_key_file
        self.exchange = self._initialize_exchange()
    
    def _initialize_exchange(self):
        with open(self.api_key_file, 'r') as f:
            api_key, api_secret = f.read().strip().split('\n')
        
        exchange_class = getattr(ccxt, self.exchange_name)
        exchange = exchange_class({
            'apiKey': api_key,
            'secret': api_secret
        })
        return exchange
    
    def fetch_tickers(self):
        try:
            tickers = self.exchange.fetch_tickers()
            return tickers
        except ccxt.NetworkError as e:
            print(f"Network error while fetching tickers from {self.exchange_name}: {e}")
            return {}
        except ccxt.ExchangeError as e:
            print(f"Exchange error while fetching tickers from {self.exchange_name}: {e}")
            return {}

class Binance(Exchange):
    def __init__(self):
        super().__init__('binance', 'keys/binance_key.txt')

class Huobi(Exchange):
    def __init__(self):
        super().__init__('huobi', 'keys/huobi_key.txt')

class OKX(Exchange):
    def __init__(self):
        super().__init__('okx', 'keys/okx_key.txt')

class Gateio(Exchange):
    def __init__(self):
        super().__init__('gateio', 'keys/gateio_key.txt')

class Coinbase(Exchange):
    def __init__(self):
        super().__init__('coinbase', 'keys/coinbase_key.txt')

class Kraken(Exchange):
    def __init__(self):
        super().__init__('kraken', 'keys/kraken_key.txt')

class Bitfinex(Exchange):
    def __init__(self):
        super().__init__('bitfinex', 'keys/bitfinex_key.txt')

class Bittrex(Exchange):
    def __init__(self):
        super().__init__('bittrex', 'keys/bittrex_key.txt')

class Poloniex(Exchange):
    def __init__(self):
        super().__init__('poloniex', 'keys/poloniex_key.txt')

class Kucoin(Exchange):
    def __init__(self):
        super().__init__('kucoin', 'keys/kucoin_key.txt')
