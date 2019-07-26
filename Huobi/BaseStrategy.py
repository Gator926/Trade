from MongdbHandler.MongodbTradeLock import MongodbTradeLock


class BaseStrategy(MongodbTradeLock):
    """
    策略基类
    """
    def __init__(self):
        MongodbTradeLock.__init__(self)

    def signal(self):
        raise NotImplementedError

    def buy(self, symbol_name, **kwargs):
        raise NotImplementedError

    def sell(self, symbol_name, **kwargs):
        raise NotImplementedError
