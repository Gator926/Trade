from huobi import RequestClient
from MongdbHandler.MongdbHandler import MongodbHandler


class MarketHandler(MongodbHandler):
    def __init__(self):
        self.request_client = RequestClient()

    def get_currency_precision(self):
        exchange_info = self.request_client.get_exchange_info()
        result = exchange_info.symbol_list
        for each in result:
            print(each)

    def check_symbol_info(self, symbol_name):
        result = self.collection.find_one({"symbol": symbol_name})
        for each in result:
            print(each)


if __name__ == '__main__':
    market_handler = MarketHandler()
    # market_handler.get_currency_precision()
    # market_handler.check_symbol_info('btcusdt')
    market_handler.get_currency_precision()
