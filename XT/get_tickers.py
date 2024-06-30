import requests
import json


def get_tickers():
    url = " https://sapi.xt.com/v4/public/ticker/price"

    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()['result']
    else:
        print("Error")

    pairs_prices = {}
    for i in data:
        for key in i:
            pair = i['s']
            price = i['p']
            pairs_prices.update({pair.upper(): price}) #Uppercase for uniformity

    for pair in pairs_prices:
        print(pair + " : " + str(pairs_prices[pair]))

    return pairs_prices

if __name__ == "__main__":
    get_tickers()
