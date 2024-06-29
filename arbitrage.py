#!/usr/bin/python3
from Binance.get_tickers import get_tickers as binance_tickers_
from Huobi.get_tickers import get_tickers as huobi_tickers_
from OKX.get_tickers import get_tickers as okx_tickers
from GateIO.get_tickers import get_tickers as gateio_tickers
from Bybit.get_tickers import get_tickers as bybit_tickers
#from binance import Client

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
bybit_tickers = bybit_tickers('tst')


def get_arbtg(exchange1, exchange2, exchange1_tickers, exchange2_tickers):
    common_tickers = {}
    for ticker in exchange1_tickers:
        if ticker in exchange2_tickers:
            common_tickers[ticker] = exchange1_tickers[ticker]

    result = f"\nCommon tickers in {exchange1} and {exchange2} are: {len(common_tickers)}\n"
    #print(result)

    percentage_diffs = {f"percentage_to_{exchange1}": 0.0, f"percentage_to_{exchange2}": 0.0}
    for ticker in common_tickers:
        if exchange1_tickers[ticker] > exchange2_tickers[ticker]:
            difference = exchange1_tickers[ticker] - exchange2_tickers[ticker]

            try:
                percentage_diffs[f"percentage_to_{exchange1}"] = difference / exchange1_tickers[ticker] * 100
                percentage_diffs[f"percentage_to_{exchange2}"] = (difference / exchange2_tickers[ticker]) * 100
            except ZeroDivisionError as e:
                 #print(f"zeroDivERROR:{ticker} : {exchange1_tickers[ticker]} ~ {exchange2_tickers[ticker]}")
                 continue

            if percentage_diffs[f"percentage_to_{exchange1}"] > 3:
                #print(ticker, end=" : ")
                # #print(percentage_diffs[f"percentage_to_{exchange1}"], f"% favouring {exchange2}") ## Don't uncomment unless testing
                #print(percentage_diffs[f"percentage_to_{exchange2}"], f"% favouring {exchange1}")
                # #result += f"{ticker} : difference is {percentage_diffs[f'percentage_to_{exchange1}']}% favouring {exchange2}\n" ## Don't uncomment unless testing
                result += f"{ticker} : difference is {percentage_diffs[f'percentage_to_{exchange2}']}% favouring {exchange1}\n" # return value construct

        elif exchange2_tickers[ticker] > exchange1_tickers[ticker]:
            difference = exchange2_tickers[ticker] - exchange1_tickers[ticker]
            try:
                percentage_diffs[f"percentage_to_{exchange2}"] = difference / exchange2_tickers[ticker] * 100
                percentage_diffs[f"percentage_to_{exchange1}"] = (difference / exchange1_tickers[ticker]) * 100
            except ZeroDivisionError as e:
                 #print(f"zeroDivERROR:{ticker} : {exchange1_tickers[ticker]} ~ {exchange2_tickers[ticker]}")
                 continue

            if percentage_diffs[f"percentage_to_{exchange2}"] > 3:
                #print(ticker, end=" : ")
                # #print(percentage_diffs[f"percentage_to_{exchange2}"], f"% favouring {exchange1}") ## Don't uncomment unless testing
                #print(percentage_diffs[f"percentage_to_{exchange1}"], f"% favouring {exchange2}")
                # #result += f"{ticker} : difference is {percentage_diffs[f'percentage_to_{exchange2}']}% favouring {exchange1}\n" ## Don't uncomment unless testing
                result += f"{ticker} : difference is {percentage_diffs[f'percentage_to_{exchange1}']}% favouring {exchange2}\n" #Constructing return value

    return result

print('\n Binance and Bybit\n',get_arbtg('binance', 'bybit', binance_tickers, bybit_tickers))
print('\n Binance and Huobi\n', get_arbtg('binance', 'huobi', binance_tickers, huobi_tickers))
print('\n Binance and OKX\n', get_arbtg('binance', 'okx', binance_tickers, okx_tickers))
print('\n Binance and gateio\n',get_arbtg('binance', 'gateio', binance_tickers, gateio_tickers))
print('\n Bybit and Huobi\n', get_arbtg('bybit', 'huobi', bybit_tickers, huobi_tickers))
print('\n Bybit and OKX\n', get_arbtg('bybit', 'okx', bybit_tickers, okx_tickers,))
print('\n Bybit and Gateio\n',get_arbtg('bybit', 'gateio', bybit_tickers, gateio_tickers))
print('\n Huobi and OKX\n', get_arbtg('huobi', 'okx', huobi_tickers, okx_tickers))
print('\n Huobi and GateIO\n', get_arbtg('huobi', 'gateio', huobi_tickers, gateio_tickers))
print('\n OKX and GateIO\n', get_arbtg('okx', 'gateio', okx_tickers, gateio_tickers))