#!/usr/bin/python
import hw1 
import datetime as dt         
#find optimized portfolio
dt_start = dt.datetime(2010, 1, 1)
dt_end = dt.datetime(2010, 12, 31)
symbols =   ['BRCM', 'TXN', 'IBM', 'HNZ']
print 'Problem 4\n',dt_start,dt_end,symbols
allocation,sharpe =hw1.portf_optimizer(dt_start, dt_end,symbols)
raw_input("Press Enter to continue...")