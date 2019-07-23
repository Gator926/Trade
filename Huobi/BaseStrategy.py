from LogHandler.LogHandler import LogHandler


class BaseStrategy(LogHandler):
    """
    策略基类
    """
    def signal(self):
        raise NotImplementedError

    def buy(self):
        raise NotImplementedError

    def sell(self):
        raise NotImplementedError
