import requests


def get_tickers(okx_secret=None):
    url = 'https://api.bitget.com/api/spot/v1/market/tickers'
    response = requests.get(url)
    data = response.json()['data']

    pairs_prices = {}
    for i in data:
        pair = i['symbol']
        price = i['close']
        pairs_prices.update({pair: float(price)})

    #for pair in pairs_prices:
    #    print(pair, ':', pairs_prices[pair]) # visualisation len~=958
    return pairs_prices


if __name__ == "__main__":
    get_tickers()
