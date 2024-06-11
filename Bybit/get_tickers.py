import requests


def get_tickers(okx_secret=None):
    if okx_secret == None:
        with open('api_secret', 'r') as f:
            secret = f.read()
    else:
        secret = okx_secret
    public_key = ''    

    url = 'https://api.bybit.com/v5/market/tickers?category=spot'
    response = requests.get(url)
    data = response.json()

    pairs_prices = {}
    for i in data['result']['list']:
        for key in i:
            pair = i['symbol']
            price = i['lastPrice']
            pairs_prices[pair] = float(price)

    #print(len(pairs_prices))
    #for pair in pairs_prices:
    #    print(pair, ':', pairs_prices[pair]) # visualisation
    return pairs_prices


if __name__ == "__main__":
    get_tickers()
