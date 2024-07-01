#!/usr/bin/python3
from Binance.get_tickers import get_tickers as binance_tickers_
from Huobi.get_tickers import get_tickers as huobi_tickers_
from OKX.get_tickers import get_tickers as okx_tickers_
from GateIO.get_tickers import get_tickers as gateio_tickers_
from Bybit.get_tickers import get_tickers as bybit_tickers_
#from BingX.get_tickers import get_tickers as bingx_tickers_
from Bitget.get_tickers import get_tickers as bitget_tickers_
from Bitrue.get_tickers import get_tickers as bitrue_tickers_
from Kraken.get_tickers import get_tickers as kraken_tickers_
from KuCoin.get_tickers import get_tickers as kucoin_tickers_
from Mexc.get_tickers import get_tickers as mexc_tickers_
from Poloniex.get_tickers import get_tickers as poloniex_tickers_
from XT.get_tickers import get_tickers as xt_tickers_

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
okx_tickers = okx_tickers_(okx_secret)
gateio_tickers = gateio_tickers_("test") #
bybit_tickers = bybit_tickers_('tst')
#bingx_tickers = bingx_tickers_()
bitget_tickers = bitget_tickers_()
bitrue_tickers = bitrue_tickers_()
kraken_tickers = kraken_tickers_()
kucoin_tickers = kucoin_tickers_()
mexc_tickers = mexc_tickers_()
poloniex_tickers = poloniex_tickers_()
xt_tickers = xt_tickers_()


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

    if result.count('\n') <= 2:
        result += '  --  No arbitrage above 3% --'
    return result


def display_arbitrage_opportunities(exchange1, exchange2, exchange1_tickers, exchange2_tickers):
    '''Displays percentage price diffs btn two exchanges'''
    print('\n', exchange1,'and', exchange2, ' \n ', get_arbtg(exchange1, exchange2, exchange1_tickers, exchange2_tickers))



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
'--'
print('\n OKX and mexc\n', get_arbtg('okx', 'mexc', okx_tickers, mexc_tickers))
print('\n Poloniex and XT\n', get_arbtg('poloniex', 'xt', poloniex_tickers, xt_tickers))
print('\n OKX and Kucoin\n', get_arbtg('okx', 'kucoin', okx_tickers, kucoin_tickers))
print('\n Binance and Bitget\n', get_arbtg('binance', 'bitget', binance_tickers, bitget_tickers))
print('\n Kraken and Kucoin\n', get_arbtg('kraken', 'kucoin', kraken_tickers, kucoin_tickers))
print('\n Poloniex and OKX\n', get_arbtg('poloniex', 'okx', poloniex_tickers, okx_tickers))
print('\n Poloniex and Mexc\n', get_arbtg('poloniex', 'mexc', poloniex_tickers, mexc_tickers))
print('\n XT and GateIO\n', get_arbtg('XT', 'gateio', xt_tickers, gateio_tickers))
print('\n XT and Bitget\n', get_arbtg('XT', 'bitget', xt_tickers, bitget_tickers))
