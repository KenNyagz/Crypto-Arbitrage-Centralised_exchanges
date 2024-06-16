import logging
from time import sleep
from arbitrage.calculate_arbitrage import ArbitrageCalculator
from arbitrage.fetch_data import DataFetcher
from arbitrage.log_data import ArbitrageOpportunity, DatabaseLogger
from visualization.visualize import visualize_opportunities

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main')

def dot_animation(seconds):
    """
    Displays a dot animation for the specified number of seconds.
    """
    for _ in range(seconds):
        print(".", end="", flush=True)
        sleep(1)
    print()  # Move to the next line after the animation

def main():
    # Initialize the database logger and create tables
    db_logger = DatabaseLogger('arbitrage.db')

    # List of supported exchanges and symbols
    exchanges = [
        'binance', 'kraken', 'bitfinex', 'bittrex', 
        'poloniex', 'huobi', 'okx', 'coinbasepro', 
        'bitstamp', 'gemini'
    ]
    symbols = ['BTC/USD', 'ETH/USD', 'LTC/USD']

    # Initialize DataFetcher and ArbitrageCalculator
    data_fetcher = DataFetcher(exchanges, symbols)
    arbitrage_calculator = ArbitrageCalculator(db_logger)

    while True:
        # Fetch data
        logger.info("Fetching data from exchanges...")
        dot_animation(5)  # Display dot animation for 5 seconds
        data = data_fetcher.fetch_data()

        # Store fetched data in the database
        for symbol, exchange_data in data.items():
            for exchange_name, ticker_data in exchange_data.items():
                if ticker_data:
                    db_logger.log_ticker(exchange_name, symbol, ticker_data['last'])

        # Calculate arbitrage opportunities
        logger.info("Calculating arbitrage opportunities...")
        opportunities = arbitrage_calculator.calculate_arbitrage(data)

        if opportunities:
            logger.info(f"Found {len(opportunities)} arbitrage opportunities")
            for opportunity in opportunities:
                db_logger.log_opportunity(opportunity)
        else:
            logger.info("No arbitrage opportunities found")

        # Visualize the arbitrage opportunities
        visualize_opportunities('arbitrage.db')

        # Wait for 30 seconds before refreshing
        sleep(30)

if __name__ == "__main__":
    main()
