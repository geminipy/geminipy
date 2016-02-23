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
