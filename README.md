# Geminipy
A library for the Gemini bitcoin exchange API.

Easily communicate with the Gemini Bitcoin exchange API without
having to deal with HTTP requests.


Requirements
============
A Python 3 interpreter (versions < 3.8 not tested)
Please get your API keys from [https://exchange.gemini.com/settings/api](https://exchange.gemini.com/settings/api)


Installation
============

```shell
pip install "git+https://github.com/pl0mo/geminipy"
```

Example
=======

```python
from geminipy import Geminipy

# Set live param to False to use Gemini testing (sandbox) enviroment.
api = Geminipy(apikey='your API key', secret='your secret key')
    
# public request
symbols = api.get_symbols()

print(symbols)
    
# authenticated request
order = api.place_order('btcusd', amount=1, price=200.0, side='buy',)
    
print(order)
    
#send a heartbeat
api.get_heartbeat()
```

The required nonce is the current millisecond timestamp.
