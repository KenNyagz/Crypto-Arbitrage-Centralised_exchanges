from binance import Client
from Binance.get_tickers import get_tickers as binance_tickers_
from Huobi.get_tickers import get_tickers as huobi_tickers_
from OKX.get_tickers import get_tickers as okx_tickers

def get_secret(file_name):
    if not isinstance(file_name, str):
        raise TypeError("file_name must be a string")
    with open(file_name, 'r') as f:
        exchange_secret = f.read()
    return exchange_secret

binance_secret = get_secret("Binance/api_secret")
okx_secret = get_secret("OKX/api_secret")
binance_tickers = binance_tickers_(binance_secret)
huobi_tickers = huobi_tickers_()
okx_tickers = okx_tickers(okx_secret)

def get_arbtg(exchange1, exchange2, exchange1_tickers, exchange2_tickers):
    common_tickers = {}
    for i in exchange1_tickers:
        if i in exchange2_tickers:
            common_tickers.update({i: exchange1_tickers[i]})

    print("\nCommon tokens in binance and okx are", len(common_tickers), "\n")
    percentage_diffs = {f"percentage_to_{exchange1}": 0.0, f"percentage_to_{exchange1}": 0.0}
    for i in common_tickers:
        if exchange1_tickers[i] > exchange2_tickers[i]:
            difference = exchange1_tickers[i] - exchange2_tickers[i]
            percentage_diffs[f"percentage_to_{exchange1}"] = difference / exchange2_tickers[i] * 100
            percentage_diffs[f"percentage_to_{exchange2}"] = (difference / exchange1_tickers[i]) * 100
            if percentage_diffs[f"percentage_to_{exchange1}"] > 3:
                print(i, end=": ")
                print("difference is", percentage_diffs[f"percentage_to_{exchange1}"], f"% favouring {exchange1}")
        elif exchange2_tickers[i] > exchange1_tickers[i]:
            difference = exchange2_tickers[i] - exchange2_tickers[i]
            percentage_diffs[f"percentage_to_{exchange2}"] = difference / exchange2_tickers[i] * 100
            percentage_diffs[f"percentageto_{exchange1}"] = (difference / exchange1_tickers[i]) * 100
            if percentage_diffs[f"percentage_to_{exchange2}"] > 3:
                print(i, end=": ")
                print("difference is", percentage_diffs[f"percentage_to_{exchange2}"], f"% favouring {exchange2}")

get_arbtg('okx', 'binance', okx_tickers, binance_tickers)
