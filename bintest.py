# -*- coding: utf-8 -*-
import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance.enums import *


# init
api_key = ''
api_secret =''
client = Client(api_key, api_secret, testnet=True)
client.API_URL = 'https://testnet.binance.vision/api'

# Initialize the client
client = Client(api_key, api_secret)

# Get the account balances
try:
    account_info = client.get_account()
    balances = account_info['balances']
    print("Spot Balances:")
    spot_total = 0
    for balance in balances:
        if float(balance['free']) > 0 or float(balance['locked']) > 0:
            if balance['asset'] == 'USDT':
                spot_total += float(balance['free']) + float(balance['locked'])
            print("{}: {}".format(balance['asset'], balance['free']))
    print("Spot balance: {:.2f} USDT".format(spot_total))

    futures_symbol = []
    exchange_info = client.futures_exchange_info()
    for s in exchange_info["symbols"]:
        if s["contractType"] == "PERPETUAL":
            futures_symbol.append(s["symbol"])
    print("\nFutures Balances:")
    futures_total = 0
    futures_account_info = client.futures_account()
    futures_balances = futures_account_info['assets']
    for balance in futures_balances:
        if float(balance['marginBalance']) > 0:
            futures_total += float(balance['marginBalance'])
            print("{}: {}".format(balance['asset'], balance['marginBalance']))
    print("Futures balance: {:.2f} USDT".format(futures_total))
    print("Futures trading is allowed for these symbols: {}".format(futures_symbol))
except BinanceAPIException as e:
    print(e)
