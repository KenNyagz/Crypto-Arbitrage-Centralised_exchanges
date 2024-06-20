import logging
from arbitrage.log_data import ArbitrageOpportunity

logger = logging.getLogger('calculate_arbitrage')

class ArbitrageCalculator:
    def __init__(self, db_logger):
        self.db_logger = db_logger

    def calculate_arbitrage(self, data):
        executable_opportunities = []
        outliers = []
        for exchange, symbols_data in data.items():
            for symbol, ticker_data in symbols_data.items():
                if 'last' not in ticker_data:
                    logger.warning(f"'last' price not found for {symbol} on {exchange}.")
                    continue

                if '/' not in symbol:
                    logger.warning(f"Invalid symbol format from {exchange}: {symbol}")
                    continue

                base_currency, quote_currency = symbol.split('/')
                last_price = ticker_data['last']

                prices = []
                exchanges = []
                for ex, sym_data in data.items():
                    if symbol in sym_data and 'last' in sym_data[symbol]:
                        prices.append(sym_data[symbol]['last'])
                        exchanges.append(ex)

                if len(prices) < 2:
                    continue

                min_price = min(prices)
                max_price = max(prices)
                min_index = prices.index(min_price)
                max_index = prices.index(max_price)

                percentage_difference = ((max_price - min_price) / min_price) * 100

                if percentage_difference > 0:
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
                    executable_opportunities.append(opportunity)
                    self.db_logger.log_opportunity(opportunity)
                    logger.info(f"Arbitrage opportunity found: {opportunity}")

                if percentage_difference < -1 or percentage_difference > 1:
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

        return executable_opportunities, outliers
