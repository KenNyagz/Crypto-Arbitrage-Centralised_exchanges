import requests


def get_tickers(okx_secret=None):
    url = 'https://api.gateio.ws/api/v4/spot/tickers'
    response = requests.get(url)
    data = response.json()

    pairs_prices = {}
    for i in data:
        pair = i['currency_pair']
        pair = pair.replace('_', '') # remove dash separating coins in pair
        price = i['last']
        pairs_prices.update({pair: float(price)})

    #for pair in pairs_prices:
    #    print(pair, ':', pairs_prices[pair]) # visualisation
    return pairs_prices


if __name__ == "__main__":
    get_tickers()
