import time
import json
import hmac
import base64
import hashlib
import requests


class Geminipy(object):

    live_url = 'https://api.gemini.com'
    sandbox_url = 'https://api.sandbox.gemini.com'
    base_url = sandbox_url
    api_key = ''
    secret_key = ''

    def __init__(self, api_key='', secret_key='', live=False):
        self.api_key = api_key
        self.secret_key = secret_key

        if live:
            self.base_url = self.live_url

    # public requests
    def symbols(self):
        """
        Send a request to get all trading symbols and return the response.
        """
        url = self.base_url + '/v1/symbols'
        response = requests.get(url)
        return response.content

    def book(self, symbol='btcusd', limit_bids=0, limit_asks=0):
        """
        Send a request to get the public order book and return the response.
        """
        url = self.base_url + '/v1/book/' + symbol
        params = {
            'limit_bids': limit_bids,
            'limit_asks': limit_asks
        }
        response = requests.get(url, params)
        return response.content

    def trades(self, symbol='btcusd', since=0, limit_trades=50,
               include_breaks=0):
        """
        Send a request to get all public trades and return the response.
        """
        url = self.base_url + '/v1/trades/' + symbol
        params = {
            'since': since,
            'limit_trades': limit_trades,
            'include_breaks': include_breaks
        }
        response = requests.get(url, params)
        return response.content

    # authenticated requests
    def new_order(self, amount, price, side, client_order_id=None,
                  symbol='btcusd', type='exchange limit'):
        """
        Send a request to place an order and return the response.
        """
        request = '/v1/order/new'
        url = self.base_url + request
        params = {
            'request': request,
            'nonce': self.get_nonce(),
            'symbol': symbol,
            'amount': amount,
            'price': price,
            'side': side,
            'type': type
        }

        if client_order_id is not None:
            params['client_order_id'] = client_order_id

        return requests.post(url, headers=self.prepare(params))

    def cancel_order(self, order_id):
        """
        Send a request to cancel an order and return the response.
        """
        request = '/v1/order/cancel'
        url = self.base_url + request
        params = {
            'request': request,
            'nonce': self.get_nonce(),
            'order_id': order_id
        }

        return requests.post(url, headers=self.prepare(params))

    def cancel_session(self):
        """
        Send a request to cancel all session orders and return the response.
        """
        request = '/v1/order/cancel/session'
        url = self.base_url + request
        params = {
            'request': request,
            'nonce': self.get_nonce()
        }

        return requests.post(url, headers=self.prepare(params))

    def cancel_all(self):
        """
        Send a request to cancel all orders and return the response.
        """
        request = '/v1/order/cancel/all'
        url = self.base_url + request
        params = {
            'request': request,
            'nonce': self.get_nonce()
        }

        return requests.post(url, headers=self.prepare(params))

    def order_status(self, order_id):
        """
        Send a request to get an order status and return the response.
        """
        request = '/v1/order/status'
        url = self.base_url + request
        params = {
            'request': request,
            'nonce': self.get_nonce(),
            'order_id': order_id
        }

        return requests.post(url, headers=self.prepare(params))

    def active_orders(self):
        """
        Send a request to get active orders and return the response.
        """
        request = '/v1/orders'
        url = self.base_url + request
        params = {
            'request': request,
            'nonce': self.get_nonce()
        }

        return requests.post(url, headers=self.prepare(params))

    def past_trades(self, symbol='btcusd', limit_trades=50, timestamp=0):
        """
        Send a trade history request and return the response.
        """
        request = '/v1/mytrades'
        url = self.base_url + request
        params = {
            'request': request,
            'nonce': self.get_nonce(),
            'symbol': symbol,
            'limit_trades': limit_trades,
            'timestamp': timestamp
        }

        return requests.post(url, headers=self.prepare(params))

    def balances(self):
        """
        Send an account balance request and Return the response.
        """
        request = '/v1/balances'
        url = self.base_url + request
        params = {
            'request': request,
            'nonce': self.get_nonce()
        }

        return requests.post(url, headers=self.prepare(params))

    def heartbeat(self):
        """
        Send a heartbeat message and return the response.
        """
        request = '/v1/heartbeat'
        url = self.base_url + request
        params = {
            'request': request,
            'nonce': self.get_nonce()
        }

        return requests.post(url, headers=self.prepare(params))

    def get_nonce(self):
        """
        Return the current millisecond timestamp as the nonce.
        """
        return int(round(time.time() * 1000))

    def prepare(self, params):
        """
        Prepare and return the required HTTP headers.

        Base 64 encode the parameters, sign it with the secret key,
        create the HTTP headres, and return the whole payload.
        """
        jsonparams = json.dumps(params)
        payload = base64.b64encode(jsonparams)
        signature = hmac.new(self.secret_key, payload,
                             hashlib.sha384).hexdigest()

        return {'X-GEMINI-APIKEY': self.api_key,
                'X-GEMINI-PAYLOAD': payload,
                'X-GEMINI-SIGNATURE': signature}
