from LogHandler.LogHandler import LogHandler


class BaseStrategy(LogHandler):

    def signal(self):
        raise NotImplementedError

    def buy(self):
        raise NotImplementedError

    def sell(self):
        raise NotImplementedError
