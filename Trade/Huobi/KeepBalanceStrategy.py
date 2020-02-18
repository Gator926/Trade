import time
from Trade.Huobi import BaseStrategy
from Util.FormatNumber import retain_decimals
from huobi.model import *
from huobi import RequestClient
from Model.Action import Action
from Model.TradeLimit import TradeLimit
from LogHandler.MailHandler import MailHandler


class KeepBalanceStrategy(BaseStrategy, MailHandler):
    """
    动态平衡策略
    """

    def __init__(self):
        BaseStrategy.__init__(self)
        self.request_client = RequestClient(api_key=self.get_config_value("huobi", "api_key"),
                                            secret_key=self.get_config_value("huobi", "secret_key"))
        self.strategy = 'KeepBalance'

    def signal(self):
        balance_dict = self.get_account_balance()
        for key, value in enumerate(balance_dict):
            if float(balance_dict[value]["amount"]) * 1.03 < float(balance_dict[value]["dollar"]):
                self.buy(value, amount=balance_dict[value]["amount"], dollar=balance_dict[value]["dollar"])
            elif float(balance_dict[value]["dollar"]) * 1.03 < float(balance_dict[value]["amount"]):
                self.sell(value, amount=balance_dict[value]["amount"], dollar=balance_dict[value]["dollar"],
                          price=balance_dict[value]["price"])
            else:
                self.logger.info(f"当前持有{value}合计金额: {balance_dict[value]['amount']}, 对标美元: "
                                 f"{balance_dict[value]['dollar']}, 小于阈值不触发交易, "
                                 f"买入阈值: {retain_decimals(float(balance_dict[value]['dollar']) / 1.05, 2)}, "
                                 f"卖出阈值: {retain_decimals(float(balance_dict[value]['dollar']) * 1.05, 2)}")

    def buy(self, symbol_name, **kwargs):
        self.trade_lock(symbol_name, self.strategy)
        try:
            assert kwargs['dollar'] >= kwargs['amount']
            buy_dollar = retain_decimals((float(kwargs['dollar']) - float(kwargs['amount'])) / 2, 2)
            if float(buy_dollar) >= TradeLimit.USDT:
                # 买入
                order_id = self.request_client.create_order(symbol_name + 'usdt', AccountType.SPOT,
                                                            OrderType.BUY_MARKET, buy_dollar, None)
                self.update_balance_and_dollar(order_id, Action.BUY, symbol_name, buy_dollar=buy_dollar)
                self.send_mail("触发买入信号", f"动态平衡策略触发买入{buy_dollar}的{symbol_name}")
            else:
                self.logger.warning(f"当前欲买入{buy_dollar}美金的{symbol_name}, 不满足最低交易限制")
        except AssertionError:
            self.logger.error(f"AssertionError, symbol={symbol_name}, amount={kwargs['amount']}, "
                              f"dollar={kwargs['dollar']}")
        finally:
            self.trade_unlock(symbol_name, self.strategy)

    def sell(self, symbol_name, **kwargs):
        self.trade_lock(symbol_name, self.strategy)
        try:
            assert kwargs['amount'] > kwargs['dollar']

            # 获取交易数目精度
            precision = self.precision_collection.find_one({"symbol": symbol_name + "usdt"}, {"amount_precision": 1})
            amount_precision = float(precision['amount_precision'])

            # 计算欲卖出的数目
            sell_currency = retain_decimals(
                (float(kwargs['amount']) - float(kwargs['dollar'])) / 2 / float(kwargs['price']), amount_precision)

            if float(sell_currency) > TradeLimit.BTC:
                order_id = self.request_client.create_order(symbol_name + 'usdt', AccountType.SPOT,
                                                            OrderType.SELL_MARKET, sell_currency, None)
                self.update_balance_and_dollar(order_id, Action.SELL, symbol_name)
                self.send_mail("触发卖出信号", f"动态平衡策略触发卖出{sell_currency}的{symbol_name}")
            else:
                self.logger.warning(f"当前欲卖出{sell_currency}美金的{symbol_name}, 不满足最低交易限制")
        except AssertionError:
            self.logger.error(f"AssertionError, symbol={symbol_name}, amount={kwargs['amount']}, "
                              f"dollar={kwargs['dollar']}")
        finally:
            self.trade_unlock(symbol_name, self.strategy)

    def update_balance_and_dollar(self, order_id, action, symbol_name, **kwargs):
        order_detail = self.request_client.get_order("symbol", order_id)

        # 验证订单是否执行完成
        while not order_detail.state == OrderState.FILLED:
            time.sleep(1)
            self.logger.info(f"{order_id}还未执行完成, 休眠1秒等待执行完成")
            order_detail = self.request_client.get_order("symbol", order_id)

        # mongodb中减去已使用的美金
        result = self.keep_balance_collection.find_one({"symbol": symbol_name})
        dollar = float(result['amount'])
        if action == 'BUY':
            dollar -= float(kwargs['buy_dollar'])
        # mongodb中加上卖出获得的美金
        elif action == 'SELL':
            dollar += float(order_detail.filled_cash_amount)

        # 格式化美金数
        dollar = retain_decimals(dollar, 2)

        # mongodb更新操作
        self.keep_balance_collection.update_one({"symbol": symbol_name}, {"$set": {"amount": dollar}})
        self.logger.info(f"{symbol_name}美金数置为: {dollar}")

    def get_account_balance(self):
        """
        获取余额大于0的交易对
        :return:
        """
        balances = self.request_client.get_account_balance()
        balance_dict = {}
        for key, value in enumerate(balances[0].balances):
            if value.balance > 0 and value.currency != 'usdt':
                if not self.check_trade_lock_exist(value.currency, self.strategy):
                    price, amount = self.get_account_amount(value.currency, value.balance)
                    if float(amount) >= 1:
                        dollar = self.get_mongodb_dollar(value.currency, amount)
                        balance_dict[value.currency] = {"balance": str(value.balance), "price": str(price),
                                                        "amount": str(amount), "dollar": dollar}
        self.logger.debug(balance_dict)
        return balance_dict

    def get_account_amount(self, symbol_name, symbol_balance):
        price = self.get_price(symbol_name + "usdt")
        amount = str(float(symbol_balance) * float(price))
        amount = retain_decimals(amount, 2)
        return price, amount

    def get_mongodb_dollar(self, symbol_name, symbol_amount):
        result = self.keep_balance_collection.find_one({"symbol": symbol_name})
        if result is None:
            self.keep_balance_collection.insert_one({"symbol": symbol_name, "amount": str(symbol_amount)})
            return symbol_amount
        else:
            return result['amount']

    def get_price(self, symbol_name):
        """
        获取当前交易对价格
        :param symbol_name:
        :return:
        """
        current_prices = self.request_client.get_latest_candlestick(symbol=symbol_name,
                                                                    interval=CandlestickInterval.DAY1, size=1)
        return current_prices[0].close


if __name__ == '__main__':
    keep_balance_strategy = KeepBalanceStrategy()
    keep_balance_strategy.signal()
