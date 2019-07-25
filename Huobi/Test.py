from unittest import TestCase
from Huobi.KeepBalanceStrategy import KeepBalanceStrategy


class TestKeepBalanceStrategy(TestCase):
    def setUp(self):
        self.strategy = KeepBalanceStrategy()

    def test_signal(self):
        self.strategy.signal()

    def test_buy(self):
        self.fail()

    def test_sell(self):
        self.fail()

    def test_update_balance_and_dollar(self):
        self.fail()

    def test_get_account_balance(self):
        balance_dict = self.strategy.get_account_balance()
        assert type(balance_dict) is dict

    def test_get_account_amount(self):
        self.fail()

    def test_get_mongodb_dollar(self):
        pass

    def test_get_price(self):
        price = self.strategy.get_price('btcusdt')
        self.assertGreaterEqual(price, 0)
