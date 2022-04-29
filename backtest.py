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


get_pair_signals = "SELECT timestamp, type FROM signals WHERE pairId=%s order by timestamp asc"
get_ohlc_point = "SELECT close FROM ohlc_data WHERE pairId=%s AND timestamp=%s"

pairId=444

cursor.execute(get_pair_signals, (pairId, ) )

signals = cursor.fetchall()

startingMoney = 10000
skipFirst = False

for row in signals:
	if skipFirst:
		skipFirst=False
		continue
	timestamp = row[0]
	signalType = row[1]
	cursor.execute(get_ohlc_point, (pairId, timestamp))
	closePrice = cursor.fetchall()[0][0]

	if(signalType == 'B'):
		print("BUY *CRYPTO* @",closePrice,"with $",startingMoney)
		startingMoney = startingMoney / closePrice
	else:
		print("SELL *CRYPTO* @",closePrice,"Have",startingMoney,"*CRYPTO*")
		startingMoney = startingMoney * closePrice

	#print(timestamp, signalType, closePrice, startingMoney)
