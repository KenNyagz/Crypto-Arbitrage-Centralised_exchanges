import ccxt

def fetch_tickers(exchange):
    """
    Fetch tickers from the exchange.

    Args:
        exchange (object): The exchange instance.

    Returns:
        dict: Tickers data.
    """
    return exchange.fetch_tickers()
