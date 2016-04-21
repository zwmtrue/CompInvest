#!/usr/bin/python
import hw1 
import datetime as dt         
#find optimized portfolio
dt_start = dt.datetime(2011, 1, 1)
dt_end = dt.datetime(2011, 12, 31)
symbols =   ['AAPL', 'GOOG', 'IBM', 'MSFT']
print 'Problem 1\n',dt_start,dt_end,symbols
allocation,sharpe =hw1.portf_optimizer(dt_start, dt_end,symbols)
raw_input("Press Enter to continue...")