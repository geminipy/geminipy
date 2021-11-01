# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import time

import requests

from geminipy.utils import _get_params


class Client:
    """Gemini API wrapper.

    Make public or authenticated requests according to the API documentation:
    https://docs.gemini.com/
    """

    def __init__(self,
                 apikey=None,
                 secret=None,
                 live=True,
                 nonce_mult=1000.0,
                 api_version=1,
                 timeout=15,
                 proxy=None):
        """Initialize the class.

        :param str apikey: your Gemini API key.
        :param str secret: your Gemini API secret key for signatures.
        :param float nonce_mult: a custom multiplier for nonce value.
        """
        # self._api_version = api_version
        if live:
            self._url = f'https://api.gemini.com'
        else:
            self._url = f'https://api.sandbox.gemini.com'
        self._proxy = {'http': proxy} if proxy else None
        self._timeout = timeout
        self._url = f'{self._url}/v{api_version}'
        self._apikey = apikey
        self._nonce_mult = nonce_mult
        self._secret = secret.encode()
        self._headers = {'X-GEMINI-APIKEY': self._apikey}

    # ================ Class private methods ================

    def _request(self, end_point, method=None, params=None):
        method = str(method or 'get').lower()

        request_args = {
            'url': f'{self._url}/{end_point}',
            'method': method,
            'timeout': self._timeout,
            'headers': self._headers
        }

        if params:
            if method in ('post',):
                params.update(
                    request=end_point,
                    nonce=self._nonce
                )
                json_params = json.dumps(params or {}).encode()
                payload = base64.b64encode(json_params)
                signature = hmac.new(self._secret, payload, hashlib.sha384)
                request_args.update(headers={
                    'X-GEMINI-PAYLOAD': payload,
                    'X-GEMINI-SIGNATURE': signature.hexdigest(),
                })
            else:
                request_args.update(params=params)

        if self._proxy:
            request_args.update(proxies=self._proxy)

        response = requests.request(**request_args)

        if response:
            if response.ok:
                return response.json()
            else:
                # elif any('json' in h for h in response.headers):
                try:
                    data = response.json()
                    return {'error': data}
                except json.JSONDecodeError:
                    return {
                        'error': {
                            'code': response.status_code,
                            'reason': response.reason,
                            'content': response.text
                        }
                    }
                except (requests.RequestException, requests.ConnectionError):
                    response.raise_for_status()

    @property
    def _nonce(self):
        """Return the current millisecond timestamp as the nonce.

        :return: current millisecond timestamp as the nonce
        """
        return f'{time.time() * self._nonce_mult:.0f}'




class GeminiPublic(Client):

    # ================ PUBLIC END POINTS ================
    def get_symbols(self):
        """Send a request to get trading symbols info."""
        return self._request('symbols')

    def get_ticker(self, symbol):
        """Send a request to get a trading symbol ticker info.

        :param symbol: symbol id to query (example: "btcusd")
        :return: trading symbol ticker info supplied by server.
        """
        return self._request(f'pubticker/{symbol}')

    def get_orderbook(self, symbol, limit_bids=0, limit_asks=0):
        """Send a request to get a symbol order book data.

        :param symbol: symbol id to query (example: "btcusd")
        :param limit_bids: limit the number of bids returned (default 0)
        :param limit_asks: limit the number of asks returned (default 0)
        :return: symbol order book info supplied by server.
        """
        params = _get_params(locals(), 'symbol')
        return self._request(f'book/{symbol}', params=params)

    def get_trades(self, symbol, since=0, limit_trades=50, include_breaks=0):
        """Send a request to get a symbol public trades.

        :param str symbol: symbol id to query (example: "btcusd")
        :param int since: return trades after this unix epoch (default 0)
        :param limit_trades: max number of trades to return (default 50).
        :param int include_breaks: whether to display broken trades (default 0)
        :return: supplied symbol public trades info supplied by server.
        """
        params = _get_params(locals(), 'symbol')
        return self._request(f'trades/{symbol}', params=params)

    def get_auction(self, symbol):
        """Send a request to get a symbol latest auction info.

        :param str symbol: symbol id to query (example: "btcusd")
        :return: supplied symbol latest auction supplied by server.
        """
        return self._request(f'auction/{symbol}')

    def get_auction_history(self, symbol, since=0, limit_auction_results=50, include_indicative=1):
        """Send a request to get a symbol auction history.

        :param str symbol: symbol id to query (example: "btcusd")
        :param since: only return auction events after this timestamp.
        :param limit_auction_results: max number of auction events to return.
        :param include_indicative: set to 0 to not include publication of indicative info.
        :return:
        """
        params = _get_params(locals(), 'symbol')
        return self._request(f'auction/{symbol}/history', params)


class Geminipy(GeminiPublic):
    """Gemini API wrapper.

    Make public or authenticated requests according to the API documentation:
    https://docs.gemini.com/
    """

    # ================ AUTHENTICATED ENDPOINTS ================

    def place_order(self, side, symbol, amount, price=None, client_order_id=None, type=None, options=None):
        """Send a request to place an order.

        :param str side: 'buy' or 'sell'
        :param str symbol: symbol id to query (example: "btcusd")
        :param float amount: symbol amount to order.
        :param float price: order price.
        :param client_order_id: an optional custom order indetifier.
        :param type: order type (default 'exchange limit')
        :param options:
        return:
        """
        params = _get_params(locals(), 'amount', 'price')
        params.update(amount=f'{amount}')
        return self._request('order/new', 'post', params)

    def cancel_order(self, order_id):
        """Send a request to cancel an order.

        :param str order_id: order id to cancel.
        :return:
        """
        params = _get_params(locals())
        return self._request('order/cancel', 'post', params)

    def cancel_session(self):
        """Send a request to cancel all session orders.

        :return:
        """
        return self._request('order/cancel/session', 'post')

    def cancel_all(self):
        """Send a request to cancel all orders.

        :return:
        """
        return self._request('order/cancel/all', 'post')

    def get_order_status(self, order_id):
        """Send a request to get an order current status.

        :param str order_id: the order id to get information on.
        :return:
        """
        params = _get_params(locals())
        return self._request('order/status', 'post', params)

    def get_active_orders(self):
        """Send a request to get active orders.

        :return:
        """
        return self._request('orders', 'post')

    def get_past_trades(self, symbol, limit_trades=50, timestamp=0):
        """Send a symbol trades history request.

        :param str symbol: symbol id to query (example: "btcusd")
        :param limit_trades: max number of trades to return (default 50)
        :param timestamp: return trades after supplied unix epoch (default 0)
        :return:
        """
        params = _get_params(locals())
        return self._request('mytrades', 'post', params)

    def get_trade_volume(self):
        """Send a request to get your trade volume."""
        return self._request('tradevolume', 'post')

    def get_balances(self):
        """Send an account balance request.

        :return:
        """
        return self._request('balances', 'post')

    def new_deposit_address(self, currency, label=None):
        """Send a request to generate a new cryptocurrency deposit address.

        :param str currency: crypto currency ID (example: btc)
        :param str label: optional label for the deposit address
        :return:
        """
        params = _get_params(locals(), 'currency')
        return self._request(f'deposit/{currency}/newAddress', 'post', params)

    def get_notional_balances(self, currency, account=None):
        """Get approved addresses for supplied network and account (if supplied)

        :param str currency: currency to get balance for.
        :param str account: account name (example: primary)
        :return:
        """
        params = _get_params(locals(), 'currency')
        return self._request(f'notionalbalances/{currency}', 'post', params)

    def remove_approved_address(self, network, address, account=None):
        """Get approved addresses for supplied network and account (if supplied)

        :param str network: accepted values: bitcoin, ethereum, bitcoincash, litecoin, zcash, filecoin, dogecoin, tezos
        :param str address: address to remove.
        :param str account: account name (example: primary)
        :return:
        """
        params = _get_params(locals(), 'network')
        return self._request(f'approvedAddresses/account/{network}/remove', 'post', params)

    def request_approved_address(self, network, address, label=None, account=None):
        """Get approved addresses for supplied network and account (if supplied)

        :param str network: accepted values: bitcoin, ethereum, bitcoincash, litecoin, zcash, filecoin, dogecoin, tezos
        :param str address: address to remove.
        :param str label: a label to identify the supplied address.
        :param str account: account name (example: primary)
        :return:
        """
        params = _get_params(locals(), 'network')
        return self._request(f'approvedAddresses/{network}/request', 'post', params)

    def get_fees(self):
        """Send a request to get fees and notional volume."""
        self._request('notionalvolume', 'post')

    def get_earn_balance(self, account=None):
        """Send an account earn balance request.

        :param str account: account name (example: primary)
        :return:
        """
        params = _get_params(locals())
        return self._request('balances/earn', 'post', params)

    def get_account_details(self):
        """Send a request to get account details related to supplied API keys.

        :return:
        """
        return self._request('account', 'post')

    def get_heartbeat(self):
        """Send a heartbeat message.

        :return:
        """
        return self._request('heartbeat', 'post')
