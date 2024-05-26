with open("Binance/api_secret", 'r') as f:
    binance_secret = f.read()
with open("OKX/api_secret", 'r') as f:
    okx_secret = f.read()


## Huobi x Binance
common_tickers_BxH = {}
for i in huobi_tickers:
    if i in binance_tickers:
        common_tickers_BxH.update({i: huobi_tickers[i]})

print("\nCommon tokens in binance and huobi are", len(common_tickers_BxH), "\n")

for i in common_tickers_BxH:
    if huobi_tickers[i] > binance_tickers[i]:
        difference = huobi_tickers[i] - binance_tickers[i]
        percentage_to_binance = difference / binance_tickers[i] * 100
        percentage_to_huobi = (difference / huobi_tickers[i]) * 100
        if percentage_to_huobi > 3:
            print(i, end=": ")
#            print("difference is", percentage_to_huobi, "% favouring huobi")
    elif binance_tickers[i] > huobi_tickers[i]:
        difference = binance_tickers[i] - huobi_tickers[i]
        percentage_to_binance = difference / binance_tickers[i] * 100
        percentage_to_huobi = (difference / huobi_tickers[i]) * 100
        if percentage_to_binance > 3:
            print(i, end=": ")
#            print("difference is", percentage_to_binance, "% favouring binance")

'=========================================================================='

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

    percentage_diffs = {f"percentage_to_{exchange1}": 0.0, f"percentage_to_{exchange2}": 0.0}
    for ticker in common_tickers:
        if exchange1_tickers[ticker] > exchange2_tickers[ticker]:
            difference = exchange1_tickers[ticker] - exchange2_tickers[ticker]

            try:
                percentage_diffs[f"percentage_to_{exchange1}"] = difference / exchange1_tickers[ticker] * 100
                percentage_diffs[f"percentage_to_{exchange2}"] = (difference / exchange2_tickers[ticker]) * 100
            except ZeroDivisionError as e:
                 print(f"ERROR: {exchange1_tickers[ticker]} - {exchange2_tickers[ticker]}")
                 continue

            if percentage_diffs[f"percentage_to_{exchange1}"] > 3:
                print(ticker, end=": ")
                print(percentage_diffs[f"percentage_to_{exchange1}"], f"% favouring {exchange1}")
                #result += f"{ticker}: difference is {percentage_diffs[f'percentage_to_{exchange1}']}% favouring {exchange1}\n" # for contructing return value

        elif exchange2_tickers[ticker] > exchange1_tickers[ticker]:
            difference = exchange2_tickers[ticker] - exchange1_tickers[ticker]
            try:
                percentage_diffs[f"percentage_to_{exchange2}"] = difference / exchange2_tickers[ticker] * 100
                percentage_diffs[f"percentage_to_{exchange1}"] = (difference / exchange1_tickers[ticker]) * 100
            except ZeroDivisionError as e:
                 print(f"ERROR: price1:{exchange1_tickers[ticker]} - price2:{exchange2_tickers[ticker]}")
                 continue

            if percentage_diffs[f"percentage_to_{exchange2}"] > 3:
                print(ticker, end=": ")
                print(percentage_diffs[f"percentage_to_{exchange2}"], f"% favouring {exchange2}")
                #result += f"{ticker}: difference is {percentage_diffs[f'percentage_to_{exchange1}']}% favouring {exchange1}\n" #Constructing return value

    #return result

#print('\n OkX and Binance\n', get_arbtg('okx', 'binance', okx_tickers, binance_tickers))
#print('\n Huobi and Binance\n', get_arbtg('huobi', 'binance', huobi_tickers, binance_tickers))
#print('\n OkX and Huobi\n', get_arbtg('okx', 'huobi', okx_tickers, huobi_tickers))
print('\n binance and gateio\n',get_arbtg('binance', 'gateio', binance_tickers, gateio_tickers))
