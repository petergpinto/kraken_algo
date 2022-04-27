#!/usr/bin/env python
import krakenex
import mysql.connector
from dotenv import load_dotenv
import json
import os
from pprint import pprint
import time

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
k.load_key(os.environ['KRAKEN_API_KEY'])

#Possible intervals to request
oneMinute=1
fiveMinutes=5
fifteenMinutes=15
thirtyMinutes=30
oneHour=60
fourHours=240
oneDay=1440
oneWeek=10080 
fifteenDays=21600


query="SELECT * FROM tradable_pairs"

cursor.execute(query)

#Response format
#"time": 1625405820000,
#"open": "35399.75000000000",
#"high": "35407.25000000000",
#"low": "35388.50000000000",
#"close": "35390.25000000000",
# ?? unknown value ??
# volume?
# trades?

insert_ohlc="INSERT IGNORE INTO ohlc_data (pairId, timestamp, open, high, low, close, volume, trades) VALUES (%s, FROM_UNIXTIME(%s), %s, %s, %s, %s, %s, %s)"
latest_timestamp="SELECT timestamp from ohlc_data WHERE pairId=%s order by timestamp desc limit 1"

tradable = cursor.fetchall()

while True:
	print("Starting OHLC data collection...")
	for id, pair, base, altname, orderMin, doTrade in tradable:
		cursor.execute(latest_timestamp, (id, ) )
		timestamp = cursor.fetchall()[0][0].timestamp()
		req_data = {'docalcs': 'true', 'pair':pair, 'interval':oneMinute, 'since' : int(timestamp) }
		OHLC_data = k.query_public('OHLC', req_data)
		for timestamp,open,high,low,close,unknown,volume,trades in OHLC_data['result'][pair]:
			cursor.execute(insert_ohlc, (id, timestamp, open, high, low, close, volume, trades))
		cnx.commit()
	print("Fetched all, sleeping for 5 minutes...")
	time.sleep(300)

cnx.commit()
cnx.close()
