#!/usr/bin/env python
import krakenex
from pprint import pprint

# configure api
k = krakenex.API()
k.load_key('combined.key')

# prepare request
req_data = {'docalcs': 'true'}

# query servers
start = k.query_public('Time')
open_positions = k.query_public('AssetPairs', req_data)
end = k.query_public('Time')
latency = end['result']['unixtime'] - start['result']['unixtime']

# parse result
#b, c = 0, 0

pprint(open_positions)

'''
for order in open_positions['result']:
    coin = order["pair"]
    if coin == 'XETHZUSD':
        b += (float(order['vol']))
    elif coin == 'XXBTZUSD':
        c += (float(order['vol']))

n_errors = len(open_positions['error'])
total = len(open_positions['result'])

msg = """
error counts: {n_errors}
latency: {latency}
open orders
    eth: {b}
    btc: {c}
    total: {total}
"""
print(msg.format(n_errors=n_errors, total=total, b=b, c=c, latency=latency))
'''
