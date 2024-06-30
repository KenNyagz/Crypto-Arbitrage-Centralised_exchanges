import requests
import json


def get_tickers():
    url = "https://api.kucoin.com/api/v1/market/allTickers"

    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()['data']
    else:
        print("Error")

    pairs_prices = {}
    for i in data['ticker']:
        for key in i:
            pair = i['symbol'].replace('-', '')
            price = i['last']
            pairs_prices.update({pair.upper(): price}) #Uppercase for uniformity

    #for pair in pairs_prices:
    #    print(pair + " : " + str(pairs_prices[pair]))  # len~1281
    return pairs_prices

if __name__ == "__main__":
    get_tickers()
