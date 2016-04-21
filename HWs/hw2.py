#!/usr/bin/python
import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

def find_events(ls_symbols, d_data):
    ''' Finding the event dataframe '''
    df_close = d_data['close']
#    ts_market = df_close['SPY']

    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]

            if f_symprice_yest >= 5:
                if f_symprice_today < 5:
                    df_events[s_sym].ix[ldt_timestamps[i]] = 1
                    
        return df_events
            
if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    ls_symbols2008 = dataobj.get_symbols_from_list('sp5002008')
    ls_symbols2008.append('SPY')
    
    ls_symbols2012 = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols2012.append('SPY')
  
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data2008 = dataobj.get_data(ldt_timestamps, ls_symbols2008, ls_keys)
    ldf_data2012 = dataobj.get_data(ldt_timestamps, ls_symbols2012, ls_keys)
    
    d_data2012 = dict(zip(ls_keys, ldf_data2012))
#It it always important to remove NAN from price data
    for s_key in ls_keys:
        d_data2012[s_key] = d_data2012[s_key].fillna(method='ffill')
        d_data2012[s_key] = d_data2012[s_key].fillna(method='bfill')
        d_data2012[s_key] = d_data2012[s_key].fillna(1.0)

    df_events2012 = find_events(ls_symbols2012, d_data2012)
    print "Creating Study"
    ep.eventprofiler(df_events2012, d_data2012, i_lookback=20, i_lookforward=20,
                s_filename='MyEventStudy2012.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')
"""
    d_data2008 = dict(zip(ls_keys, ldf_data2008))
#It it always important to remove NAN from price data
    for s_key in ls_keys:
        d_data2008[s_key] = d_data2008[s_key].fillna(method='ffill')
        d_data2008[s_key] = d_data2008[s_key].fillna(method='bfill')
        d_data2008[s_key] = d_data2008[s_key].fillna(1.0)

    df_events2008= find_events(ls_symbols2008, d_data2008)
    print "Creating Study"
    ep.eventprofiler(df_events2008, d_data2008, i_lookback=20, i_lookforward=20,
                s_filename='MyEventStudy2008.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')
"""
    
