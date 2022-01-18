# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 20:28:25 2022

@author: TAMIL SELVAN
"""

from kiteconnect import KiteConnect, KiteTicker
import pandas as pd
import datetime as dt
import numpy as np
import os
import time
import json



api_key = 'your_api_key'
api_secret = 'your_api_secret'

kite = KiteConnect(api_key)
url = kite.login_url()

request_token = 'your_request_token'
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
        if not os.path.isfile(symbol+'.csv'):
            data = pd.DataFrame()
            instrument_token = lookup(instruments, symbol)  
            if duration>100:
                no_of_hundreds = duration//100
                start = 100
                end = 0
                for i in range(no_of_hundreds):
                    df = pd.DataFrame(kite.historical_data(instrument_token, from_date = dt.datetime.today()-dt.timedelta(start), 
                    to_date = dt.datetime.today()-dt.timedelta(end), interval = tf))
                    data = data.append(df)
                    start+=100
                    end+=100
                dur1 = duration%100
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
    fetchandstoreOHLC(ticker, 1095, '5minute')


