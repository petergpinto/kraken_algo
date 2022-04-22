#!/usr/bin/env python
import krakenex
import mysql.connector
from dotenv import load_dotenv
import json
import os
from pprint import pprint

load_dotenv()

cnx = mysql.connector.connect(
	user=os.environ['MYSQL_DB_USER'],
	password=os.environ['MYSQL_DB_PASS'],
	host=os.environ['MYSQL_DB_HOST'],
	database=os.environ['MYSQL_DB_NAME']
)
cursor = cnx.cursor()

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

add_pair = "INSERT IGNORE INTO tradable_pairs (pair, base, altname, orderMin) VALUES (%s, %s, %s, %s)"


for pair, data in open_positions['result'].items():
	cursor.execute(add_pair, (pair, data['base'], data['altname'], data['ordermin']))


cnx.commit()

cursor.close()
cnx.close()
