import requests
import json


def get_tickers():
    url = "https://api.mexc.com/api/v3/ticker/price"
    headers = {
        'X-MEXC-APIKEY': '',
        'Content-Type':	'application/json'
    }

    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
    else:
        print("Error")

    pairs_prices = {}
    for i in data:
        for key in i:
            pair = i['symbol']
            price = i['price']
            pairs_prices.update({pair.upper(): price}) #Uppercase for uniformity

    #for pair in pairs_prices:
    #    print(pair + " : " + str(pairs_prices[pair]))  # len~2915

    return pairs_prices

if __name__ == "__main__":
    get_tickers()
