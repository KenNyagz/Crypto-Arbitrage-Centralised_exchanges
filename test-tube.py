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


