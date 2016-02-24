import json
import requests

class geminipy:

    # set up default values
    base_url = "https://api.gemini.com"
    apikey = ""

    def __init__(self, key = ""):
        if key != "":
            self.apikey = key

    def symbols(self):
        url = self.base_url + '/v1/symbols'
        response = requests.get(url)
        return response.content

    def book(self, symbol, limit_bids = 0, limit_asks = 0):
        if symbol == "":
            return "Error: No symbol specified"

        url = self.base_url + '/v1/book/' + symbol
        params = {'limit_bids':limit_bids,'limit_asks':limit_asks}
        response = requests.get(url, params)
        return response.content

    def trades(self, symbol, since = 0, limit_trades = 50, include_breaks = 0):
        if symbol == "":
            return "Error: No symbol specified"

        url = self.base_url + '/v1/trades/' + symbol
        params = {'since':since,'limit_trades':limit_trades,'include_breaks':include_breaks}
        response = requests.get(url, params)
        return response.content

testcon = geminipy()

#response = testcon.symbols()
#print(response)

#response = testcon.book('btcusd')
#print(response)

response = testcon.trades('btcusd')
print(response)
