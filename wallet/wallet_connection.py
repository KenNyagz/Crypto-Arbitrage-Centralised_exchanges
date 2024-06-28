import os
import ccxt
import logging
import time
from dotenv import load_dotenv
from direct_connect import DirectConnector
from arbitrage.log_data import DatabaseLogger

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('wallet')

# Constants for session timeout and popular currencies
SESSION_TIMEOUT = 300  # 5 minutes
POPULAR_CURRENCIES = ['BTC', 'ETH', 'USDT', 'BNB', 'ADA', 'XRP', 'SOL', 'DOT', 'DOGE', 'LTC']

class WalletManager:
    def __init__(self):
        self.exchanges = {}  # Dictionary to hold exchange instances
        self.last_access_time = {}  # Dictionary to track the last access time of each exchange
        self.db_logger = DatabaseLogger('arbitrage.db')  # Initialize the DatabaseLogger
        self.db_logger._create_tables()  # Ensure the tables are created
        self.load_api_keys()  # Load API keys and initialize exchanges

    def load_api_keys(self):
        """
        Load API keys and initialize exchanges based on user input.
        """
        user_choice = input("Do you want to connect to all exchanges or one in particular? (all/one): ").strip().lower()
        if user_choice == 'all':
            self.connect_to_all_exchanges()
        elif user_choice == 'one':
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

            exchange_class = getattr(ccxt, exchange_name, None)
            if exchange_class:
                exchange = exchange_class({
                    'apiKey': api_key,
                    'secret': secret,
                    'enableRateLimit': True,
                })
                self.exchanges[exchange_name] = exchange
                logger.info(f"Connected to {exchange_name} exchange via ccxt.")
            else:
                logger.warning(f"Exchange {exchange_name} not supported by ccxt. Trying direct connection.")
                direct_connection = DirectConnector()
                direct_connection.connect(exchange_name, api_key, secret)
                self.exchanges[exchange_name] = direct_connection
                logger.info(f"Directly connected to {exchange_name} exchange.")
            self.last_access_time[exchange_name] = time.time()
        except Exception as e:
            logger.error(f"Failed to connect to {exchange_name}: {str(e)}")

    def check_session_timeout(self):
        """
        Check if any exchange sessions have timed out and disconnect them.
        """
        current_time = time.time()
        timed_out_exchanges = [exchange for exchange, last_access in self.last_access_time.items()
                               if current_time - last_access > SESSION_TIMEOUT]
        for exchange in timed_out_exchanges:
            logger.info(f"Session for {exchange} has timed out. Disconnecting.")
            del self.exchanges[exchange]
            del self.last_access_time[exchange]

    def get_balance(self, exchange_name, retries=3):
        """
        Fetch the balance from the specified exchange and limit to 10 most popular currencies.
        Retries fetching the balance up to 'retries' times in case of failure.
        """
        self.check_session_timeout()
        if exchange_name in self.exchanges:
            for attempt in range(retries):
                try:
                    exchange = self.exchanges[exchange_name]
                    if isinstance(exchange, DirectConnector):
                        balance = exchange.get_balance()
                    else:
                        balance = exchange.fetch_balance()
                    self.last_access_time[exchange_name] = time.time()
                    if balance:
                        limited_balance = {currency: balance['total'][currency] for currency in POPULAR_CURRENCIES if currency in balance['total']}
                        return limited_balance
                except Exception as e:
                    logger.error(f"Failed to fetch balance from {exchange_name} (Attempt {attempt + 1}/{retries}): {str(e)}")
        else:
            logger.error(f"Exchange {exchange_name} not initialized or session timed out.")
        return None

    def manual_refresh(self):
        """
        Allow manual refresh of all exchange sessions.
        """
        for exchange_name in list(self.exchanges.keys()):
            logger.info(f"Refreshing session for {exchange_name}.")
            self.initialize_exchange(exchange_name)

    def list_supported_exchanges(self):
        """
        List all supported exchanges.
        """
        return ['binance', 'huobi', 'okx']

    def check_api_key_validity(self, exchange_name):
        """
        Validate if the provided API keys are valid for the specified exchange.
        """
        if exchange_name in self.exchanges:
            try:
                exchange = self.exchanges[exchange_name]
                if isinstance(exchange, DirectConnector):
                    valid = exchange.validate_api_keys()
                else:
                    exchange.fetch_balance()
                    valid = True
                return valid
            except Exception as e:
                logger.error(f"Invalid API keys for {exchange_name}: {str(e)}")
                return False
        else:
            logger.error(f"Exchange {exchange_name} not initialized.")
        return False

    def log_balances_to_db(self, exchange_name, balance):
        """
        Log fetched balances to the database.
        """
        try:
            for currency, amount in balance.items():
                if isinstance(amount, dict):
                    free = amount.get('free', 0)
                    locked = amount.get('locked', 0)
                else:
                    free = amount
                    locked = 0
                self.db_logger.log_balance(exchange_name, currency, free, locked)
            logger.info(f"Balances for {exchange_name} logged to database successfully.")
        except Exception as e:
            logger.error(f"Error logging balances to database: {e}")

# main menu for wallet
if __name__ == '__main__':
    wallet_manager = WalletManager()

    def main_menu():
        while True:
            print("\nMain Menu:")
            print("1. Connect and fetch balance from a single exchange")
            print("2. Connect and fetch balances from all exchanges")
            print("3. List supported exchanges")
            print("4. Refresh all sessions")
            print("5. Check API key validity")
            print("6. Exit")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                exchange_choice = input("Enter the exchange to fetch balance from: ").strip().lower()
                balance = wallet_manager.get_balance(exchange_choice)
                if balance:
                    print(f"{exchange_choice.capitalize()} Balance:", balance)
                    wallet_manager.log_balances_to_db(exchange_choice, balance)
                else:
                    print(f"Failed to fetch balance for {exchange_choice}.")
                    
            elif choice == '2':
                for exchange in wallet_manager.list_supported_exchanges():
                    balance = wallet_manager.get_balance(exchange)
                    if balance:
                        print(f"{exchange.capitalize()} Balance:", balance)
                        wallet_manager.log_balances_to_db(exchange, balance)
                    else:
                        print(f"Failed to fetch balance for {exchange}.")
                    
            elif choice == '3':
                print("Supported exchanges:", wallet_manager.list_supported_exchanges())
                
            elif choice == '4':
                refresh_choice = input("Do you want to refresh all sessions? (yes/no): ").strip().lower()
                if refresh_choice == 'yes':
                    wallet_manager.manual_refresh()
                    print("Sessions refreshed successfully.")
                else:
                    print("Session refresh canceled.")
                    
            elif choice == '5':
                api_check_choice = input("Enter the exchange to check API key validity: ").strip().lower()
                if wallet_manager.check_api_key_validity(api_check_choice):
                    print(f"API keys for {api_check_choice} are valid.")
                else:
                    print(f"API keys for {api_check_choice} are invalid.")
                    
            elif choice == '6':
                print("Exiting the program.")
                break
                
            else:
                print("Invalid choice. Please select a valid option.")

    main_menu()

