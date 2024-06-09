import plotly.graph_objects as go

def plot_arbitrage_opportunities(arbitrage_data):
    """
    Plot arbitrage opportunities.

    Args:
        arbitrage_data (dict): Arbitrage data to plot.
    """
    tickers = list(arbitrage_data.keys())
    values = list(arbitrage_data.values())

    fig = go.Figure(data=[go.Bar(x=tickers, y=values)])

    fig.update_layout(
        title='Arbitrage Opportunities',
        xaxis_title='Ticker',
        yaxis_title='Arbitrage Percentage'
    )

    fig.show()
