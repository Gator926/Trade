from huobi import RequestClient
from MongdbHandler.MongdbHandler import MongodbHandler
from huobi.model.symbol import Symbol


class MarketHandler(MongodbHandler):
    def __init__(self):
        MongodbHandler.__init__(self)
        self.request_client = RequestClient()
        self.symbol_key_list = self.get_config_value("symbol", "symbol_key_list").split(",")

    def check_currency_precision(self):
        result_list = self.get_currency_precision()
        for key, value in enumerate(result_list):
            self.check_symbol_info(value)
            self.logger.info(value)

    def get_currency_precision(self):
        """
        获取所有交易对数量精度与价格精度
        :return:
        """
        exchange_info = self.request_client.get_exchange_info()
        result = exchange_info.symbol_list
        result_list = []
        for key, value in enumerate(result):
            self.logger.info(f"{key} {value}")
            if type(value) == dict:
                value = self.change_dict_to_symbol(value)
            result_list.append({"symbol": value.symbol, "quote_currency": value.quote_currency,
                                "base_currency": value.base_currency, "amount_precision": value.amount_precision,
                                "price_precision": value.price_precision, "symbol_partition": value.symbol_partition})
        return result_list

    def check_symbol_info(self, symbol_info):
        """
        检查交易对信息与数据库是否一致
        :param symbol_info:
        :return:
        """
        symbol_name = symbol_info["symbol"]
        result = self.precision_collection.find_one({"symbol": symbol_name}, {"_id": 0})
        if result is None:
            self.logger.info(f"{symbol_name} was not found, insert now! {symbol_info}")
            self.insert_symbol_info(symbol_info)
        else:
            for key, value in enumerate(self.symbol_key_list):
                if not result[value] == symbol_info[value]:
                    self.logger.info(f"{symbol_name} was changed! {symbol_info}")
                    self.update_symbol_info(symbol_info)

    def update_symbol_info(self, symbol_info):
        """
        根据交易对名称修改交易对信息
        :param symbol_info:
        :return:
        """
        self.precision_collection.update_one({"symbol": symbol_info["symbol"]}, {"$set": symbol_info})

    def insert_symbol_info(self, symbol_info):
        self.precision_collection.insert_one(symbol_info)

    @staticmethod
    def change_dict_to_symbol(symbol_dict):
        """
        将请求的交易对信息中dict类型的脏数据转换成Symbol类型
        :param symbol_dict:
        :return:
        """
        symbol = Symbol()
        symbol.symbol = symbol_dict['symbol']
        symbol.quote_currency = symbol_dict['quote_currency']
        symbol.base_currency = symbol_dict['base_currency']
        symbol.amount_precision = symbol_dict['amount_precision']
        symbol.price_precision = symbol_dict['price_precision']
        symbol.symbol_partition = symbol_dict['symbol_partition']
        return symbol


if __name__ == '__main__':
    market_handler = MarketHandler()
    market_handler.check_currency_precision()
