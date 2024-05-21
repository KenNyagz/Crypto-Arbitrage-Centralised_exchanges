from binance import Client


def get_tokens(binance_secret=None):
    if binance_secret is None:
        with open("api_secret", 'r') as f:
            secret = f.read()
    else:
        secret = binance_secret

    pub = "xab1YQKg42rWQviBVcViQinX6fkYd7hVM6hndxUsWT4Q3xRXP0XeEhmdJnGVMbrV"
    client = Client(pub, secret)

    tickers = client.get_all_tickers()
    #for ticker in tickers:
    #    print(ticker)
    pairs_list = {}

    for i in tickers:
        for key in i:
            pair = i['symbol']
            price = i['price']
            pairs_list.update({pair: price})

    #for pair in pairs_list:
    #    print(pair,':', pairs_list[pair])
    return pairs_list


if __name__ == "__main__":
    get_tokens()
