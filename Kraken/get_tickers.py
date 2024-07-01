import requests
import json


def get_tickers():
    url = "https://api.kraken.com/0/public/Ticker"

    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()['result']
    else:
        print("Error")

    pairs_prices = {}
    for i in data:
        for _ in data[i]:
            pair = i
            price = data[i]['c'][0]
            pairs_prices.update({pair.upper(): float(price)}) # Uppercase for uniformity

    #for pair in pairs_prices:
    #    print(pair + " : " + str(pairs_prices[pair])) #Viz *len~809

    return pairs_prices

if __name__ == "__main__":
    get_tickers()
