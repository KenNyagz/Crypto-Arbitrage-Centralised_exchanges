from binance import Client
from Binance.tokens import get_tokens as binance_tickers
from Huobi.get_tickers import get_tickers as huobi_tickers


with open("Binance/api_secret", 'r') as f:
    binance_secret = f.read()

binance_tickers = binance_tickers(binance_secret)
huobi_tickers = huobi_tickers()

common_tickers = {}
for i in huobi_tickers:
    if i in binance_tickers:
        common_tickers.update({i: huobi_tickers[i]})

for i in common_tickers:
    print(i) # ~320
