import requests
import json


def get_tickers():
    prices_url = 'https://open-api.bingx.com/open-api/spot/v1/ticker/price'
    headers = {
        'Cookie': '__cf_bm=.9x3muHMteED9dZdnwt_n6i4WVDV5mRIyM6_gqwfTk8-1719675361-1.0.1.1-LtiHZ2uHVw611b2UlhQDH_qL8CSz9ZEpH2MoxqMM6MWnH9td1VWwXUdmevtCAeAQ_BAbDsVog31Vld3Gc7dZPA',
        #'Host': 'PC',
        'User-Agent': 'Python',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive'
    }
               
    resp = requests.get(prices_url, headers=headers).json()
    print(resp)
    pairs = resp['data']
    pairs_prices = {}
    for i in pairs:
        pair = i['symbol']
        price = i['trades']['price']
        pairs_prices.update({pair.upper(): price}) #Uppercase for uniformity

    for pair in pairs_prices:
        print(pair + " : " + str(pairs_prices[pair]))

    return pairs_prices

if __name__ == "__main__":
    get_tickers()
