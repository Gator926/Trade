from MongdbHandler.MongodbHandler import MongodbHandler
import datetime


def trade_lock(symbol_name, strategy):
    """
    交易同步锁, 避免重复交易
    :param symbol_name:
    :param strategy:
    :return:
    """
    mongodb_handler = MongodbHandler()
    document = {"symbol": symbol_name, "strategy": strategy, "time": datetime.datetime.now()}
    mongodb_handler.lock_collection.insert_one(document)


def trade_unlock(symbol_name, strategy):
    """
    解除交易同步锁
    :param symbol_name:
    :param strategy:
    :return:
    """
    mongodb_handler = MongodbHandler()
    document = {"symbol": symbol_name, "strategy": strategy}
    mongodb_handler.lock_collection.delete_many(document)
