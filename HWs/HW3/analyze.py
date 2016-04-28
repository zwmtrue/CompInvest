# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 15:37:00 2016

@author: William
"""
#!/usr/bin/python
import csv
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)

class value:
    '''class for storing value info'''
    def __init__(self,info):
        
        self.date = dt.datetime(int(info[0]),int(info[1]),int(info[2]))
        self.value = float(info[3])
    
    
    def __str__(self):
        s = str(self.date)+'\t'+str(self.value)
        return s
        
def get_rets(dt_start, dt_end,symbols):
    """ get normalized returns"""
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, ls_keys)
    
    d_data = dict(zip(ls_keys, ldf_data))
    na_price = d_data['close'].values
    na_price = na_price/ na_price[0,:]
    return na_price

if __name__ == '__main__':
    val_output = open('values.csv','rU')
    val_book = csv.reader(val_output,delimiter = ',')
    ls_vals = list()
    ls_alldates = list()
    
    for valueinfo in val_book:
        val = value(valueinfo)
        ls_vals.append(val.value)
        ls_alldates.append(val.date)
    dt_first = min(ls_alldates)
    dt_last = max(ls_alldates)
    init_val = ls_vals[0]
    normalized_vals = [v/init_val for v in ls_vals]
  #  dailyval =normalized_vals.copy() ;

#    num_of_days = int((dt_last - dt_first).days-1)

    ts_rets  = pd.TimeSeries( normalized_vals,index = ls_alldates)
    anual_trading_days = 252
     
    rets = tsu.returnize0(ts_rets)#returns
    vol = np.std(rets)#Volatility
    portf_cum_rets = normalized_vals[-1]
    daily_ret = np.average(rets)#Average Daily Return   
    sharpe_ratio = daily_ret*math.sqrt(anual_trading_days)/vol#Sharpe Ratio
    
    spx_normalized_price = get_rets(dt_start, dt_end,'')
    
    

    
