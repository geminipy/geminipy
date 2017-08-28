# Geminipy
A library for the Gemini bitcoin exchange API

Easily communicate with the Gemini Bitcoin exchange API without
having to deal with HTTP requests.


Requirements
============
Please get an API key from [https://exchange.gemini.com/settings/api](https://exchange.gemini.com/settings/api)


Installation
============

```shell
pip install geminipy
```

Example
=======

```python
from geminipy import Geminipy

# The connection defaults to the Gemini sandbox.
# Add 'live=True' to use the live exchange
con = Geminipy(api_key='your API key', secret_key='your secret key', live=True)
    
# public request
symbols = con.symbols()
    
# a Requests response is returned.
# So we can access the HTTP reponse code,
# the raw response content, or a json object
print symbols.status_code
print symbols.content
print symbols.json()
    
# authenticated request
order = con.new_order(amount='1', price='200',side='buy')
    
print order.json()
    
#send a heartbeat
con.heartbeat()
```

The required nonce is the current millisecond timestamp.
