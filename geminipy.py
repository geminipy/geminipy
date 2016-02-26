import time
import json
import hmac
import base64
import hashlib
import requests

class geminipy:

    live_url = 'https://api.gemini.com'
    sandbox_url = 'https://api.sandbox.gemini.com'
    base_url = sandbox_url
    apikey = ''
    secretkey = ''

    def __init__(self, live = False):
        if live:
            self.base_url = self.live_url

    # public requests
    def symbols(self):
        url = self.base_url + '/v1/symbols'
        response = requests.get(url)
        return response.content

    def book(self, symbol = 'btcusd', limit_bids = 0, limit_asks = 0):
        url = self.base_url + '/v1/book/' + symbol
        params = {'limit_bids':limit_bids,'limit_asks':limit_asks}
        response = requests.get(url, params)
        return response.content

    def trades(self, symbol = 'btcusd', since = 0, limit_trades = 50, include_breaks = 0):
        url = self.base_url + '/v1/trades/' + symbol
        params = {'since':since,'limit_trades':limit_trades,'include_breaks':include_breaks}
        response = requests.get(url, params)
        return response.content

    # authenticated requests
    def neworder(self, amount, price, side, client_order_id = None, symbol = 'btcusd', type = 'exchange limit'):
        request = '/v1/order/new'
        url = self.base_url + request
        params = {
            "request": request,
            "nonce": self.get_nonce(),
            "symbol": symbol,
            "amount": amount,
            "price": price,
            "side": side,
            "type": type
        }

        if client_order_id is not None:
            params['client_order_id'] = client_order_id

        return requests.post(url, headers=self.prepare(params))

    def cancelorder(self, order_id):
        request = '/v1/order/cancel'
        url = self.base_url + request
        params = {
            "request": request,
            "nonce": self.get_nonce(),
            "order_id": order_id
        }

        return requests.post(url, headers=self.prepare(params))

    def cancelsession(self):
        request = '/v1/order/cancel/session'
        url = self.base_url + request
        params = {
            "request": request,
            "nonce": self.get_nonce()
        }

        return requests.post(url, headers=self.prepare(params))

    def cancelall(self):
        request = '/v1/order/cancel/all'
        url = self.base_url + request
        params = {
            "request": request,
            "nonce": self.get_nonce()
        }

        return requests.post(url, headers=self.prepare(params))

    def orderstatus(self, order_id):
        request = '/v1/order/status'
        url = self.base_url + request
        params = {
            "request": request,
            "nonce": self.get_nonce(),
            "order_id": order_id
        }

        return requests.post(url, headers=self.prepare(params))

    def activeorders(self):
        request = '/v1/orders'
        url = self.base_url + request
        params = {
            "request": request,
            "nonce": self.get_nonce()
        }

        return requests.post(url, headers=self.prepare(params))

    def pasttrades(self, symbol = 'btcusd', limit_trades = 50, timestamp = 0):
        request = '/v1/mytrades'
        url = self.base_url + request
        params = {
            "request": request,
            "nonce": self.get_nonce(),
            "symbol": symbol,
            "limit_trades": limit_trades,
            "timestamp": timestamp
        }

        return requests.post(url, headers=self.prepare(params))

    def balances(self):
        request = '/v1/balances'
        url = self.base_url + request
        params = {
            "request": request,
            "nonce": self.get_nonce()
        }

        return requests.post(url, headers=self.prepare(params))

    def heartbeat(self):
        request = '/v1/heartbeat'
        url = self.base_url + request
        params = {
            "request": request,
            "nonce": self.get_nonce()
        }

        return requests.post(url, headers=self.prepare(params))

    def get_nonce(self):
        return int(round(time.time() * 1000))

    def prepare(self, params):
        jsonparams = json.dumps(params)
        payload = base64.b64encode(jsonparams)
        signature = hmac.new(self.secretkey, payload, hashlib.sha384).hexdigest()

        return {"X-GEMINI-APIKEY":self.apikey, "X-GEMINI-PAYLOAD":payload, "X-GEMINI-SIGNATURE":signature}
