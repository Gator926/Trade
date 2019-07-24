from LogHandler.LogHandler import LogHandler


class BaseStrategy(LogHandler):
    """
    策略基类
    """
    def __init__(self):
        LogHandler.__init__(self)

    def signal(self):
        raise NotImplementedError

    def buy(self, symbol_name, **kwargs):
        raise NotImplementedError

    def sell(self, symbol_name, **kwargs):
        raise NotImplementedError
