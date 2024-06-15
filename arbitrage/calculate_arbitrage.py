import logging

class ArbitrageCalculator:
    def __init__(self, name, data, target_exchanges, threshold=0.5):
        """
        Initialize the ArbitrageCalculator.

        Parameters:
        name (str): The name of the source exchange.
        data (dict): Ticker data from the source exchange.
        target_exchanges (dict): Dictionary of target exchanges with their ticker data.
        threshold (float): Minimum price difference percentage to consider as arbitrage opportunity.
        """
        self.name = name
        self.data = data
        self.target_exchanges = target_exchanges
        self.threshold = threshold
        logging.basicConfig(level=logging.INFO)

    def calculate_arbitrage(self):
        """
        Calculate arbitrage opportunities between the source exchange and target exchanges.

        Returns:
        list: A list of dictionaries containing arbitrage opportunities.
        """
        opportunities = []

        # Iterate through all tickers in the source exchange data
        for ticker, source_data in self.data.items():
            # Iterate through all target exchanges
            for target_exchange_name, target_exchange in self.target_exchanges.items():
                # Check if the target exchange has the same ticker
                if ticker in target_exchange:
                    target_data = target_exchange[ticker]

                    # Calculate the price difference as a percentage
                    price_diff = (source_data['last'] - target_data['last']) / source_data['last'] * 100

                    # Check if the price difference exceeds the threshold
                    if abs(price_diff) >= self.threshold:
                        # Create an arbitrage opportunity dictionary
                        opportunity = {
                            'ticker': ticker,
                            'source_exchange': self.name,
                            'target_exchange': target_exchange_name,
                            'source_price': source_data['last'],
                            'target_price': target_data['last'],
                            'price_diff': price_diff
                        }

                        # Add the opportunity to the list
                        opportunities.append(opportunity)

                        # Log the opportunity for debugging and monitoring
                        logging.info(f"Arbitrage Opportunity: {opportunity}")

        return opportunities
