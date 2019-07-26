from unittest import TestCase
from MongdbHandler.MongodbTradeLock import MongodbTradeLock
from MongdbHandler.MongodbHandler import MongodbHandler


class TestMongodbHandler(TestCase):
    def test_init_mongodb(self):
        mongodb_handler = MongodbHandler()
        self.assertIsInstance(mongodb_handler, MongodbHandler)


class TestMongodbTradeLock(TestCase):
    def setUp(self):
        self.symbol_name = 'btc'
        self.strategy = 'KeepBalance'
        self.mongodb_handler = MongodbHandler()
        self.mongodb_trade_lock = MongodbTradeLock()

    def test_trade_lock(self):
        self.clean_test_record()
        self.assertEqual(self.count_lock_record_number(), 0)
        self.mongodb_trade_lock.trade_lock(self.symbol_name, self.strategy)
        self.assertEqual(self.count_lock_record_number(), 1)

    def test_trade_unlock(self):
        self.clean_test_record()
        self.mongodb_trade_lock.trade_lock(self.symbol_name, self.strategy)
        self.assertEqual(self.count_lock_record_number(), 1)
        self.mongodb_trade_lock.trade_unlock(self.symbol_name, self.strategy)
        self.assertEqual(self.count_lock_record_number(), 0)

    def test_check_trade_lock_exist(self):
        self.clean_test_record()
        self.mongodb_trade_lock.trade_lock(self.symbol_name, self.strategy)
        self.assertEqual(self.mongodb_trade_lock.check_trade_lock_exist(self.symbol_name, self.strategy), True)
        self.mongodb_trade_lock.trade_unlock(self.symbol_name, self.strategy)
        self.assertEqual(self.mongodb_trade_lock.check_trade_lock_exist(self.symbol_name, self.strategy), False)

    def count_lock_record_number(self):
        """
        获取满足条件的记录数
        :return:
        """
        count = self.mongodb_handler.lock_collection.count_documents({"symbol": self.symbol_name,
                                                                      "strategy": self.strategy})
        return count

    def clean_test_record(self):
        """
        清空测试数据, 避免上次遗留的测试数据
        :return:
        """
        self.mongodb_handler.lock_collection.delete_many({"symbol": self.symbol_name, "strategy": self.strategy})
