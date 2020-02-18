from threading import Thread

from huobi import SubscriptionClient
from huobi.model import *
from LogHandler.LogHandler import LogHandler
from ConfigHandler.ConfigHandler import ConfigHandler
from IO.File import FileReadAndWrite


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

    def callback(self, candlestick_event: 'CandlestickEvent'):
        content = f"{str(candlestick_event.timestamp)},{str(candlestick_event.data.close)}"
        FileReadAndWrite.write(f"{self.get_config_value('strategy', 'price_file_locate')}{candlestick_event.symbol}.txt",
                               content)

    def run(self, currency_pairs):
        self.sub_client.subscribe_candlestick_event(currency_pairs, CandlestickInterval.MIN1, self.callback)


if __name__ == '__main__':
    price_data = CollectPriceData()
    thread_btcusdt = Thread(target=price_data.run('btcusdt'))
    thread_hb10usdt = Thread(target=price_data.run('hb10usdt'))
    thread_eosusdt = Thread(target=price_data.run('eosusdt'))
    thread_btcusdt.start()
    thread_hb10usdt.start()
    thread_eosusdt.start()
