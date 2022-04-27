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

get_pairs = "SELECT id from tradable_pairs"
get_ohlc = "SELECT timestamp, open, high, low, close FROM ohlc_data INNER JOIN tradable_pairs ON ohlc_data.pairId=tradable_pairs.id WHERE tradable_pairs.id=%s"
insert_sma = "INSERT INTO simple_moving_average (timestamp, pairId, period, open, high, low, close) VALUES (%s, %s, %s, %s, %s, %s, %s)"

window_size = 200
pd.set_option("display.precision", 2)

cursor.execute(get_pairs)

pairs=cursor.fetchall()

for pair in pairs:
	cursor.execute(get_ohlc, pair)
	data = cursor.fetchall()
	
	df = pd.DataFrame()
	
	df['open'] = pd.Series([e[1] for e in data])
	df['high'] = pd.Series([e[2] for e in data])
	df['low'] = pd.Series([e[3] for e in data])
	df['close'] = pd.Series([e[4] for e in data]) 
	df['timestamp'] = pd.Series([e[0] for e in data], dtype='datetime64[ns]')
	df.set_index('timestamp', inplace=True)
	#print(df)

	sma = pd.DataFrame()
	sma['open'] = df['open'].rolling(window_size).mean().dropna()
	sma['high'] = df['high'].rolling(window_size).mean().dropna()
	sma['low'] = df['low'].rolling(window_size).mean().dropna()
	sma['close'] = df['close'].rolling(window_size).mean().dropna()
	sma['pairId'] = pair[0]
	sma['period'] = window_size

	sma.to_sql('simple_moving_average', con=conn, if_exists='append')

	#print(sma)

