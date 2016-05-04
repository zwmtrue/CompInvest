# -*- coding: utf-8 -*-
"""
CompInvest HW4    
@author: William
"""
import pandas as pd
import numpy as np
import math
import copy
import csv
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

def find_events(ls_symbols, d_data,thresh):
    ''' Finding the event dataframe '''
    df_close = d_data['actual_close']
    
    print "Finding Events"
 
    ldt_timestamps = df_close.index
    val_output = open('evt_trade.csv','wb')
    writetocsv = csv.writer(val_output,delimiter = ',')

    for i in range(1, len(ldt_timestamps)):
         for s_sym in ls_symbols:
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]

            if f_symprice_yest >= thresh and f_symprice_today < thresh:
                date1_str =str(ldt_timestamps[i]).split()[0].split('-')
                row1_to_enter = [date1_str[0],date1_str[1],date1_str[2],s_sym,'BUY',100]
                writetocsv.writerow(row1_to_enter)
                if len(ldt_timestamps)>(i+5):
                    date2_str =str(ldt_timestamps[i+5]).split()[0].split('-')
                else:
                    date2_str =str(ldt_timestamps[-1]).split()[0].split('-')
                
                row2_to_enter= [date2_str[0],date2_str[1],date2_str[2],s_sym,'SELL',100]
                writetocsv.writerow(row2_to_enter)                    
            
                
    val_output.close()                
    return 

def order_gen(ldt_timestamps,symbols_gen,target_thresh):
    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list(symbols_gen)    
    ls_symbols.append('SPY')
    ls_keys = ['close','actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
    
    find_events(ls_symbols, d_data,target_thresh)

if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    target_thresh = 5.0

    order_gen(ldt_timestamps, 'sp5002012',target_thresh)
   # profile_gen(ldt_timestamps, 'sp5002012')


    
