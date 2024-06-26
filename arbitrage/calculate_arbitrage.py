import logging
from arbitrage.log_data import ArbitrageOpportunity

# Set up a logger named 'calculate_arbitrage'
logger = logging.getLogger('calculate_arbitrage')

class ArbitrageCalculator:
    def __init__(self, db_logger):
        # Initialize the ArbitrageCalculator with a database logger
        self.db_logger = db_logger

    def calculate_arbitrage(self, data):
        executable_opportunities = []  # List to store executable arbitrage opportunities
        outliers = []  # List to store detected outliers

        # Iterate over each exchange and its corresponding symbols data
        for exchange, symbols_data in data.items():
            # Iterate over each symbol and its ticker data
            for symbol, ticker_data in symbols_data.items():
                # Check if 'last' price is available
                if 'last' not in ticker_data:
                    logger.warning(f"'last' price not found for {symbol} on {exchange}.")
                    continue

                # Check if symbol format is valid
                if '/' not in symbol:
                    logger.warning(f"Invalid symbol format from {exchange}: {symbol}")
                    continue

                # Extract base and quote currencies
                base_currency, quote_currency = symbol.split('/')
                last_price = ticker_data['last']

                prices = []  # List to store prices from different exchanges
                exchanges = []  # List to store exchange names

                # Collect prices and exchanges for the current symbol
                for ex, sym_data in data.items():
                    if symbol in sym_data and 'last' in sym_data[symbol]:
                        prices.append(sym_data[symbol]['last'])
                        exchanges.append(ex)

                # If there are fewer than 2 prices, skip to the next symbol
                if len(prices) < 2:
                    continue

                # Calculate minimum and maximum prices and their respective indices
                min_price = min(prices)
                max_price = max(prices)
                min_index = prices.index(min_price)
                max_index = prices.index(max_price)

                # Calculate the percentage difference between the max and min prices
                percentage_difference = ((max_price - min_price) / min_price) * 100

                # Log the current state of prices and percentage difference
                logger.debug(f"Checking {symbol} across exchanges: {exchanges}, prices: {prices}, "
                             f"min_price: {min_price}, max_price: {max_price}, percentage_difference: {percentage_difference:.6f}")

                # If the percentage difference is greater than 1%, consider it an arbitrage opportunity
                if percentage_difference > 1:
                    opportunity = ArbitrageOpportunity(
                        symbol=symbol,
                        base_currency=base_currency,
                        quote_currency=quote_currency,
                        source_exchange=exchanges[min_index],
                        target_exchange=exchanges[max_index],
                        source_price=min_price,
                        target_price=max_price,
                        source_fee=0,  # Replace with actual fee if available
                        target_fee=0,  # Replace with actual fee if available
                        volume=0,  # Replace with actual volume if available
                        percentage=percentage_difference
                    )
                    executable_opportunities.append(opportunity)  # Add the opportunity to the list
                    self.db_logger.log_opportunity(opportunity)  # Log the opportunity in the database
                    logger.info(f"Arbitrage opportunity found: {opportunity}")

                # If the percentage difference is greater than 0%, consider it an outlier
                elif percentage_difference > 0:
                    outliers.append({
                        'symbol': symbol,
                        'base_currency': base_currency,
                        'quote_currency': quote_currency,
                        'source_exchange': exchanges[min_index],
                        'target_exchange': exchanges[max_index],
                        'source_price': min_price,
                        'target_price': max_price,
                        'percentage': percentage_difference
                    })

        # Log the number of executable opportunities and outliers found
        logger.info(f"Executable opportunities: {len(executable_opportunities)} found.")
        logger.info(f"Outliers: {len(outliers)} found.")
        
        return executable_opportunities, outliers  # Return the lists of opportunities and outliers
