#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 08:37:03 2017

@author: massimo
"""

import pandas as pd
import numpy as np
import os
from IOready import IOready
from IOready_inout import *

# Test integration of investments on 2 regions table, use 'capital formation' method
regions = ['EU', 'USA']
products = ['product1', 'product2', 'product3', 'product4', 'product5']
activities = ['act1', 'act2', 'act3', 'act4']
unit = ['euro']
key = [1, 2, 3, 4, 4]

prods = len(regions) * products
acts = len(regions) * activities
reg_acts = [reg for reg in regions for _ in range(len(activities))] # found here: https://stackoverflow.com/questions/2449077/duplicate-each-member-in-a-list-python
reg_prods = [reg for reg in regions for _ in range(len(products))]
units = len(reg_prods) * unit

tdata = pd.DataFrame(np.split(np.arange(1,21), 5)) #nice
tdata = pd.concat([tdata, tdata], ignore_index=True)
tdata = pd.concat([tdata, tdata], axis=1)
tdata

FD = IOready().build(table=tdata, rows=prods, cols=acts, regcols=reg_acts, regrows=reg_prods, units=units)
FD.square(key)
print(FD.table)

USE = IOready().build(table=tdata, rows=prods, cols=acts, regcols=reg_acts, regrows=reg_prods, units=units)
USE.square(key)
print(USE.table)

VAact = IOready().build(table=pd.DataFrame([1,4,0,5,1,4,0,5]).T, 
               rows=['VAname'], cols=acts, regcols=reg_acts, 
               regrows=['VAextension'], units=['VAunits'])
VAact.table

# using the 'capital formation' method 
# Use 2nd column of the FD table: "act2"
USE.integrate_inv_CF(FD, 'act2', VAact, 'VAname')
print(USE.table)

        
# Test on exiobase mock-up version
# Import USE and FD tables (already squared)
USEdata = importing((os.getcwd()+'/Test_data/exio_USEsq.csv'), 'exiobase')

USEdata.info()
USEdata.iloc[30:33,0] # OK, same as in excel file used for testing
print(USEdata.shape)

FDdata = importing((os.getcwd()+'/Test_data/exio_FDsq.csv'), 'exiobase')
print(FDdata.shape)

VAactdata = importing((os.getcwd()+'/Test_data/exio_VAact.csv'), 'exiobase')
print(VAactdata.shape)

# Use IOready class
USE_original = IOready().frommultidf(USEdata)
USE = IOready().frommultidf(USEdata)
FD = IOready().frommultidf(FDdata)
VAact = IOready().frommultidf(VAactdata)

print("USE_original", USE_original.table.shape)
print("USE", USE.table.shape)
print("FD", FD.table.shape)
print("VAact", VAact.table.shape)

# Integrate investments with the 'capital formation' method.
USE.integrate_inv_CF(FD, 'Gross fixed capital formation', VAact, 'Operating surplus: Consumption of fixed capital')
print("USEoriginal", USE_original.table.shape)
print("USE", USE.table.shape)
print("FD", FD.table.shape)  # FD is still the same

USE_original.table.iloc[31:34,0:4] == USE.table.iloc[31:34,0:4]
# Good, it worked