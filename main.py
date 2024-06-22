import logging
import threading
import time
import concurrent.futures
from arbitrage.fetch_data import DataFetcher
from arbitrage.calculate_arbitrage import ArbitrageCalculator
from arbitrage.log_data import DatabaseLogger
from visualization.visualize import plot_data

# Configure logging to display info messages with timestamps
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('main')

def fetch_data_task(data_fetcher):
    """
    Fetch market data using the DataFetcher instance.
    """
    logger.info("Fetching market data.")
    data = data_fetcher.fetch_data()
    logger.info("Market data fetched successfully.")
    return data

def calculate_arbitrage_task(data, arbitrage_calculator, db_logger):
    """
    Calculate arbitrage opportunities using the provided market data and ArbitrageCalculator instance,
    then log the results using DatabaseLogger.
    """
    logger.info("Calculating arbitrage opportunities.")
    executable_opportunities, outliers = arbitrage_calculator.calculate_arbitrage(data)
    logger.info("Arbitrage opportunities calculated successfully.")

    # Log opportunities and outliers
    for opportunity in executable_opportunities:
        db_logger.log_opportunity(opportunity)
        logger.info(f"Arbitrage opportunity logged successfully: {opportunity}")

    for outlier in outliers:
        db_logger.log_outlier(outlier)
        logger.info(f"Outlier logged successfully: {outlier}")

    return executable_opportunities, outliers

def main():
    while True:
        logger.info("Starting the arbitrage detection process.")

        # Define the exchanges and symbols to fetch data for
        exchanges = ['binance', 'kraken', 'htx', 'coinbase', 'bitfinex', 'gemini', 'bittrex', 'bybit', 'huobi']
        symbols = [
            'ETH/USD', 'BTC/USD', 'USDT/USD', 'BNB/USDT', 'ADA/USD', 'XRP/USD',
            'LTC/USD', 'SOL/USD', 'DOT/USD', 'LINK/USD', 'USDC/USD'
        ]
        public_api_urls = {
            'binance': 'https://api.binance.com/api/v3/ticker/price',
            'kraken': 'https://api.kraken.com/0/public/Ticker',
            'coinbase_pro': 'https://api.pro.coinbase.com/products/ticker',
            'cryptocompare': 'https://min-api.cryptocompare.com/data/pricemultifull',
            'coinmarketcap': 'https://api.coinmarketcap.com/v1/ticker/',
            'huobi': 'https://api.huobi.com/market/tickers',
            'gateio': 'https://api.gateio.ws/api/v4/spot/tickers',
            'bitfinex': 'https://api.bitfinex.com/v2/tickers',
            'bittrex': 'https://api.bittrex.com/v3/markets/tickers',
            'poloniex': 'https://poloniex.com/public?command=returnTicker',
            'kucoin': 'https://api.kucoin.com/api/v1/market/tickers'
        }

        # Initialize components
        logger.info("Initializing data fetcher.")
        data_fetcher = DataFetcher(exchanges, symbols, public_api_urls)

        logger.info("Initializing database logger.")
        db_logger = DatabaseLogger('arbitrage.db')
        db_logger._create_tables()  # Ensure tables are created

        logger.info("Initializing arbitrage calculator.")
        arbitrage_calculator = ArbitrageCalculator(db_logger)  # Pass db_logger instance here

        # Use ThreadPoolExecutor to fetch data and calculate arbitrage concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit fetch data task to the executor
            future_data = executor.submit(fetch_data_task, data_fetcher)
            data = future_data.result()

            # Submit calculate arbitrage task to the executor
            future_arbitrage = executor.submit(calculate_arbitrage_task, data, arbitrage_calculator, db_logger)
            executable_opportunities, outliers = future_arbitrage.result()

        # Log results
        logger.info(f"Executable opportunities: {len(executable_opportunities)} found.")
        for opportunity in executable_opportunities:
            logger.info(opportunity)

        logger.info(f"Outliers: {len(outliers)} found.")
        for outlier in outliers:
            logger.info(outlier)

        # Visualize opportunities
        logger.info("Visualizing arbitrage opportunities.")
        plot_data('arbitrage.db')

        # Close database connection
        logger.info("Closing database connection.")
        db_logger.close()

        logger.info("Arbitrage detection process completed.")

        # Wait for 5 minutes (300 seconds) before the next execution
        time.sleep(300)

if __name__ == '__main__':
    main()
