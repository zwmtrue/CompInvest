# -*- coding: utf-8 -*-
"""
CompInvestI
HW3
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
    price = d_data['close'].values
    na_price = price/ price[0,:]
    return price,na_price

def eval_rets(normalized_Prices):
    """calculate sharpe ratio and other terms for value series"""    
    anual_trading_days = 252
    portf_rets =  normalized_Prices.copy()
    rets = tsu.returnize0(portf_rets)#returns
    vol = np.std(portf_rets)#Volatility
    daily_ret = np.average(rets)#Average Daily Return
    sharpe = daily_ret/vol*math.sqrt(anual_trading_days)#Sharpe Ratio
    cum_ret = normalized_Prices[-1]#Cumulative Return
    return vol,daily_ret,sharpe,cum_ret 
    
    
    
    
if __name__ == '__main__':
    #val_output = open('values.csv','rU')
    val_output = open('evt.csv','rU')
   #val_output = open('values2.csv','rU')
    val_book = csv.reader(val_output,delimiter = ',')
    ls_vals = list()
    ls_alldates = list()
    anual_trading_days = 252
    
    for valueinfo in val_book:
        val = value(valueinfo)
        ls_vals.append(val.value) 
        ls_alldates.append(val.date)

    dt_timeofday = dt.timedelta(hours=16)
    dt_first = min(ls_alldates) 
    dt_last = max(ls_alldates)
    del ls_alldates[-1]
    del ls_vals[-1]

    init_val = ls_vals[0]
    normalized_vals = [v/init_val for v in ls_vals]
    ts_rets  = pd.TimeSeries( normalized_vals,index = ls_alldates)
    ls_symbols = ["$SPX"]
    spx_price,spx_normalized_price = get_rets(dt_first, dt_last,ls_symbols)
    [sim_vol,sim_daily_ret,sim_sharpe_ratio,sim_cum_ret] = eval_rets(ts_rets)  
    [spx_vol,spx_daily_ret,spx_sharpe_ratio,spx_cum_ret] = eval_rets(spx_normalized_price)
    
    print'Details of the Performance of the portfolio :'
    print'Data Range :'+ str(dt_first +dt_timeofday) +' to '+ str(dt_last +dt_timeofday)
    print'Sharpe Ratio of Fund :  ',sim_sharpe_ratio
    print'Sharpe Ratio of $SPX :  ',spx_sharpe_ratio
    print'Total Return of Fund :  ',sim_cum_ret
    print'Total Return of $SPX : ',spx_cum_ret[0]
    print'Standard Deviation of Fund :  ',sim_vol
    print'Standard Deviation of $SPX : ',spx_vol
    print'Average Daily Return of Fund :  ',sim_daily_ret
    print'Average Daily Return of $SPX : ',spx_daily_ret

    pltsimbol = ['$SPX','MarketSim']
    plt.clf()

    plt.plot(ls_alldates, spx_normalized_price)
    plt.plot(ls_alldates, normalized_vals)
    plt.legend(pltsimbol)    
    plt.ylabel('Adjusted Close')
    plt.xlabel('Date')
    plt.title('Normalized Price History')

    plt.show()
    plt.savefig('Normalized_Price_History.pdf', format='pdf')
