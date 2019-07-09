from huobi import RequestClient
from huobi.model import *
import time


class MarketHandler:
    def __init__(self):
        self.request_client = RequestClient()
        exchange_info = self.request_client.get_exchange_info()
        result = exchange_info.symbol_list
        for each in result:
            print(each)


if __name__ == '__main__':
    market_handler = MarketHandler()
