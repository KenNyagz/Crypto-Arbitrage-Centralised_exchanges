import requests


def get_tickers(binance_secret=None):
    if binance_secret == None:
        with open('api_secret', 'r') as f:
            secret = f.read()
    else:
        secret = binance_secret
    public_key = ''

    url = 'https://api.binance.com/api/v3/ticker/bookTicker'
    response = requests.get(url)
    data = response.json()

    pairs_prices = {}
    for i in data:
        pair = i['symbol']
        price = i['bidPrice']
        pairs_prices.update({pair: float(price)})

    #for pair in pairs_prices:
    #    print(pair, ':', pairs_prices[pair]) # visualisation
    return pairs_prices


if __name__ == "__main__":
    get_tickers()
