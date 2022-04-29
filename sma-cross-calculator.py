#!/usr/bin/env python
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert
from dotenv import load_dotenv
import json
import os
from pprint import pprint
import numpy as np
import pandas as pd

load_dotenv()

con_str = "mysql+pymysql://"+os.environ['MYSQL_DB_USER']+":"+os.environ['MYSQL_DB_PASS']+"@"+os.environ['MYSQL_DB_HOST']+"/"+os.environ['MYSQL_DB_NAME']
conn = create_engine(con_str)

cnx = mysql.connector.connect(
        user=os.environ['MYSQL_DB_USER'],
        password=os.environ['MYSQL_DB_PASS'],
        host=os.environ['MYSQL_DB_HOST'],
        database=os.environ['MYSQL_DB_NAME']
)

@compiles(Insert)
def _prefix_insert_with_ignore(insert, compiler, **kw):
    return compiler.visit_insert(insert.prefix_with('IGNORE'), **kw)

cursor = cnx.cursor()

get_pairs = "SELECT id from tradable_pairs where doTrading=1"
get_ohlc = "SELECT timestamp, open, high, low, close FROM ohlc_data WHERE pairId=%s"
insert_signal = "INSERT IGNORE INTO signals (pairId, type, metric, timestamp) VALUES (%s, %s, %s, %s)"


window_size = 200
pd.set_option("display.precision", 2)

cursor.execute(get_pairs)

pairs=cursor.fetchall()

for pair in pairs:
	
	df = pd.read_sql("SELECT timestamp, close FROM ohlc_data WHERE pairId=%s", con=conn, params=[pair])
	df.set_index('timestamp', inplace=True)
	sma = pd.DataFrame()
	sma['sma30']  = df['close'].rolling(30).mean().dropna()
	sma['sma200'] = df['close'].rolling(200).mean().dropna()

	lastSMA30 = sma['sma30'].iloc[0]
	lastSMA200 = sma['sma200'].iloc[0]
	for index, row in sma.iterrows():
		if row['sma30'] > row['sma200'] and lastSMA30 < lastSMA200:
			cursor.execute(insert_signal, (pair[0], 'B', 'SMA30AboveSMA200', index))
			#print("SMA Cross Above: ", index)
		if row['sma30'] < row['sma200'] and lastSMA30 > lastSMA200:
			cursor.execute(insert_signal, (pair[0], 'S', 'SMA30BelowSMA200', index))
			#print("SMA Cross Below: ", index)
		lastSMA30 = row['sma30']
		lastSMA200 = row['sma200']
	cnx.commit()

