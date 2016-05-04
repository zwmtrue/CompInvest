# -*- coding: utf-8 -*-
"""
CompInvestI
HW3

@author: William
"""
import csv
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

class order:
    """Class obj for order"""
    def  __init__(self, orderinfo ):
        info = orderinfo#.split()
        self.date =  dt.datetime(int(info[0]),int(info[1]), int(info[2]),16,00)
        self.symbol = info[3]
        
        
        info[4] = info[4].strip()
        if info[4] == 'BUY':
            self.exchange = 'buy'
            
            self.volume = int(info[5])
        elif info[4] == 'SELL':
            self.exchange = 'sell'
            self.volume = - int(info[5])
        else:
            self.volume = info[4]#float('nan')
    
    def __str__(self):
        s = str(self.date)+'   '+ self.exchange +  '  '+self.symbol +'  in quantity of  '+ str(abs(self.volume))
        return s
    
if __name__ == '__main__':
    dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    dt_timeofday = dt.timedelta(hours=16)
    starting_cash = 50000
#step 1
    ordercsv = open('evt_trade.csv','rU')
    orderbook = csv.reader(ordercsv,delimiter = ',')
    ls_alldates = list()
    ls_symbols = list()
    ls_orders = list()

    for orderinfo in orderbook:
        thisorder = order(orderinfo)
        ls_orders.append(thisorder)
        ls_alldates.append(thisorder.date)
        ls_symbols.append(thisorder.symbol)
    #duplicates removal
    ls_symbols =   list(set(ls_symbols))
    ls_tradeddates =  sorted(list(set(ls_alldates)))
    dt_first = min(ls_alldates)
    dt_last = max(ls_alldates)
    dt_start_read = dt_first
    dt_end_read = dt_last + dt.timedelta(days=1)
    ls_alldates = du.getNYSEdays(dt_start_read, dt_end_read, dt_timeofday)

#step2
    ldt_timestamps = du.getNYSEdays(dt_start_read, dt_end_read, dt_timeofday)
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        #DATA CLEANSING IS ALWAYS IMPORTANT
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
    df_close = d_data['close']
    
    init_val = np.zeros((len(ls_alldates),len(ls_symbols)))
#step 3
    df_trade = pd.DataFrame(init_val,index = ls_alldates, columns = ls_symbols)
    ordercount = 0
    for one_order in ls_orders:
        try:
            alreadytrade = df_trade[ one_order.symbol][one_order.date]
        except:
            alreadytrade = 0
        df_trade.set_value(one_order.date, one_order.symbol, one_order.volume + alreadytrade )
#step 4
    ls_symbols.append("_CASH")
    ts_cash = pd.Series(np.zeros(len(ls_alldates)),index = ls_alldates)
    for today in ls_alldates:
        if today in ls_tradeddates:
            orders_in_today = [o for o in ls_orders if o.date == today]
            expense = 0
            for o in orders_in_today:
                expense += df_close[o.symbol][today]*o.volume
            if today == dt_first:
                ts_cash[today]= starting_cash - expense
            else:
                ts_cash[today]=   -expense 
            
        
    df_close['_CASH']= 1.0
    df_trade['_CASH'] = ts_cash
#step 5
    df_holding = df_trade.cumsum()

  #  print 'holding\n',df_holding
    val_output = open('evt.csv','wb')
    ts_fund = pd.Series()
    writetocsv = csv.writer(val_output,delimiter = ',')
    for idate in range(len(ls_alldates)):
        curval = 0.0
        curval =sum( df_holding.iloc[idate] * df_close.iloc[idate])
        date = ls_alldates[idate]
#        for symbol in ls_symbols:
#            curval += df_holding[symbol][date]*df_close[symbol][date]

        ts_fund[date] = curval
        rows_to_enter = [date.year,date.month,date.day,curval]
        writetocsv.writerow(rows_to_enter)
    val_output.close()
    ordercsv.close()
