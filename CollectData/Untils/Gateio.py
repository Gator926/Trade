import random

from websocket import create_connection
import time
import json
import hmac
import base64
import hashlib


def get_sign(secret_key, message):
    h = hmac.new(secret_key, message, hashlib.sha512)
    return base64.b64encode(h.digest())


class GateWs:
    def __init__(self, url, api_key, secret_key):
        self.__url = url
        self.__api_key = api_key
        self.__secret_key = secret_key

    def gate_get(self, method, params):
        if params is None:
            params = []
        ws = create_connection(self.__url)
        data = {'id': self.generate_rand_number(), 'method': method, 'params': params}
        js = json.dumps(data)
        ws.send(js)
        return ws.recv()

    def gate_request(self, method, params):
        ws = create_connection(self.__url)
        nonce = int(time.time() * 1000)
        signature = get_sign(self.__secret_key, str(nonce))
        data = {'id': self.generate_rand_number(), 'method': 'server.sign', 'params': [self.__api_key, signature, nonce]}
        js = json.dumps(data)
        ws.send(js)
        if method == "server.sign":
            return ws.recv()
        else:
            ws.recv()
            data = {'id': self.generate_rand_number(), 'method': method, 'params': params}
            js = json.dumps(data)
            ws.send(js)
            return ws.recv()

    @staticmethod
    def generate_rand_number():
        return random.randint(0, 99999)
