from binance import Client

with open("api_secret", 'r') as f:
    secret = f.read()

pub = "xab1YQKg42rWQviBVcViQinX6fkYd7hVM6hndxUsWT4Q3xRXP0XeEhmdJnGVMbrV"
client = Client(pub, secret)

tickers = client.get_all_tickers()
#for ticker in tickers:
 #   print(ticker)
print(len(tickers))
