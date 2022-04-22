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
