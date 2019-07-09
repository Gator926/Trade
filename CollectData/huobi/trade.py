from websocket import create_connection
import gzip
import time
import json

if __name__ == '__main__':
    while (1):
        try:
            ws = create_connection("wss://api.huobi.pro/ws")
            break
        except:
            print('connect ws error,retry...')
            time.sleep(5)
    # 请求 KLine 数据
    tradeStr = """{"req": "market.btcusdt.kline.1min","id": "btcusdt", "from": 1325347201, "to": 1344579200}"""
    print(tradeStr)
    ws.send(tradeStr)
    trade_id = ''
    while 1:
        compressData = ws.recv()
        result = gzip.decompress(compressData).decode('utf-8')
        if result[:7] == '{"ping"':
            ts = result[8:21]
            pong = '{"pong":' + ts + '}'
            ws.send(pong)
        else:
            print(json.loads(result))
