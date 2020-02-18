from unittest import TestCase
from Trade.Huobi import KeepBalanceStrategy
from Trade.Huobi import MarketHandler
from MongdbHandler.MongodbHandler import MongodbHandler
import copy


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

    def test_get_mongodb_dollar_with_empty_data(self):
        self.strategy.get_mongodb_dollar('')

    def test_get_mongodb_dollar_with_data(self):
        pass

    def test_get_price(self):
        price = self.strategy.get_price('btcusdt')
        self.assertGreaterEqual(price, 0)


class TestMarketHandler(TestCase):
    def setUp(self):
        self.symbol_info = {'symbol': 'bhtusdt', 'quote_currency': 'usdt', 'base_currency': 'bht',
                            'amount_precision': 2, 'price_precision': 6, 'symbol_partition': 'innovation'}
        self.market_handler = MarketHandler()
        self.mongodb_handler = MongodbHandler()

    def test_check_currency_precision(self):
        self.market_handler.check_currency_precision()

    def test_get_currency_precision(self):
        precision = self.market_handler.get_currency_precision()
        self.assertIsInstance(precision, list)
        self.assertIsInstance(precision[0], dict)

    def test_check_symbol_info_with_empty_data(self):
        """
        检查交易对信息与数据库是否一致(无数据情况)
        :return:
        """
        self.mongodb_handler.precision_collection.delete_many({})

        self.market_handler.check_symbol_info(self.symbol_info)
        number = self.mongodb_handler.precision_collection.count_documents(
            {"symbol": self.symbol_info['symbol']})
        self.assertEqual(number, 1)

    def test_check_symbol_info_with_changed_data(self):
        """
        检查交易对信息与数据库是否一致(数据变更)
        :return:
        """
        self.mongodb_handler.precision_collection.delete_many({})

        changed_symbol_info = copy.deepcopy(self.symbol_info)
        changed_symbol_info['amount_precision'] = 3
        self.market_handler.check_symbol_info(changed_symbol_info)
        result = self.mongodb_handler.precision_collection.find_one(
            {"symbol": self.symbol_info['symbol']})
        self.assertEqual(result['amount_precision'], 3)

    def test_change_dict_to_symbol(self):
        symbol = self.market_handler.change_dict_to_symbol(self.symbol_info)
        self.assertEqual(symbol.symbol, self.symbol_info['symbol'])
        self.assertEqual(symbol.quote_currency, self.symbol_info['quote_currency'])
        self.assertEqual(symbol.base_currency, self.symbol_info['base_currency'])
        self.assertEqual(symbol.amount_precision, self.symbol_info['amount_precision'])
        self.assertEqual(symbol.price_precision, self.symbol_info['price_precision'])
        self.assertEqual(symbol.symbol_partition, self.symbol_info['symbol_partition'])
