from huobi import SubscriptionClient
from huobi.model import *
from LogHandler.LogHandler import LogHandler
from ConfigHandler.ConfigHandler import ConfigHandler


class CollectAccountData(LogHandler, ConfigHandler):
    def __init__(self):
        LogHandler.__init__(self)
        ConfigHandler.__init__(self)
        self.sub_client = SubscriptionClient(api_key=self.get_config_value("huobi", "api_key"),
                                             secret_key=self.get_config_value("huobi", "secret_key"))

    @staticmethod
    def callback(account_event: 'AccountEvent'):
        print("---- Account Change: " + account_event.change_type + " ----")
        for change in account_event.account_change_list:
            print("Account: " + change.account_type)
            print("Currency: " + change.currency)
            print("Balance: " + str(change.balance))
            print("Balance type: " + str(change.balance_type))

    def run(self):
        self.sub_client.subscribe_account_event(BalanceMode.TOTAL, self.callback)


class CollectPriceData(ConfigHandler):
    def __init__(self):
        ConfigHandler.__init__(self)
        self.sub_client = SubscriptionClient()

    @staticmethod
    def callback(candlestick_event: 'CandlestickEvent'):
        print("Timestamp: " + str(int(candlestick_event.timestamp / 1000 / 60)))
        print("Symbol: " + candlestick_event.symbol)
        print("High: " + str(candlestick_event.data.high))
        print("Low: " + str(candlestick_event.data.low))
        print("Open: " + str(candlestick_event.data.open))
        print("Close: " + str(candlestick_event.data.close))
        print("Volume: " + str(candlestick_event.data.volume))
        print()

    def run(self):
        self.sub_client.subscribe_candlestick_event("btcusdt", CandlestickInterval.MIN1, self.callback)


if __name__ == '__main__':
    collect_price_data = CollectPriceData()
    collect_price_data.run()
