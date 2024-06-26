import unittest
from unittest.mock import patch, MagicMock
import os
from wallet_connection import WalletManager

class TestWalletManager(unittest.TestCase):

    @patch.dict(os.environ, {
        'BINANCE_API_KEY': 'test_binance_api_key',
        'BINANCE_SECRET': 'test_binance_secret',
        'HUOBI_API_KEY': 'test_huobi_api_key',
        'HUOBI_SECRET': 'test_huobi_secret',
        'OKX_API_KEY': 'test_okx_api_key',
        'OKX_SECRET': 'test_okx_secret'
    })
    def setUp(self):
        self.wallet_manager = WalletManager()

    @patch('wallet_connection.input', return_value='one')
    @patch('wallet_connection.input', return_value='binance')
    @patch('ccxt.binance')
    def test_connect_to_single_exchange(self, mock_binance, mock_input_one, mock_input_exchange):
        mock_binance.return_value.fetch_balance.return_value = {'total': {'BTC': 1.0}}
        self.wallet_manager.connect_to_single_exchange()
        self.assertIn('binance', self.wallet_manager.exchanges)
        self.assertEqual(self.wallet_manager.get_balance('binance')['total']['BTC'], 1.0)

    @patch('wallet_connection.input', return_value='all')
    @patch('ccxt.binance')
    @patch('ccxt.huobi')
    @patch('ccxt.okx')
    def test_connect_to_all_exchanges(self, mock_okx, mock_huobi, mock_binance, mock_input):
        mock_binance.return_value.fetch_balance.return_value = {'total': {'BTC': 1.0}}
        mock_huobi.return_value.fetch_balance.return_value = {'total': {'ETH': 2.0}}
        mock_okx.return_value.fetch_balance.return_value = {'total': {'USDT': 3.0}}
        self.wallet_manager.connect_to_all_exchanges()
        self.assertIn('binance', self.wallet_manager.exchanges)
        self.assertIn('huobi', self.wallet_manager.exchanges)
        self.assertIn('okx', self.wallet_manager.exchanges)
        self.assertEqual(self.wallet_manager.get_balance('binance')['total']['BTC'], 1.0)
        self.assertEqual(self.wallet_manager.get_balance('huobi')['total']['ETH'], 2.0)
        self.assertEqual(self.wallet_manager.get_balance('okx')['total']['USDT'], 3.0)

    @patch('wallet_connection.time.time', side_effect=[0, 600])
    def test_check_session_timeout(self, mock_time):
        self.wallet_manager.exchanges = {'binance': MagicMock()}
        self.wallet_manager.last_access_time = {'binance': 0}
        self.wallet_manager.check_session_timeout()
        self.assertNotIn('binance', self.wallet_manager.exchanges)

    @patch('wallet_connection.ccxt.binance')
    def test_get_balance_ccxt_connection(self, mock_binance):
        mock_binance.return_value.fetch_balance.return_value = {'total': {'BTC': 1.0}}
        self.wallet_manager.exchanges['binance'] = mock_binance.return_value
        balance = self.wallet_manager.get_balance('binance')
        self.assertEqual(balance['total']['BTC'], 1.0)

    @patch('wallet_connection.ccxt.binance')
    def test_get_balance_ccxt_connection_failure(self, mock_binance):
        mock_binance.return_value.fetch_balance.side_effect = Exception("API error")
        self.wallet_manager.exchanges['binance'] = mock_binance.return_value
        balance = self.wallet_manager.get_balance('binance')
        self.assertIsNone(balance)

    @patch('wallet_connection.DirectConnection')
    def test_get_balance_direct_connection(self, mock_direct_connection):
        instance = mock_direct_connection.return_value
        instance.get_balance.return_value = {'BTC': 1.0}
        self.wallet_manager.exchanges['some_direct_exchange'] = instance
        balance = self.wallet_manager.get_balance('some_direct_exchange')
        self.assertEqual(balance['BTC'], 1.0)

    @patch('wallet_connection.DirectConnection')
    def test_get_balance_direct_connection_failure(self, mock_direct_connection):
        instance = mock_direct_connection.return_value
        instance.get_balance.side_effect = Exception("API error")
        self.wallet_manager.exchanges['some_direct_exchange'] = instance
        balance = self.wallet_manager.get_balance('some_direct_exchange')
        self.assertIsNone(balance)

    @patch('wallet_connection.input', return_value='invalid_exchange')
    def test_invalid_exchange_choice(self, mock_input):
        self.wallet_manager.connect_to_single_exchange()
        self.assertNotIn('invalid_exchange', self.wallet_manager.exchanges)

if __name__ == '__main__':
    unittest.main()
