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
if __name__ == '__main__':
    dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    dt_timeofday = dt.timedelta(hours=16)
#step 1
    ordercsv = 'C:\Users\William\PycharmProjects\CompInvest\HWs\HW3\orders.csv'
    orderbook = csv.reader(open(ordercsv,'rU'),delimiter = ',')
    ls_alldates = list()
    ls_symbols = list()

    for order in orderbook:
 #       print order
        ls_alldates.append(dt.datetime(int(order[0]),int(order[1]),int(order[2]),16,00))

        ls_symbols .append(order[3])


    ls_alldates =  sorted(list(set(ls_alldates)))
    dt_first = min(ls_alldates)
    dt_last = max(ls_alldates)
    ls_symbols =   list(set(ls_symbols))
#    print dt_alldates,'\n',dt_first,'\n',dt_last
#    print ls_symbols
    dt_start_read = dt_first
    dt_end_read = dt_last + dt.timedelta(days=1)
#step2
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start_read, dt_end_read, dt_timeofday)
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)

    d_data = dict(zip(ls_keys, ldf_data))


    init_val = np.zeros((len(ls_alldates),len(ls_symbols)))
   # print df_close
#step 3
    df_trade = pd.DataFrame(init_val,index = ls_alldates,columns = ls_symbols)
    orderbook = csv.reader(open(ordercsv,'rU'),delimiter = ',')
    for order in orderbook:
      #  print order
        date = dt.datetime(int(order[0]),int(order[1]),int(order[2]),16,00)
        symbol = order[3]
        vol = int(order[5])
        if order[4] is 'Sell':
            vol = -vol

        #init = df_trade_matrix.get_value(, symbol)
        id = ls_alldates.index(date)
        isy = ls_symbols.index(symbol)
   #     print id, isy
        #this is not necessary
        #val =df_trade_matrix.get_value(ls_alldates[id], ls_symbols[isy])
        fin_val = df_trade.set_value(date, symbol, vol )
  #  print df_trade_matrix
    #step 4
    ts_cash = pd.TimeSeries(np.zeros(len(ls_alldates)),index = ls_alldates)
    orderbook = csv.reader(open(ordercsv, 'rU'), delimiter=',')

    for order in orderbook:
        date= dt.datetime(int(order[0]),int(order[1]),int(order[2]),16,00)
        vol =int(order[5])
        price = d_data['close'][symbol][date]
        print price















