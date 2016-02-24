import json
import requests

class geminipy:

    live_url = "https://api.gemini.com"
    sandbox_url = "https://api.sandbox.gemini.com"
    base_url = sandbox_url

    def __init__(self, live = False):
        if live:
            base_url = self.live_url

    # public requests
    def symbols(self):
        url = self.base_url + '/v1/symbols'
        response = requests.get(url)
        return response.content

    def book(self, symbol = "btcusd", limit_bids = 0, limit_asks = 0):
        if symbol == "":
            return "Error: No symbol specified"

        url = self.base_url + '/v1/book/' + symbol
        params = {'limit_bids':limit_bids,'limit_asks':limit_asks}
        response = requests.get(url, params)
        return response.content

    def trades(self, symbol = "btcusd", since = 0, limit_trades = 50, include_breaks = 0):
        if symbol == "":
            return "Error: No symbol specified"

        url = self.base_url + '/v1/trades/' + symbol
        params = {'since':since,'limit_trades':limit_trades,'include_breaks':include_breaks}
        response = requests.get(url, params)
        return response.content

        
