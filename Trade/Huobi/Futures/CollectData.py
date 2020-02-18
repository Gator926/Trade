import json

from websocket import create_connection
from Model.FutureType import FutureType
from IO.File import FileReadAndWrite
from threading import Thread
from Util.Time import millisecond_timestamp_to_date
import gzip
import time


class CollectFuturesData:
    def __init__(self, future_type: str):
        self.future_type = future_type
        self.url = "wss://www.hbdm.com/ws"
        self.tradeStr_market_depth = '{"sub": "market.BTC_' + self.future_type + '.depth.step0", "id": "id9"}'
        self.tradeStr_kline_req = '{"req": "market.BTC_' + self.future_type + '.kline.1min", "id": "id4"}'
        while True:
            try:
                self.ws = create_connection("wss://www.hbdm.com/ws")
                break
            except Exception:
                print('connect ws error,retry...')
                time.sleep(5)

    def write_to_file(self, result: dict):
        date = millisecond_timestamp_to_date(int(result["ts"]))
        FileReadAndWrite.write_with_append("/root/price/future/BTC_" + self.future_type + "_" + date + '.txt',
                                           str(result) + "\n")

    def book_data(self):
        self.ws.send(self.tradeStr_market_depth)
        while True:
            compress_data = self.ws.recv()
            result = gzip.decompress(compress_data).decode('utf-8')
            ts = result[8:21]
            if 'ping' in result:
                pong = '{"pong":' + ts + '}'
                self.ws.send(pong)
            else:
                result = json.loads(result)
                self.write_to_file(result)


if __name__ == '__main__':
    cw = CollectFuturesData(FutureType.CW)
    nw = CollectFuturesData(FutureType.NW)
    cq = CollectFuturesData(FutureType.CQ)
    thread_cw = Thread(target=cw.book_data)
    thread_nw = Thread(target=nw.book_data)
    thread_cq = Thread(target=cq.book_data)
    thread_cw.start()
    thread_nw.start()
    thread_cq.start()
