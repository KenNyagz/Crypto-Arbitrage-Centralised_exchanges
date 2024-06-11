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
    for ticker in exchange1_tickers:
        if ticker in exchange2_tickers:
            common_tickers[ticker] = exchange1_tickers[ticker]

    result = f"\nCommon tickers in {exchange1} and {exchange2} are: {len(common_tickers)}\n"
    print(result)

    percentage_diffs = {f"percentage_to_{exchange1}": [], f"percentage_to_{exchange2}": []}
    for ticker in common_tickers:
        if exchange1_tickers[ticker] > exchange2_tickers[ticker]:
            difference = exchange1_tickers[ticker] - exchange2_tickers[ticker]
            percentage_diff = difference / exchange1_tickers[ticker] * 100
            percentage_diffs[f"percentage_to_{exchange1}"].append((ticker, percentage_diff))

        elif exchange2_tickers[ticker] > exchange1_tickers[ticker]:
            difference = exchange2_tickers[ticker] - exchange1_tickers[ticker]
            percentage_diff = difference / exchange2_tickers[ticker] * 100
            percentage_diffs[f"percentage_to_{exchange2}"].append((ticker, percentage_diff))

    # Displaying the results
    for direction, percentages in percentage_diffs.items():
        print(f"\n{direction.capitalize()} Favouring Tickers:")
        for ticker, percentage_diff in percentages:
            print(f"{ticker}: {percentage_diff:.2f}%")

# Example usage remains the same
#print('\n OkX and Binance\n', get_arbtg('okx', 'binance', okx_tickers, binance_tickers))
#print('\n Huobi and Binance\n', get_arbtg('huobi', 'binance', huobi_tickers, binance_tickers))
print('\n OkX and Huobi\n', get_arbtg('okx', 'huobi', okx_tickers, huobi_tickers))
