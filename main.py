from connectivity.check_status import check_connection_and_api_status
from arbitrage.fetch_data import Binance, Huobi, OKX, Gateio, Coinbase, Kraken, Bitfinex, Bittrex, Poloniex, Kucoin
from arbitrage.calculate_arbitrage import ArbitrageCalculator
from arbitrage.log_data import DataLogger
from visualization.visualize import plot_arbitrage_opportunities

# Setup database and logger
logger = DataLogger()

# API URLs to check
api_urls = [
    'https://api.binance.com',
    'https://api.huobi.pro',
    'https://www.okx.com',
    'https://api.gateio.ws',
    'https://api.pro.coinbase.com',
    'https://api.kraken.com',
    'https://api.bitfinex.com',
    'https://api.bittrex.com',
    'https://api.poloniex.com',
    'https://api.kucoin.com'
]

# Ensure there is an internet connection and check API statuses
check_connection_and_api_status(api_urls)

# Initialize exchanges
exchange_classes = {
    'binance': Binance,
    'huobi': Huobi,
    'okx': OKX,
    'gateio': Gateio,
    'coinbase': Coinbase,
    'kraken': Kraken,
    'bitfinex': Bitfinex,
    'bittrex': Bittrex,
    'poloniex': Poloniex,
    'kucoin': Kucoin
}
exchanges = {name: exchange_class() for name, exchange_class in exchange_classes.items()}

# Log exchange names and get their IDs
exchange_ids = {name: logger.log_exchange(name) for name in exchanges}

# Fetch ticker data for all exchanges
tickers = {}
for name, exchange in exchanges.items():
    tickers[name] = exchange.fetch_tickers()
    # Log ticker data
    for ticker, data in tickers[name].items():
        logger.log_ticker(exchange_ids[name], ticker, data['last'])

# Calculate and log arbitrage opportunities between all pairs of exchanges
for exchange1_name, exchange1_data in tickers.items():
    for exchange2_name, exchange2_data in tickers.items():
        if exchange1_name != exchange2_name:
            arbitrage_calculator = ArbitrageCalculator(exchange1_name, exchange1_data, {exchange2_name: exchange2_data})
            arbitrage_opportunities = arbitrage_calculator.calculate_arbitrage()
            # Log arbitrage opportunities
            for opportunity in arbitrage_opportunities:
                logger.log_arbitrage_opportunity(
                    exchange_ids[opportunity['source_exchange']],
                    exchange_ids[opportunity['target_exchange']],
                    opportunity['ticker'],
                    opportunity['source_price'],
                    opportunity['target_price'],
                    opportunity['price_diff']
                )
            if arbitrage_opportunities:
                print(f"\nArbitrage Opportunities between {exchange1_name} and {exchange2_name}:")
                plot_arbitrage_opportunities(arbitrage_opportunities)

# Close the logger
logger.close()
