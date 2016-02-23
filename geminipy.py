import json
import requests

class geminipy:

    # set up default values
    base_url = "https://api.gemini.com"
    apikey = ""

    def __init__(self, url = ""):
        if url != "":
            self.base_url = url

    def symbols(self):
        url = self.base_url + '/v1/symbols'
        response = requests.get(url)
        return response.content

    def book(self, symbol):
        if symbol == "":
            return "Error: No symbol specified"

        url = self.base_url + '/v1/book/' + symbol
        response = requests.get(url)
        return response.content
        
    def trades(self, symbol, since="", limit_trades=50, include_breaks=False):
        if symbol == "":
            return "Error: No symbol specified"

        url = self.base_url + '/v1/trades/' + symbol
        print url
        params = {'since':since,'limit_trades':limit_trades,'include_breaks':include_breaks}
        response = requests.get(url, params)
        return response.content

testcon = geminipy()

symbolsresponse = testcon.symbols()
print(symbolsresponse)

#bookresponse = testcon.book('btcusd')
#print(bookresponse)

#tradesresponse = testcon.trades('btcusd')
#print(tradesresponse)
