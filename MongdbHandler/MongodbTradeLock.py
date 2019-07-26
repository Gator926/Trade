from MongdbHandler.MongodbHandler import MongodbHandler
from LogHandler.LogHandler import LogHandler
import datetime


class MongodbTradeLock(MongodbHandler):
    def __init__(self):
        MongodbHandler.__init__(self)

    def trade_lock(self, symbol_name: str, strategy: str) -> None:
        """
        交易同步锁, 避免重复交易
        :param symbol_name:
        :param strategy:
        :return:
        """
        document = {"symbol": symbol_name, "strategy": strategy, "time": datetime.datetime.now()}
        self.lock_collection.insert_one(document)
        self.logger.info(f"{strategy}策略的{symbol_name}币种交易正在执行, 已被锁定")

    def trade_unlock(self, symbol_name: str, strategy: str) -> None:
        """
        解除交易同步锁
        :param symbol_name:
        :param strategy:
        :return:
        """
        document = {"symbol": symbol_name, "strategy": strategy}
        self.lock_collection.delete_many(document)
        self.logger.info(f"{strategy}策略的{symbol_name}币种交易完成, 解除锁定")

    def check_trade_lock_exist(self, symbol_name: str, strategy: str) -> bool:
        """
        查看交易同步锁是否存在
        :param symbol_name:
        :param strategy:
        :return:
        """
        document = {"symbol": symbol_name, "strategy": strategy}
        count_documents = self.lock_collection.count_documents(document)
        if count_documents > 0:
            self.logger.info(f"{strategy}策略的{symbol_name}币种存在交易锁")
            return True
        else:
            self.logger.info(f"{strategy}策略的{symbol_name}币种未发现交易锁")
            return False
