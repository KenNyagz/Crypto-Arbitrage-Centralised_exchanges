import logging
from fetch_data import DataFetcher
from calculate_arbitrage import ArbitrageCalculator
from log_data import DataLogger

def main():
    """
    Main function to execute the arbitrage calculation process.
    """
    logging.basicConfig(level=logging.INFO)

    # Define the exchanges and initialize their respective data fetchers
    exchanges = {
        'binance': DataFetcher('binance', 'binance_api_key', 'binance_secret'),
        'huobi': DataFetcher('huobi', 'huobi_api_key', 'huobi_secret'),
        'okx': DataFetcher('okx', 'okx_api_key', 'okx_secret')
    }

    # Fetch data from all exchanges
    exchange_data = {}
    for exchange_name, fetcher in exchanges.items():
        try:
            exchange_data[exchange_name] = fetcher.fetch_data()
            logging.info(f"Fetched data for {exchange_name}: {exchange_data[exchange_name]}")
        except Exception as e:
            logging.error(f"Error fetching data for {exchange_name}: {e}")

    # Initialize the target exchanges dictionary
    target_exchanges = {name: data for name, data in exchange_data.items() if name != 'binance'}

    # Initialize the arbitrage calculator
    arbitrage_calculator = ArbitrageCalculator(
        name='binance',
        data=exchange_data['binance'],
        target_exchanges=target_exchanges,
        threshold=1.0
    )

    # Calculate arbitrage opportunities
    opportunities = arbitrage_calculator.calculate_arbitrage()

    # Log opportunities to the database
    data_logger = DataLogger('arbitrage.db')
    for opportunity in opportunities:
        buy_exchange_id = data_logger.log_exchange(opportunity['source_exchange'])
        sell_exchange_id = data_logger.log_exchange(opportunity['target_exchange'])
        data_logger.log_arbitrage_opportunity(
            buy_exchange_id,
            sell_exchange_id,
            opportunity['ticker'],
            opportunity['source_price'],
            opportunity['target_price'],
            opportunity['price_diff']
        )

    # Close data logger
    data_logger.close()

    logging.info("Arbitrage calculation process completed.")

if __name__ == "__main__":
    main()
