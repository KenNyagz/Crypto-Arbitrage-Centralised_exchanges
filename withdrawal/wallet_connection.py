import os
import ccxt
import logging
import time
from dotenv import load_dotenv
from direct_connect import DirectConnector

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('wallet')

# Constants for session timeout
SESSION_TIMEOUT = 300  # 5 minutes

class WalletManager:
    def __init__(self):
        # Dictionary to hold exchange instances
        self.exchanges = {}
        # Dictionary to track the last access time of each exchange
        self.last_access_time = {}
        # Load API keys and initialize exchanges based on user choice
        self.load_api_keys()

    def load_api_keys(self):
        """
        Load API keys and initialize exchanges based on user input.
        """
        user_choice = input("Do you want to connect to all exchanges or one in particular? (all/one): ").strip().lower()
        if user_choice == 'all':
            # Connect to all exchanges
            self.connect_to_all_exchanges()
        elif user_choice == 'one':
            # Prompt user to choose a specific exchange
            self.connect_to_single_exchange()
        else:
            logger.error("Invalid choice. Please choose 'all' or 'one'.")

    def connect_to_all_exchanges(self):
        """
        Connect to all exchanges using environment variables.
        """
        exchanges = ['binance', 'huobi', 'okx']
        for exchange_name in exchanges:
            self.initialize_exchange(exchange_name)

    def connect_to_single_exchange(self):
        """
        Prompt the user to choose a specific exchange to connect to.
        """
        exchanges = ['binance', 'huobi', 'okx']
        exchange_choice = input(f"Choose an exchange to connect to ({', '.join(exchanges)}): ").strip().lower()
        if exchange_choice in exchanges:
            self.initialize_exchange(exchange_choice)
        else:
            logger.error(f"Invalid exchange choice: {exchange_choice}")

    def initialize_exchange(self, exchange_name):
        """
        Initialize connection to an exchange using ccxt or directly if not supported.
        """
        try:
            api_key = os.getenv(f'{exchange_name.upper()}_API_KEY')
            secret = os.getenv(f'{exchange_name.upper()}_SECRET')
            if not api_key or not secret:
                logger.error(f"No API key/secret found for {exchange_name}.")
                return

            # Try to get the exchange class from ccxt
            exchange_class = getattr(ccxt, exchange_name, None)
            if exchange_class:
                # Initialize exchange using ccxt
                exchange = exchange_class({
                    'apiKey': api_key,
                    'secret': secret,
                    'enableRateLimit': True,
                })
                self.exchanges[exchange_name] = exchange
                logger.info(f"Connected to {exchange_name} exchange via ccxt.")
            else:
                # If ccxt does not support the exchange, connect directly
                logger.warning(f"Exchange {exchange_name} not supported by ccxt. Trying direct connection.")
                direct_connection = DirectConnector()
                direct_connection.connect(exchange_name, api_key, secret)
                self.exchanges[exchange_name] = direct_connection
                logger.info(f"Directly connected to {exchange_name} exchange.")
            # Update the last access time for the exchange
            self.last_access_time[exchange_name] = time.time()
        except Exception as e:
            logger.error(f"Failed to connect to {exchange_name}: {str(e)}")

    def check_session_timeout(self):
        """
        Check if any exchange sessions have timed out and disconnect them.
        """
        current_time = time.time()
        for exchange_name in list(self.exchanges.keys()):
            if current_time - self.last_access_time[exchange_name] > SESSION_TIMEOUT:
                logger.info(f"Session for {exchange_name} has timed out. Disconnecting.")
                del self.exchanges[exchange_name]
                del self.last_access_time[exchange_name]

    def get_balance(self, exchange_name):
        """
        Fetch the balance from the specified exchange.
        """
        self.check_session_timeout()
        if exchange_name in self.exchanges:
            try:
                exchange = self.exchanges[exchange_name]
                if isinstance(exchange, DirectConnector):  # Direct connection
                    return exchange.get_balance()
                else:  # ccxt connection
                    balance = exchange.fetch_balance()
                    self.last_access_time[exchange_name] = time.time()  # Update access time
                    return balance
            except Exception as e:
                logger.error(f"Failed to fetch balance from {exchange_name}: {str(e)}")
        else:
            logger.error(f"Exchange {exchange_name} not initialized or session timed out.")
        return None

# Example usage
if __name__ == '__main__':
    wallet_manager = WalletManager()

    # Example: Fetch balance
    exchange_choice = input("Enter the exchange to fetch balance from: ").strip().lower()
    balance = wallet_manager.get_balance(exchange_choice)
    if balance:
        print(f"{exchange_choice.capitalize()} Balance:", balance)
