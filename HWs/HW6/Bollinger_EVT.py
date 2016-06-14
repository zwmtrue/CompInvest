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
import QSTK.qstkstudy.EventProfiler as ep

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
dataobj = da.DataAccess('Yahoo', cachestalltime=0) 

def bollinger(ldt_timestamps,symbols_gen,lookback,thresh):
    """ get prices of a single stock in given period"""
 
    ls_keys = ['close','actual_close']
    ls_symbols = dataobj.get_symbols_from_list(symbols_gen)    
    ls_symbols.append('SPY')
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
    price = copy.deepcopy(d_data['close'])
    price_Rolling_mean = pd.rolling_mean(price,lookback)
    price_Rolling_std = pd.rolling_std(price,lookback)
    bollinger_val = (price - price_Rolling_mean) / (price_Rolling_std)
    evt_data = bollinger_val    
    print "Finding Events"
 
    df_events = copy.deepcopy(evt_data)
    df_events = df_events * np.NAN


    for i in range(1, len(ldt_timestamps)):
         SPY_BV = evt_data['SPY'].ix[ldt_timestamps[i]]
         if SPY_BV>= 1.1:
             for s_sym in ls_symbols:
                f_sym_indicator_today = evt_data[s_sym].ix[ldt_timestamps[i]]
                f_sym_indicator_yest = evt_data[s_sym].ix[ldt_timestamps[i - 1]]
    
                if f_sym_indicator_yest >= thresh and f_sym_indicator_today < thresh:
                     df_events[s_sym].ix[ldt_timestamps[i]] = 1
             
    ep.eventprofiler(b_evt, d_data, i_lookback=20, i_lookforward=20,
            s_filename='MyEventStudy'+ symbols_gen+'.pdf', b_market_neutral=True, b_errorbars=True,
            s_market_sym='SPY')

    
    return df_events,evt_data
 

dt_s = dt.datetime(2010,1,1)
dt_e = dt.datetime(2010,12,31)
dt_timeofday = dt.timedelta(hours=16)
ldt_timestamps = du.getNYSEdays(dt_s, dt_e, dt_timeofday)
symbols_gen = 'sp5002012'
#['AAPL','GOOG','IBM','MSFT']
lookback  = 20
thresh = 2.0
b_evt,evt_data = bollinger(ldt_timestamps,symbols_gen,lookback,thresh)
