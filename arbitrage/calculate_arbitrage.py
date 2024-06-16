from .log_data import ArbitrageOpportunity
import logging

class ArbitrageCalculator:
    def __init__(self, logger):
        self.logger = logger

    def calculate_arbitrage(self, data):
        opportunities = []

        for symbol, exchange_data in data.items():
            for exchange1 in exchange_data:
                for exchange2 in exchange_data:
                    if exchange1 != exchange2:
                        if 'ask' in exchange_data[exchange1] and 'bid' in exchange_data[exchange2]:
                            ask_price = exchange_data[exchange1]['ask']
                            bid_price = exchange_data[exchange2]['bid']
                            if ask_price and bid_price:
                                percentage_diff = ((bid_price - ask_price) / ask_price) * 100
                                opportunities.append(ArbitrageOpportunity(
                                    symbol=symbol,
                                    base_currency=symbol.split('/')[0],
                                    quote_currency=symbol.split('/')[1],
                                    source_exchange=exchange1,
                                    target_exchange=exchange2,
                                    source_price=ask_price,
                                    target_price=bid_price,
                                    source_fee=0,  # Assuming no fees for simplicity
                                    target_fee=0,  # Assuming no fees for simplicity
                                    volume=1,  # Assuming volume of 1 for simplicity
                                    percentage=percentage_diff
                                ))
                            else:
                                self.logger.warning(f"Missing data for {symbol} on {exchange1} or {exchange2}")
                        else:
                            self.logger.warning(f"Missing bid or ask data for {symbol} on {exchange1} or {exchange2}")

        return opportunities
