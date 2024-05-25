from binance import Client
from Binance.get_tickers import get_tickers as binance_tickers_
from Huobi.get_tickers import get_tickers as huobi_tickers_
from OKX.get_tickers import get_tickers as okx_tickers
from GateIO.get_tickers import get_tickers as gateio_tickers

def get_secret(file_name):
    if not isinstance(file_name, str):
        raise TypeError("file_name must be a string")
    with open(file_name, 'r') as f:
        exchange_secret = f.read()
    return exchange_secret

# getting the secret keys
binance_secret = get_secret("Binance/api_secret")
okx_secret = get_secret("OKX/api_secret")

# Getting all ticker symbols and their prices from exchanges
binance_tickers = binance_tickers_(binance_secret)
huobi_tickers = huobi_tickers_() #
okx_tickers = okx_tickers(okx_secret)
gateio_tickers = gateio_tickers("test") #


def get_arbtg(exchange1, exchange2, exchange1_tickers, exchange2_tickers):
    common_tickers = {}
    for i in exchange1_tickers:
        if i in exchange2_tickers:
            common_tickers.update({i: exchange1_tickers[i]})

    print(f"\nCommon tickers in {exchange1} and {exchange2} are", len(common_tickers), "\n")

    percentage_diffs = {f"percentage_to_{exchange1}": 0.0, f"percentage_to_{exchange1}": 0.0}
    for i in common_tickers:
        if exchange1_tickers[i] > exchange2_tickers[i]:
            difference = exchange1_tickers[i] - exchange2_tickers[i]
            print(exchange1_tickers[i], exchange2_tickers[i], difference)
            break
            difference = exchange1_tickers[i] - exchange2_tickers[i]

            try:
                percentage_diffs[f"percentage_to_{exchange1}"] = difference / exchange2_tickers[i] * 100
                percentage_diffs[f"percentage_to_{exchange2}"] = (difference / exchange1_tickers[i]) * 100
            except ZeroDivisionError as e:
                 print(f"ERROR: {exchange1_tickers[i]} - {exchange2_tickers[i]}")

            if percentage_diffs[f"percentage_to_{exchange1}"] > 3:
                print(i, end=": ")
                print("difference is", percentage_diffs[f"percentage_to_{exchange1}"], f"% favouring {exchange1}")

        elif exchange2_tickers[i] > exchange1_tickers[i]:
            difference = exchange2_tickers[i] - exchange2_tickers[i]
            try:
                percentage_diffs[f"percentage_to_{exchange2}"] = difference / exchange2_tickers[i] * 100
                percentage_diffs[f"percentageto_{exchange1}"] = (difference / exchange1_tickers[i]) * 100
            except ZeroDivisionError as e:
                 print(f"ERROR: price1:{exchange1_tickers[i]} - price2:{exchange2_tickers[i]}")

            if percentage_diffs[f"percentage_to_{exchange2}"] > 3:
                print(i, end=": ")
                print(f" {exchange1_tickers[i]} <-> {exchange2}")
                print("difference is", percentage_diffs[f"percentage_to_{exchange2}"], f"% favouring {exchange2}")


#print('\n OkX and Binance\n', get_arbtg('okx', 'binance', okx_tickers, binance_tickers))
print('\n Huobi and Binance\n', get_arbtg('huobi', 'binance', huobi_tickers, binance_tickers))
#print('\n OkX and Huobi\n', get_arbtg('okx', 'huobi', okx_tickers, huobi_tickers))
#get_arbtg('binance', 'gateio', binance_tickers, gateio_tickers)

