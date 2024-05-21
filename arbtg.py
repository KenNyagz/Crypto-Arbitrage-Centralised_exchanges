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

print("Common tokens in binance and gateio are", len(common_tickers), "\n") # ~320
for i in common_tickers:
    if huobi_tickers[i] > binance_tickers[i]:
        difference = huobi_tickers[i] - binance_tickers[i]
        percentage_to_binance = difference / binance_tickers[i] * 100
        percentage_to_huobi = (difference / huobi_tickers[i]) * 100
        if percentage_to_huobi > 3:
            print(i, end=": ")
            print("difference is", percentage_to_huobi, "% favouring huobi")
    elif binance_tickers[i] > huobi_tickers[i]:
        difference = binance_tickers[i] - huobi_tickers[i]
        percentage_to_binance = difference / binance_tickers[i] * 100
        percentage_to_huobi = (difference / huobi_tickers[i]) * 100
        if percentage_to_binance > 3:
            print(i, end=": ")
            print("difference is", percentage_to_huobi, "% favouring binance")

