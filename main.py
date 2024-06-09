import ccxt
from connectivity.check_status import check_connection_and_api_status
from arbitrage.fetch_data import fetch_tickers
from arbitrage.calculate_arbitrage import get_arbtg
from visualization.visualize import plot_arbitrage_opportunities

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

# API URLs to check
api_urls = [
    'https://api.binance.com',
    'https://api.huobi.pro',
    'https://www.okx.com',
    'https://api.gateio.ws'
]

# Ensure there is an internet connection and check API statuses
check_connection_and_api_status(api_urls)

# Initialize CCXT exchanges
binance = ccxt.binance()
huobi = ccxt.huobi()
okx = ccxt.okx()
gateio = ccxt.gateio()

# Fetch ticker data
binance_tickers = fetch_tickers(binance)
huobi_tickers = fetch_tickers(huobi)
okx_tickers = fetch_tickers(okx)
gateio_tickers = fetch_tickers(gateio)

# Calculate arbitrage opportunities
okx_binance_arbitrage = get_arbtg('okx', 'binance', okx_tickers, binance_tickers)
huobi_binance_arbitrage = get_arbtg('huobi', 'binance', huobi_tickers, binance_tickers)
okx_huobi_arbitrage = get_arbtg('okx', 'huobi', okx_tickers, huobi_tickers)

# Plot arbitrage opportunities
print("\nOkX and Binance Arbitrage Opportunities:")
plot_arbitrage_opportunities(okx_binance_arbitrage)

print("\nHuobi and Binance Arbitrage Opportunities:")
plot_arbitrage_opportunities(huobi_binance_arbitrage)

print("\nOkX and Huobi Arbitrage Opportunities:")
plot_arbitrage_opportunities(okx_huobi_arbitrage)
