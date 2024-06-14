import matplotlib.pyplot as plt

def plot_arbitrage_opportunities(arbitrage_opportunities):
    """
    Plot arbitrage opportunities.

    Args:
        arbitrage_opportunities (dict): Arbitrage opportunities to plot.
    """
    tickers = list(arbitrage_opportunities.keys())
    percentage_diffs = [data['percentage_diff'] for data in arbitrage_opportunities.values()]

    plt.figure(figsize=(10, 6))
    plt.bar(tickers, percentage_diffs, color='blue')
    plt.xlabel('Tickers')
    plt.ylabel('Percentage Difference')
    plt.title('Arbitrage Opportunities')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
