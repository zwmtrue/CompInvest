#!/usr/bin/python
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def portfolio_assesor(dt_start,dt_end,symbols,allocatio):
    c_dataobj = da.DataAccess('Yahoo')
#    s_path = c_dataobj.rootdir
    ls_all_syms = c_dataobj.get_all_symbols()
    for s in symbols:
        if s not in ls_all_syms:
            print "Invalid Symbols"
    if dt_start>dt_end or len(symbols) <4 or len(allocatio)<4 :
        print "Invalide Input!"
        return
    
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    ls_keys = 'close'
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    print d_data.keys()
    print ldf_data

"""
    na_price = d_data['close'].values
    na_normalized_price = na_price / na_price[0,:]
    na_normalized_price_w_allocs = na_normalized_price * lf_port_alloc
    na_total_port = na_normalized_price_w_allocs.cumsum(axis=1)[:,3]

    na_rets = na_total_port.copy()
    tsu.returnize0(na_rets)

    std_of_daily_returns = na_rets.std()

    avg_daily_returns = na_rets.mean()

    sharpe_ratio = math.sqrt(252) * avg_daily_returns/std_of_daily_returns

    cum_return = na_total_port[len(ldt_timestamps)-1]

    return std_of_daily_returns, avg_daily_returns, sharpe_ratio, cum_return
"""    




dt_start = dt.datetime(2006, 1, 1)
dt_end = dt.datetime(2006, 1, 31)

#vol, daily_ret, sharpe, cum_ret =
portfolio_assesor(dt_start, dt_end, ['GOOG','AAPL','GLD','XOM'], [0.2,0.3,0.4,0.1])
        
    
