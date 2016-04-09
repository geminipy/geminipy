# Geminipy
A library for the Gemini bitcoin exchange API

Easily communicate with the Gemini Bitcoin exchange API without
having to deal with HTTP requests.


Installation
============

Just download geminipy.py

Example
=======

    from geminipy import Geminipy
    
    con = Geminipy(api_key='your API key', secret_key='your secret key')
    
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

The required nonce is the current millisecond timestamp.

Dependencies
============

requests >=2.9.1

    sudo pip install requests --upgrade
    
