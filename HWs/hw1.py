#!/usr/bin/python
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
dt_timeofday = dt.timedelta(hours=16)

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

def portfolio_assesor(dt_start,dt_end,symbols,allocation):
    """ function to asses portfolio performance"""
# checke for input
    ls_all_syms = c_dataobj.get_all_symbols()
    for s in symbols:
        if s not in ls_all_syms:
            print "Invalid Symbols"
    if not(dt_start<dt_end) or (sum(allocation) != 1) or (len(symbols) != len(allocation) ):
        print "Invalide Input!"
        return
 
    na_normalized_price = get_rets(dt_start, dt_end,symbols)
#    na_normalized_price = na_price/ na_price[0,:]
    na_normalized_price = na_normalized_price*allocation
    na_normalized_price = na_normalized_price.sum(axis=1)
    portf_rets = na_normalized_price.copy()
    rets = tsu.returnize0(portf_rets)#returns
    vol = np.std(rets)#Volatility
    daily_ret = np.average(rets)#Average Daily Return
    sharpe = daily_ret/vol*math.sqrt(252)#Sharpe Ratio
    cum_ret = na_normalized_price[-1]#Cumulative Return
    return vol,daily_ret,sharpe,cum_ret
 
def portf_optimizer(dt_start, dt_end,symbols):
    "A function that optimize the portfolio by maxmizing sharpe_ratio"
    zto = [x/10.0 for x in range(0,11,1)]#0-1 vector, step = 0.1
    allocs = [[i,j,k,l] for i in  zto for j in  zto for k  in  zto for l in  zto if  i+j+k+l == 1.0]
    #all possible allocations
    Higheset_SR = 0.0
    for allocation in allocs:
        
        vol, daily_ret, sharpe, cum_ret = portfolio_assesor(dt_start, dt_end,symbols ,allocation )
#        print allocation,sharpe
        if sharpe > Higheset_SR:
            Best_alloc = allocation
            Higheset_SR = sharpe
    print symbols,'\n',Best_alloc,'\n','Sharpe Ratio = ', Higheset_SR

    return allocation,sharpe

"""
symbols = ['AAPL', 'GOOG', 'IBM', 'MSFT']
dt_start = dt.datetime(2011,1,1)
dt_end = dt.datetime(2011,12,31)
allocation,sharpe =portf_optimizer(dt_start, dt_end,symbols)

#Verification w. examples
dt_start = dt.datetime(2011, 1, 1)
dt_end = dt.datetime(2011, 12, 31)

symbols1 = ['AAPL', 'GLD', 'GOOG', 'XOM']
alloc1 =[0.4, 0.4, 0.0, 0.2]
vol,daily_ret, sharpe, cum_ret= portfolio_assesor(dt_start, dt_end,symbols1 ,alloc1 )

print dt_start,'-',dt_end,'\n',symbols1,'\n',alloc1
print 'Sharpe Ratio',sharpe,'\nVolatility',vol,'\nAverage Daily Return',daily_ret,'\nCumulative Return',cum_ret

dt_start = dt.datetime(2010, 1, 1)
dt_end = dt.datetime(2010, 12, 31)
symbols2 =['AXP', 'HPQ', 'IBM', 'HNZ']
alloc2 = [0.0, 0.0, 0.0, 1.0]
vol, daily_ret, sharpe, cum_ret= portfolio_assesor(dt_start, dt_end,symbols2 ,alloc2 )
print dt_start,'-',dt_end,'\n',symbols2,'\n',alloc2
print 'Sharpe Ratio',sharpe,'\nVolatility',vol,'\nAverage Daily Return',daily_ret,'\nCumulative Return',cum_ret

#find optimized portfolio
dt_start = dt.datetime(2011, 1, 1)
dt_end = dt.datetime(2011, 12, 31)
symbols = ['AAPL', 'GLD', 'GOOG', 'XOM']
t1=dt.datetime.now()
allocation,sharpe =portf_optimizer(dt_start, dt_end,symbols)
t2=dt.datetime.now()
print t2 - t1
portf_rets = get_rets(dt_start,dt_end,symbols)
portf_rets *= allocation
portf_rets = portf_rets.sum(axis = 1)

spx_rets = get_rets(dt_start,dt_end,["$SPX"])

ldt_timestamps  = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
plt.clf()
plt.plot(ldt_timestamps, spx_rets)  # $SPX 50 days
plt.plot(ldt_timestamps, portf_rets)  # port_folio 50 days
plt.axhline(y=0, color='r')
plt.legend(['$SPX', 'Portf'])
plt.ylabel('Daily Returns')
plt.xlabel('Date')
plt.savefig('rets.pdf', format='pdf')
"""
