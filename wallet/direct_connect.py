# direct_connect.py

import base64
import logging
import requests
from requests.exceptions import RequestException
from dotenv import load_dotenv
import os
import hashlib
import hmac
import time

import urllib3

# Load environment variables from .env file
load_dotenv()

# Configure logging
logger = logging.getLogger('wallet')

class DirectConnector:
    def __init__(self):
        # Dictionary to hold direct connections for unsupported exchanges
        self.exchange_funcs = {
            'binance': self.connect_and_fetch_binance,
            'kraken': self.connect_and_fetch_kraken,
            'huobi': self.connect_and_fetch_huobi,
            'okx': self.connect_and_fetch_okx,
        }

    def connect_and_fetch_balance(self, exchange_name):
        """
        Establish direct API connection to the specified exchange and fetch balance.
        """
        api_key = os.getenv(f'{exchange_name.upper()}_API_KEY')
        secret = os.getenv(f'{exchange_name.upper()}_SECRET')

        if not api_key or not secret:
            logger.error(f"API keys not found for {exchange_name}.")
            return None
        
        try:
            fetch_balance_func = self.exchange_funcs.get(exchange_name)
            if fetch_balance_func:
                return fetch_balance_func(api_key, secret)
            else:
                logger.error(f"Direct connection not implemented for {exchange_name}.")
                return None
        except RequestException as e:
            logger.error(f"Failed to connect to {exchange_name}: {e}")
            return None

    def connect_and_fetch_binance(self, api_key, secret):
        """
        Establish direct API connection to Binance exchange and fetch balance.
        """
        try:
            base_url = 'https://api.binance.com'
            headers = {
                'X-MBX-APIKEY': api_key
            }
            # Test connectivity endpoint
            response = requests.get(f"{base_url}/api/v3/ping")
            response.raise_for_status()
            logger.info("Connected to Binance exchange.")

            # Fetch balance
            timestamp = int(time.time() * 1000)
            query_string = f"timestamp={timestamp}"
            signature = hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
            url = f"{base_url}/api/v3/account?{query_string}&signature={signature}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            balance_data = response.json()
            balances = {}
            for asset in balance_data['balances']:
                if float(asset['free']) > 0.0 or float(asset['locked']) > 0.0:
                    balances[asset['asset']] = {
                        'free': float(asset['free']),
                        'locked': float(asset['locked'])
                    }
            logger.info("Fetched Binance balance.")
            return balances
        except RequestException as e:
            logger.error(f"Failed to fetch Binance balance: {e}")
            return None

    def connect_and_fetch_kraken(self, api_key, secret):
        """
        Establish direct API connection to Kraken exchange and fetch balance.
        """
        try:
            base_url = 'https://api.kraken.com'
            url_path = '/0/private/Balance'
            nonce = str(int(time.time() * 1000))
            post_data = {'nonce': nonce}
            encoded_post_data = (nonce + urllib3.parse.urlencode(post_data)).encode()
            message = url_path.encode() + hashlib.sha256(encoded_post_data).digest()
            signature = hmac.new(base64.b64decode(secret), message, hashlib.sha512).digest()
            headers = {
                'API-Key': api_key,
                'API-Sign': base64.b64encode(signature).decode()
            }
            response = requests.post(f"{base_url}{url_path}", headers=headers, data=post_data)
            response.raise_for_status()
            balance_data = response.json()
            if balance_data['error']:
                logger.error(f"Kraken API error: {balance_data['error']}")
                return None
            balances = {k: float(v) for k, v in balance_data['result'].items() if float(v) > 0.0}
            logger.info("Fetched Kraken balance.")
            return balances
        except RequestException as e:
            logger.error(f"Failed to fetch Kraken balance: {e}")
            return None

    def connect_and_fetch_huobi(self, api_key, secret):
        """
        Establish direct API connection to Huobi exchange and fetch balance.
        """
        try:
            base_url = 'https://api.huobi.pro'
            url_path = '/v1/account/accounts'
            timestamp = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
            params = {
                'AccessKeyId': api_key,
                'SignatureMethod': 'HmacSHA256',
                'SignatureVersion': '2',
                'Timestamp': timestamp
            }
            params_str = '&'.join([f"{key}={requests.utils.quote(str(value), safe='')}" for key, value in sorted(params.items())])
            payload = '\n'.join(['GET', 'api.huobi.pro', url_path, params_str])
            signature = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).digest()
            params['Signature'] = base64.b64encode(signature).decode()
            response = requests.get(f"{base_url}{url_path}", params=params)
            response.raise_for_status()
            accounts_data = response.json()
            account_id = accounts_data['data'][0]['id']
            url_path = f'/v1/account/accounts/{account_id}/balance'
            response = requests.get(f"{base_url}{url_path}", params=params)
            response.raise_for_status()
            balance_data = response.json()
            balances = {}
            for item in balance_data['data']['list']:
                if float(item['balance']) > 0.0:
                    balances[item['currency']] = {
                        'type': item['type'],
                        'balance': float(item['balance'])
                    }
            logger.info("Fetched Huobi balance.")
            return balances
        except RequestException as e:
            logger.error(f"Failed to fetch Huobi balance: {e}")
            return None

    def connect_and_fetch_okx(self, api_key, secret):
        """
        Establish direct API connection to OKX exchange and fetch balance.
        """
        try:
            base_url = 'https://www.okx.com'
            url_path = '/api/v5/account/balance'
            timestamp = str(time.time())
            headers = {
                'OK-ACCESS-KEY': api_key,
                'OK-ACCESS-TIMESTAMP': timestamp,
                'OK-ACCESS-PASSPHRASE': os.getenv('OKX_PASSPHRASE'),
                'OK-ACCESS-SIGN': base64.b64encode(hmac.new(secret.encode(), (timestamp + 'GET' + url_path).encode(), hashlib.sha256).digest()).decode()
            }
            response = requests.get(f"{base_url}{url_path}", headers=headers)
            response.raise_for_status()
            balance_data = response.json()
            balances = {}
            for item in balance_data['data'][0]['details']:
                if float(item['availBal']) > 0.0 or float(item['frozenBal']) > 0.0:
                    balances[item['ccy']] = {
                        'available': float(item['availBal']),
                        'frozen': float(item['frozenBal'])
                    }
            logger.info("Fetched OKX balance.")
            return balances
        except RequestException as e:
            logger.error(f"Failed to fetch OKX balance: {e}")
            return None
