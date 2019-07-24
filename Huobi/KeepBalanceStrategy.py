from Huobi.BaseStrategy import BaseStrategy
from MongdbHandler.MongdbHandler import MongodbHandler
from huobi.model import *
from huobi import RequestClient


class KeepBalanceStrategy(BaseStrategy, MongodbHandler):
    """
    动态平衡策略
    """

    def __init__(self):
        BaseStrategy.__init__(self)
        MongodbHandler.__init__(self)
        self.request_client = RequestClient(api_key=self.get_config_value("huobi", "api_key"),
                                            secret_key=self.get_config_value("huobi", "secret_key"))

    def signal(self, symbol_name):
        current_price = self.request_client.get_latest_candlestick(symbol_name, CandlestickInterval.MIN1, 1)
        print(current_price[0].close)

    def buy(self):
        pass

    def sell(self):
        pass

    def get_account_balance(self):
        balances = self.request_client.get_account_balance()
        balance_dict = {}
        for key, value in enumerate(balances[0].balances):
            if value.balance > 0:
                balance_dict[value.currency] = value.balance
        print(balance_dict)


if __name__ == '__main__':
    keep_balance_strategy = KeepBalanceStrategy()
    keep_balance_strategy.get_account_balance()
