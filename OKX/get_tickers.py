import requests


def get_tickers(okx_secret=None):
    # if okx_secret == None:
        # with open('api_secret', 'r') as f:
           # secret = f.read()
    #else:
        #secret = okx_secret
    #public_key = '6114f3f9-1c11-47b4-ba6a-7bf5dca15972'    

    url = 'https://www.okx.com/api/v5/market/tickers?instType=SPOT'
    response = requests.get(url)
    data = response.json()

    pairs_prices = {}
    for i in data['data']:
        for key in i:
            pair = i['instId']
            pair = pair.replace('-', '') # remove dash separating coins in pair
            price = i['last']
            pairs_prices.update({pair: float(price)})

    #for pair in pairs_prices:
    #    print(pair, ':', pairs_prices[pair]) # visualisation
    return pairs_prices


if __name__ == "__main__":
    get_tickers()
