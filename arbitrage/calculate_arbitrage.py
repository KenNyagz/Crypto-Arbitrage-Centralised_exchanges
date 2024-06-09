def get_arbtg(exchange1_name, exchange2_name, exchange1_tickers, exchange2_tickers):
    """
    Identify common tickers between two exchanges and calculate the percentage differences.

    Args:
        exchange1_name (str): Name of the first exchange.
        exchange2_name (str): Name of the second exchange.
        exchange1_tickers (dict): Ticker data from the first exchange.
        exchange2_tickers (dict): Ticker data from the second exchange.

    Returns:
        dict: Arbitrage opportunities.
    """
    common_tickers = {}
    for ticker in exchange1_tickers:
        if ticker in exchange2_tickers:
            common_tickers[ticker] = exchange1_tickers[ticker]

    percentage_diffs = {}
    for ticker in common_tickers:
        if exchange1_tickers[ticker]['last'] > exchange2_tickers[ticker]['last']:
            difference = exchange1_tickers[ticker]['last'] - exchange2_tickers[ticker]['last']
            percentage_diff = difference / exchange1_tickers[ticker]['last'] * 100
            percentage_diffs[ticker] = percentage_diff
        elif exchange2_tickers[ticker]['last'] > exchange1_tickers[ticker]['last']:
            difference = exchange2_tickers[ticker]['last'] - exchange1_tickers[ticker]['last']
            percentage_diff = difference / exchange2_tickers[ticker]['last'] * 100
            percentage_diffs[ticker] = percentage_diff

    return percentage_diffs
