from huobi import RequestClient
from MongdbHandler.MongdbHandler import MongodbHandler
from huobi.model.symbol import Symbol


class MarketHandler(MongodbHandler):
    def __init__(self):
        self.request_client = RequestClient()

    def check_currency_precision(self):
        result_list = self.get_currency_precision()
        for key, value in enumerate(result_list):
            # self.insert_symbol_info(value)
            print(value)

    def get_currency_precision(self):
        """
        获取所有交易对数量精度与价格精度
        :return:
        """
        exchange_info = self.request_client.get_exchange_info()
        result = exchange_info.symbol_list
        result_list = []
        for key, value in enumerate(result):
            if type == dict:
                value = self.change_dict_to_symbol(value)
            result.append({"symbol": value.symbol, "quote_currency": value.quote_currency,
                           "base_currency": value.base_currency, "amount_precision": value.amount_precision,
                           "price_precision": value.price_precision, "symbol_partition": value.symbol_partition})
        return result_list

    def check_symbol_info(self, symbol_name):
        result = self.mongo_collection.find_one({"symbol": symbol_name})
        for each in result:
            print(each)

    def insert_symbol_info(self, symbol_info):
        self.mongo_collection.insert(symbol_info)

    @staticmethod
    def change_dict_to_symbol(symbol_dict):
        """
        将请求的交易对信息中dict类型的脏数据转换成Symbol类型
        :param symbol_dict:
        :return:
        """
        symbol = Symbol(symbol=symbol_dict['symbol'], quote_currency=symbol_dict['quote_currency'],
                        base_currency=symbol_dict['base_currency'], amount_precision=symbol_dict['amount_precision'],
                        price_precision=symbol_dict['price_precision'],
                        symbol_partition=symbol_dict['symbol_partition'])
        return symbol


if __name__ == '__main__':
    market_handler = MarketHandler()
    # market_handler.get_currency_precision()
    # market_handler.check_symbol_info('btcusdt')
    market_handler.check_currency_precision()
