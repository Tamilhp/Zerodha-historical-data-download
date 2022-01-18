# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 19:49:29 2021

@author: TAMIL SELVAN
"""

from kiteconnect import KiteConnect, KiteTicker
import pandas as pd
import datetime as dt
import numpy as np
import os
from selenium import webdriver
import time
#from pyotp import TOTP
#import requests
import json
#from selenium import webdriver

#totp = TOTP("TLAAJOPQWGQEKYGXRSBB4BDNZJ4ZKN7E")
#token = totp.now()

with open('C:/Users/TAMIL SELVAN/.spyder-py3/app.json', 'r') as key:
    app = json.load(key)

api_key = app['api_key']
api_secret = app['api_secret']

kite = KiteConnect(api_key)
url = kite.login_url()

browser = webdriver.Chrome()
browser.get(url)

username_box = browser.find_element_by_id("userid")
print(type(username_box))
username_box.send_keys(app['userid'])


password_box = browser.find_element_by_id("password")
print(type(password_box))
password_box.send_keys(app['pass'])
password_box.submit()

time.sleep(5)

#pin_box = browser.find_elements_by_id("totp")
#print(pin_box)
#pin_box[0].send_keys(token)
#pin_box[0].submit() 

pin_box = browser.find_elements_by_id("pin")
print(pin_box)
pin_box[0].send_keys(app['pin'])
pin_box[0].submit()

request_token = 'X31XQeMhse75McoYaTlZ1EhbUytOebai'
session = kite.generate_session(request_token, api_secret)
access_token = session['access_token']
kite.set_access_token(access_token)

instruments = pd.DataFrame(kite.instruments('NSE'))

def lookup(df, symbol):
    try:
        return df[df.tradingsymbol==symbol].instrument_token.values[0]
    except:
        return -1

def fetchandstoreOHLC(symbol,duration,tf):
    nodata=[]
    try:
        if not os.path.isfile(symbol+'.csv'):   #checks whether the file is already present or not
            data = pd.DataFrame()               
            instrument_token = lookup(instruments, symbol)  #gets the instrument token of the symbol, where instruments is the dataframe of instruments fetched from kiteconnect
            if duration>2000:      
                no_of_two_thousands = duration//2000  #gets the no of 2000s : for eg: if duration is 4350, it returns 2 since there are 2 thousands....this is due to the 2000 days limit set by kite
                start = 2000
                end = 0
                for i in range(no_of_two_thousands):
                    df = pd.DataFrame(kite.historical_data(instrument_token, from_date = dt.datetime.today()-dt.timedelta(start), 
                    to_date = dt.datetime.today()-dt.timedelta(end), interval = tf))
                    data = data.append(df)
                    start+=2000
                    end+=2000
                dur1 = duration%2000
                df1 = pd.DataFrame(kite.historical_data(instrument_token, from_date = dt.datetime.today()-dt.timedelta(duration), 
                                      to_date = dt.datetime.today()-dt.timedelta(duration-dur1), interval = tf))
                data = data.append(df1)
            else:
                df2 = pd.DataFrame(kite.historical_data(instrument_token, from_date = dt.datetime.today()-dt.timedelta(duration), 
                                      to_date = dt.datetime.today(), interval = tf))
                data = data.append(df2)
            data.set_index("date", inplace = True)
            data.sort_index(ascending= True,inplace = True)
            print('Storing {} days data for {}'.format(duration, symbol))
            data.to_csv(symbol+'.csv')
        else:
            print('Data already available for{}'.format(symbol))
            return
    except:
        print("skipping for {}".format(symbol))
        nodata.append(symbol)
    
tickers = ['HDFCBANK','ICICIBANK','KOTAKBANK', 'AXISBANK', 'SBIN', 'RELIANCE','TCS','INFY','HINDUNILVR','HDFC','BAJFINANCE','WIPRO','BHARTIARTL','HCLTECH','ASIANPAINT','ITC','LT','ULTRACEMCO',
           'MARUTI','SUNPHARMA','TATASTEEL','JSWSTEEL','TITAN','ADANIPORTS','ONGC','HDFCLIFE','TECHM','DIVISLAB','POWERGRID','SBILIFE','NTPC','BAJAJ-AUTO','BPCL','IOC','M&M','SHREECEM','HINDALCO',
           'GRASIM','BRITANNIA','TATAMOTORS','COALINDIA','TATACONSUM','INDUSINDBK','DRREDDY','CIPLA','EICHERMOT','UPL','NESTLEIND','HEROMOTOCO','NIFTY 50','NIFTY BANK']


for ticker in tickers:
    fetchandstoreOHLC(ticker, 7665, 'day')

# =============================================================================
# for ticker in tickers:
#     fetchandstoreOHLC(ticker, 100, '5minute')
# 
# for i in range(1,len(tickers)):
#     print(i)
#     i+=1
# fetchandstoreOHLC('IRCTC', 100, '5minute')
# fetchandstoreOHLC('BIOCON', 100, '5minute')
# =============================================================================
