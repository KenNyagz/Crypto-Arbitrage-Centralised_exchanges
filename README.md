# Crypto-Arbitrage-Centralised_exchanges-1

## Overview
This project aims to identify cryptocurrency arbitrage opportunities across multiple centralized exchanges. It fetches ticker data from various exchanges, calculates potential arbitrage opportunities, and provides tools to visualize these opportunities. Additionally, it includes functionality to check connectivity and API status, handle withdrawals, and manage API keys securely.

## Project Structure
Crypto-Arbitrage-Centralised_exchanges-1/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── keys/
│ ├── binance_key.txt
│ ├── huobi_key.txt
│ └── okx_key.txt
├── connectivity/
│ └── check_connection.py
├── withdrawal/
│ └── withdrawal.py
├── visualization/
│ └── visualize.py
├── arbitrage/
│ ├── fetch_data.py
│ └── calculate_arbitrage.py
└── venv/


### 1. **Keys Folder**: 
- **Purpose**: Stores API keys for different exchanges in separate files.
- **Files**:
  - `binance_key.txt`
  - `huobi_key.txt`
  - `okx_key.txt`

### 2. **Connectivity Folder**: 
- **Purpose**: Contains functionality to check internet connectivity and the status of APIs.
- **Files**:
  - `check_connection.py`: Checks if there is an internet connection and if the APIs are reachable.

### 3. **Withdrawal Folder**: 
- **Purpose**: Handles withdrawals from exchanges.
- **Files**:
  - `withdrawal.py`: Contains functions to perform withdrawals.

### 4. **Visualization Folder**: 
- **Purpose**: Provides tools for visualizing arbitrage opportunities.
- **Files**:
  - `visualize.py`: Contains functions to plot arbitrage data.

### 5. **Arbitrage Folder**: 
- **Purpose**: Contains modules for fetching data from exchanges and calculating arbitrage opportunities.
- **Files**:
  - `fetch_data.py`: Fetches ticker data from exchanges.
  - `calculate_arbitrage.py`: Identifies arbitrage opportunities and calculates potential profit percentages.

### 6. **Main Script**: 
- **File**: `main.py`
- **Purpose**: Orchestrates the functionality by calling functions from different modules.

## Installation

1. **Clone the Repository**
    ```sh
    git clone https://github.com/yourusername/Crypto-Arbitrage-Centralised_exchanges-1.git
    cd Crypto-Arbitrage-Centralised_exchanges-1
    ```

2. **Create a Virtual Environment**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the Dependencies**
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. **Add API Keys**
   - Place your API keys in the `keys/` folder:
     - `binance_key.txt`
     - `huobi_key.txt`
     - `okx_key.txt`

2. **Configure API Connectivity Check**
   - Ensure that the `connectivity/check_connection.py` script has the correct URLs to check the status of the APIs you are using.

## Usage

1. **Run the Main Script**
    ```sh
    python main.py
    ```

2. **Functionality Breakdown**

### Connectivity Check
- **File**: `connectivity/check_connection.py`
- **Function**: `check_connection_and_api_status(api_urls)`
  - Checks if there is an internet connection and if specified APIs are reachable.

### Fetching Ticker Data
- **File**: `arbitrage/fetch_data.py`
- **Function**: `fetch_tickers(exchange)`
  - Fetches ticker data from the specified exchange.

### Calculating Arbitrage Opportunities
- **File**: `arbitrage/calculate_arbitrage.py`
- **Function**: `get_arbtg(exchange1_name, exchange2_name, exchange1_tickers, exchange2_tickers)`
  - Identifies common tickers between two exchanges and calculates the percentage differences for potential arbitrage.

### Visualizing Data
- **File**: `visualization/visualize.py`
- **Function**: `plot_arbitrage_opportunities(arbitrage_data)`
  - Plots arbitrage opportunities using matplotlib.

### Main Orchestration
- **File**: `main.py`
- **Description**: The main script that integrates all functionalities:
  - Checks internet connection and API statuses.
  - Initializes exchanges using the `ccxt` library.
  - Fetches ticker data from multiple exchanges.
  - Calculates arbitrage opportunities between pairs of exchanges.
  - Visualizes the identified arbitrage opportunities.

