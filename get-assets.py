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
k.load_key(os.environ['KRAKEN_API_KEY'])

asset_classes = ['currency', 'forex']

# prepare request
req_data = {'docalcs': 'true'}

add_asset = "INSERT IGNORE INTO assets (asset, altname, decimals, displayDecimals, class) VALUES (%s, %s, %s, %s ,%s)"
update_asset = "UPDATE assets SET decimals=%s, displayDecimals=%s, altname=%s WHERE asset=%s"

for asset_class in asset_classes:
	req_data = {'docalcs': 'true', 'aclass':asset_class}
	assets = k.query_public('Assets', req_data)

	#Attempt to insert every asset into the database, INSERT IGNORE will skip already existing assets
	for asset, data in assets['result'].items():
		cursor.execute(add_asset, (asset, data['altname'], data['decimals'], data['display_decimals'], data['aclass']))	
	cnx.commit()

	#For assets that already exist in the database, update values to make sure that they are consistent API
	for asset, data in assets['result'].items():
		cursor.execute(update_asset, (data['decimals'], data['display_decimals'], data['altname']))
	cnx.commit()

cursor.close()
cnx.close()
