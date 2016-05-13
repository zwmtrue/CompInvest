# -*- coding: utf-8 -*-
"""
Created on Wed May 11 22:43:28 2016

@author: William
Part 1: 
Implement Bollinger bands as an indicator using 20 day look back. 
Create code that generates a chart showing the rolling mean, the stock price, 
and upper and lower bands. The upper band should represent the mean plus one 
standard deviation and here the lower band is the mean minus one standard 
deviation. Traditionally the upper and lower Bollinger bands are 2 standard 
deviations but for this assignment we would use a tighter band of 1 or a 
single standard deviation.
"""

#Load stock price of a period
import csv
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
dataobj = da.DataAccess('Yahoo', cachestalltime=0) 

def get_price(ldt_timestamps,symbol):
    """ get prices of a single stock in given period"""
 
    ls_keys =['close']
    ldf_data = dataobj.get_data(ldt_timestamps, symbol, ls_keys)
    
    d_data = dict(zip(ls_keys, ldf_data))
    price = d_data['close'].values
    return price

def bollinger(ldt_timestamps,price):
    price_Rolling_mean = pd.rolling_mean(price,20)
    price_Rolling_std = pd.rolling_std(price,20)
    price_LB = price_Rolling_mean - price_Rolling_std
    price_UB = price_Rolling_mean + price_Rolling_std
 
    bollinger_val = (price - price_Rolling_mean) / (price_Rolling_std)
    fig = plt.figure(1)
    plt.subplot(211)
    plt.plot(ldt_timestamps,price_Rolling_mean)
    plt.plot(ldt_timestamps,price_LB)
    plt.plot(ldt_timestamps,price_UB)
    ax1 = fig.add_subplot(211)
    ax1.plot(ldt_timestamps,price)
    
    ax2 = fig.add_subplot(212)
    ax2.plot(ldt_timestamps,bollinger_val)
    daily_indicator_val = np.zeros([len(bollinger_val),1])
    for idx in range(len(bollinger_val)):
        dayily_bollingerval = bollinger_val[idx]
        if dayily_bollingerval >= 1:
            daily_indicator_val[idx] = 1
            ax1.axvline(x=ldt_timestamps[idx], ymin =-1 ,ymax =1,c ='green')
            ax2.axvline(x=ldt_timestamps[idx], ymin =-1 ,ymax =1,c ='green')
        if dayily_bollingerval <= -1:        
            daily_indicator_val[idx] = -1
            ax2.axvline(x=ldt_timestamps[idx], ymin =-1 ,ymax =1,c ='red')
            ax1.axvline(x=ldt_timestamps[idx], ymin =-1 ,ymax =1,c ='red')
   # bollinger_indicator =  pd.TimeSeries(daily_indicator_val,index = ldt_timestamps)
    return bollinger_val#,daily_indicator_val

dt_s = dt.datetime(2010,1,1)
dt_e = dt.datetime(2010,12,31)
dt_timeofday = dt.timedelta(hours=16)
ldt_timestamps = du.getNYSEdays(dt_s, dt_e, dt_timeofday)
#ls_sylboms = ['AAPL','GOOG','IBM','MSFT']
Google_price = get_price(ldt_timestamps,['GOOG'])
Google_bollinger_val = bollinger(ldt_timestamps,Google_price)
Apple_price = get_price(ldt_timestamps,['AAPL'])
Apple_bollinger_val = bollinger(ldt_timestamps,Apple_price)
MSFT_price = get_price(ldt_timestamps,['MSFT'])
MSFT_bollinger_val = bollinger(ldt_timestamps,MSFT_price)