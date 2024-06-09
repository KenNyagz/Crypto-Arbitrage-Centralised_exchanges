import requests
from binance import Client
from Binance.get_tickers import get_tickers as binance_tickers_
from Huobi.get_tickers import get_tickers as huobi_tickers_
from OKX.get_tickers import get_tickers as okx_tickers
from GateIO.get_tickers import get_tickers as gateio_tickers

def get_secret(file_name):
    """
    Read the secret key from a file.

    Args:
        file_name (str): The name of the file containing the secret key.

    Returns:
        str: The secret key.

    Raises:
        TypeError: If file_name is not a string.
        FileNotFoundError: If the file does not exist.
    """
    if not isinstance(file_name, str):
        raise TypeError("file_name must be a string")
    with open(file_name, 'r') as f:
        exchange_secret = f.read().strip()
    return exchange_secret

def check_connection_and_api_status(api_urls):
    """
    Check if there is an active internet connection and if APIs are reachable.

    Args:
        api_urls (list): A list of API base URLs to check.

    Raises:
        ConnectionError: If there is no internet connection or if any API is not reachable.
    """
    # Check for internet connection
    try:
        requests.get('https://www.google.com/', timeout=5)
    except (requests.ConnectionError, requests.Timeout):
        raise ConnectionError("No internet connection available.")

    # Check API statuses
    for api_url in api_urls:
        try:
            response = requests.get(api_url, timeout=5)
            if response.status_code != 200:
                raise ConnectionError(f"API at {api_url} is not responding correctly.")
        except (requests.ConnectionError, requests.Timeout):
            raise ConnectionError(f"API at {api_url} is not reachable.")

# API URLs to check
api_urls = [
    'https://api.binance.com',
    'https://api.huobi.pro',
    'https://www.okx.com',
    'https://api.gateio.ws'
]

# Ensure there is an internet connection and check API statuses
check_connection_and_api_status(api_urls)

# Getting the secret keys
binance_secret = get_secret("Binance/api_secret")
okx_secret = get_secret("OKX/api_secret")

# Getting all ticker symbols and their prices from exchanges
binance_tickers = binance_tickers_(binance_secret)
huobi_tickers = huobi_tickers_()
okx_tickers = okx_tickers(okx_secret)
gateio_tickers = gateio_tickers("test")

def get_arbtg(exchange1, exchange2, exchange1_tickers, exchange2_tickers):
    """
    Identify common tickers between two exchanges and calculate the percentage differences.

    Args:
        exchange1 (str): Name of the first exchange.
        exchange2 (str): Name of the second exchange.
        exchange1_tickers (dict): Ticker data from the first exchange.
        exchange2_tickers (dict): Ticker data from the second exchange.

    Returns:
        str: Results of the arbitrage opportunities.
    """
    common_tickers = {}
    for ticker in exchange1_tickers:
        if ticker in exchange2_tickers:
            common_tickers[ticker] = exchange1_tickers[ticker]

    result = f"\nCommon tickers in {exchange1} and {exchange2} are: {len(common_tickers)}\n"
    print(result)

    percentage_diffs = {f"percentage_to_{exchange1}": [], f"percentage_to_{exchange2}": []}
    for ticker in common_tickers:
        if exchange1_tickers[ticker] > exchange2_tickers[ticker]:
            difference = exchange1_tickers[ticker] - exchange2_tickers[ticker]
            percentage_diff = difference / exchange1_tickers[ticker] * 100
            percentage_diffs[f"percentage_to_{exchange1}"].append((ticker, percentage_diff))
        elif exchange2_tickers[ticker] > exchange1_tickers[ticker]:
            difference = exchange2_tickers[ticker] - exchange1_tickers[ticker]
            percentage_diff = difference / exchange2_tickers[ticker] * 100
            percentage_diffs[f"percentage_to_{exchange2}"].append((ticker, percentage_diff))

    # Displaying the results
    for direction, percentages in percentage_diffs.items():
        print(f"{direction.capitalize()} Favouring Tickers:")
        for ticker, percentage_diff in percentages:
            print(f"{ticker}: {percentage_diff:.2f}%")

# Example usage
print('\n OkX and Binance\n', get_arbtg('okx', 'binance', okx_tickers, binance_tickers))
print('\n Huobi and Binance\n', get_arbtg('huobi', 'binance', huobi_tickers, binance_tickers))
print('\n OkX and Huobi\n', get_arbtg('okx', 'huobi', okx_tickers, huobi_tickers))
