import requests


def get_tickers(okx_secret=None):
    url = 'https://openapi.bitrue.com/api/v1/ticker/24hr'
    headers = {
        'X-MBX-APIKEY':  '',# How API keys are passed to the API endpoint; Trade ones
    }
    response = requests.get(url)
    data = response.json()

    pairs_prices = {}
    for i in data:
        pair = i['symbol']
        price = i['lastPrice']
        pairs_prices.update({pair: float(price)})

    #for pair in pairs_prices:
    #    print(pair, ':', pairs_prices[pair]) # visualisation len~=1571
    return pairs_prices


if __name__ == "__main__":
    get_tickers()
