def calculate_arbitrage(self):
    opportunities = []
    # Iterate through all tickers in the exchange data
    for ticker in self.data.keys():
        for target_exchange_name, target_exchange in self.target_exchanges.items():
            if ticker in target_exchange.keys():
                # Calculate the price difference
                price_diff = (self.data[ticker]['last'] - target_exchange[ticker]['last']) / self.data[ticker]['last'] * 100
                if abs(price_diff) > 0:
                    opportunities.append({
                        'ticker': ticker,
                        'source_exchange': self.name,
                        'target_exchange': target_exchange_name,
                        'source_price': self.data[ticker]['last'],
                        'target_price': target_exchange[ticker]['last'],
                        'price_diff': price_diff
                    })
    return opportunities
