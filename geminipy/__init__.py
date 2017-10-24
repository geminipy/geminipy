"""
This module contains a class to make requests to the Gemini API.

Author: Mike Marzigliano
"""
import time
import json
import hmac
import base64
import hashlib
import requests


class Geminipy(object):
    """
    A class to make requests to the Gemini API.

    Make public or authenticated requests according to the API documentation:
    https://docs.gemini.com/
    """

    live_url = 'https://api.gemini.com'
    sandbox_url = 'https://api.sandbox.gemini.com'
    base_url = sandbox_url
    api_key = ''
    secret_key = ''

    def __init__(self, api_key='', secret_key='', live=False):
        """
        Initialize the class.

        Arguments:
        api_key -- your Gemini API key
        secret_key -- your Gemini API secret key for signatures
        live -- use the live API? otherwise, use the sandbox (default False)
        """
        self.api_key = api_key
        self.secret_key = secret_key

        if live:
            self.base_url = self.live_url

    # public requests
    def symbols(self):
        """Send a request for all trading symbols, return the response."""
        url = self.base_url + '/v1/symbols'

        return requests.get(url)

    def book(self, symbol='btcusd', limit_bids=0, limit_asks=0):
        """
        Send a request to get the public order book, return the response.

        Arguments:
        symbol -- currency symbol (default 'btcusd')
        limit_bids -- limit the number of bids returned (default 0)
        limit_asks -- limit the number of asks returned (default 0)
        """
        url = self.base_url + '/v1/book/' + symbol
        params = {
            'limit_bids': limit_bids,
            'limit_asks': limit_asks
        }

        return requests.get(url, params)

    def trades(self, symbol='btcusd', since=0, limit_trades=50,
               include_breaks=0):
        """
        Send a request to get all public trades, return the response.

        Arguments:
        symbol -- currency symbol (default 'btcusd')
        since -- only return trades after this unix timestamp (default 0)
        limit_trades -- maximum number of trades to return (default 50).
        include_breaks -- whether to display broken trades (default False)
        """
        url = self.base_url + '/v1/trades/' + symbol
        params = {
            'since': since,
            'limit_trades': limit_trades,
            'include_breaks': include_breaks
        }

        return requests.get(url, params)

    # authenticated requests
    def new_order(self, amount, price, side, client_order_id=None,
                  symbol='btcusd', type='exchange limit', options=None):
        """
        Send a request to place an order, return the response.

        Arguments:
        amount -- quoted decimal amount of BTC to purchase
        price -- quoted decimal amount of USD to spend per BTC
        side -- 'buy' or 'sell'
        client_order_id -- an optional client-specified order id (default None)
        symbol -- currency symbol (default 'btcusd')
        type -- the order type (default 'exchange limit')
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

        if options is not None:
            params['options'] = options

        return requests.post(url, headers=self.prepare(params))

    def cancel_order(self, order_id):
        """
        Send a request to cancel an order, return the response.

        Arguments:
        order_id - the order id to cancel
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
        """Send a request to cancel all session orders, return the response."""
        request = '/v1/order/cancel/session'
        url = self.base_url + request
        params = {
            'request': request,
            'nonce': self.get_nonce()
        }

        return requests.post(url, headers=self.prepare(params))

    def cancel_all(self):
        """Send a request to cancel all orders, return the response."""
        request = '/v1/order/cancel/all'
        url = self.base_url + request
        params = {
            'request': request,
            'nonce': self.get_nonce()
        }

        return requests.post(url, headers=self.prepare(params))

    def order_status(self, order_id):
        """
        Send a request to get an order status, return the response.

        Arguments:
        order_id -- the order id to get information on
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
        """Send a request to get active orders, return the response."""
        request = '/v1/orders'
        url = self.base_url + request
        params = {
            'request': request,
            'nonce': self.get_nonce()
        }

        return requests.post(url, headers=self.prepare(params))

    def past_trades(self, symbol='btcusd', limit_trades=50, timestamp=0):
        """
        Send a trade history request, return the response.

        Arguements:
        symbol -- currency symbol (default 'btcusd')
        limit_trades -- maximum number of trades to return (default 50)
        timestamp -- only return trades after this unix timestamp (default 0)
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
        """Send an account balance request, return the response."""
        request = '/v1/balances'
        url = self.base_url + request
        params = {
            'request': request,
            'nonce': self.get_nonce()
        }

        return requests.post(url, headers=self.prepare(params))

    def heartbeat(self):
        """Send a heartbeat message, return the response."""
        request = '/v1/heartbeat'
        url = self.base_url + request
        params = {
            'request': request,
            'nonce': self.get_nonce()
        }

        return requests.post(url, headers=self.prepare(params))

    def get_nonce(self):
        """Return the current millisecond timestamp as the nonce."""
        return int(round(time.time() * 1000))

    def prepare(self, params):
        """
        Prepare, return the required HTTP headers.

        Base 64 encode the parameters, sign it with the secret key,
        create the HTTP headers, return the whole payload.

        Arguments:
        params -- a dictionary of parameters
        """
        jsonparams = json.dumps(params)
        payload = base64.b64encode(jsonparams.encode())
        signature = hmac.new(self.secret_key.encode(), payload,
                             hashlib.sha384).hexdigest()

        return {'X-GEMINI-APIKEY': self.api_key,
                'X-GEMINI-PAYLOAD': payload,
                'X-GEMINI-SIGNATURE': signature}
