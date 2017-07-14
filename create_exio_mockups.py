#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 14:03:31 2017

@author: massimo
"""

import pandas as pd
import numpy as np
import os
import json
from IOready import IOready
from IOready_inout import *

metadata = json.load(open(os.getcwd()+'/Test_data/exio_metadata.txt'))
metadata.keys() # is a dict...
metadata.items()
len(metadata['products_names_short'])


# Create mock-up versions of exiobase (same size and labels, random numbers)
# these are all dataframe objects
USE = pd.DataFrame(np.random.rand(9600//48*3,7872//48*3), dtype=float)
SUP = pd.DataFrame(np.random.rand(9600//48*3,7872//48*3), dtype=float)
FD = pd.DataFrame(np.random.rand(9600//48*3,288//48*3), dtype=float)
VAact = pd.DataFrame(np.random.rand(23,7872//48*3), dtype=float)

print(SUP.shape, SUP.shape, FD.shape, VAact.shape)

# Get random key for squaring
# Let's assume the first 36 sectors will be aggregated
key_vec = [1]*37 + list(range(2,(200-35)))
len(key_vec)

# need to give the names to my three regions...here my favourite ones
countries_codes = ['IT', 'DK', 'EU']

# building the labels for each table, it's the boring part...

# c = country, n = name, u = unit
# rindex = row index, cindex = column index
# short = 164 products, long = 200 products
# so 'c_rindex_short' is a list where each country codes is repeated 164 times
# to be used as label for the products (i.e. the rows)

c_rindex_short = [reg for reg in countries_codes for _ in range(len(metadata['products_names_short']))]  # found here: https://stackoverflow.com/questions/2449077/duplicate-each-member-in-a-list-python
c_rindex_long = [reg for reg in countries_codes for _ in range(len(metadata['products_names_long']))]
n_rindex_short = metadata['products_names_short'] * len(countries_codes)
n_rindex_long = metadata['products_names_long'] * len(countries_codes)
u_rindex_short = metadata['activities_phi_units'] * len(countries_codes)
u_rindex_long = metadata['products_phi_units_long'] * len(countries_codes)
c_cindex = [reg for reg in countries_codes for _ in range(len(metadata['activities_names']))]
n_cindex = metadata['activities_names'] * len(countries_codes)
fd_c_cindex = [reg for reg in countries_codes for _ in range(len(metadata['final_demand_names']))]
fd_n_cindex = metadata['final_demand_names'] * len(countries_codes)
va_c_rindex = metadata['value_added_code1']
va_n_rindex = metadata['value_added_names']
va_u_rindex = metadata['value_added_units']

for i in [c_rindex_short,c_rindex_long, n_rindex_short,n_rindex_long,
          u_rindex_short,u_rindex_long,c_cindex,n_cindex,fd_c_cindex,fd_n_cindex,
          va_c_rindex,va_n_rindex,va_u_rindex]: print(len(i))

# Use the IOready class to create tables and export in exiobase format
# Supply
SUPi = IOready().build(SUP, rows=n_rindex_long, cols=n_cindex, 
              units=u_rindex_long, regrows=c_rindex_long , regcols=c_cindex)
SUPi.table.info()

# Use
USEi = IOready().build(USE, rows=n_rindex_long, cols=n_cindex, 
              units=u_rindex_long, regrows=c_rindex_long , regcols=c_cindex)
USEi.table.info()

# Final Demand
FDi = IOready().build(FD, rows=n_rindex_long, cols=fd_n_cindex, 
              units=u_rindex_long, regrows=c_rindex_long , regcols=fd_c_cindex)
FDi.table.info()

# Value Added activities
VAacti = IOready().build(VAact, rows=va_n_rindex, cols=n_cindex, 
              units=va_u_rindex, regrows=va_c_rindex, regcols=c_cindex)
VAacti.table.info()
exporting(VAacti.table, (os.getcwd()+'/Test_data/exio_VAact.csv'))

# Square SUP
SUPi.square(key_vec)
SUPi.table.info() # it's square!

# Square USE
USEi.square(key_vec)
USEi.table.info()
exporting(USEi.table, (os.getcwd()+'/Test_data/exio_USEsq.csv'))

# Square FD
FDi.square(key_vec)
FDi.table.info()
exporting(FDi.table, (os.getcwd()+'/Test_data/exio_FDsq.csv'))
