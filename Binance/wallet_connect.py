from binance.client import Client

with open('api_secret', 'r') as f: 
        exchange_secret = f.read()
        exchange_secret = exchange_secret.strip()
with open('api_key', 'r') as f:
	exchange_key = f.read()
	exchange_key = exchange_key.strip() # Clean new line character

client = Client(exchange_key, exchange_secret)

account_info = client.get_account()
balances = account_info['balances']
for balance in balances:
	if float(balance['free']) > 0:
 		print(f"{balance['asset']} : {balance['free']}")
#print(balances)
