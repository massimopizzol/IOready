#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 08:37:03 2017

@author: massimo
"""

import pandas as pd
import numpy as np
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

        

# Test on exiobase

# Import HIOTand FD tables (already squared)
HIOTdata = importing('/Users/massimo/Documents/AAU/Research/Databases/exiobase_vtext/IOready_MR_HUSE_2011_v3.3.11_final_HIOT_zerodiag.csv', 'exiobase')

HIOTdata.info()
HIOTdata.iloc[30:33,0] # OK, same as in excel file used for testing
print(HIOTdata.shape)

FDdata = importing('/Users/massimo/Documents/AAU/Research/Databases/exiobase_vtext/IOready_MR_HUSE_2011_v3.3.11_final_FDsq.csv', 'exiobase')
print(FDdata.shape)

VAactdata = importing('/Users/massimo/Documents/AAU/Research/Databases/exiobase_vtext/IOready_MR_HIOT_2011_v3.3.11_VA_act.csv', 'exiobase')
print(VAactdata.shape)

# Use IOready class
HIOT_original = IOready().frommultidf(HIOTdata)
HIOT = IOready().frommultidf(HIOTdata)
FD = IOready().frommultidf(FDdata)
VAact = IOready().frommultidf(VAactdata)

print("HIOT_original", HIOT_original.table.shape)
print("HIOT", HIOT.table.shape)
print("FD", FD.table.shape)
print("VAact", VAact.table.shape)


# Integrate investments with the 'capital formation' method.

HIOT.integrate_inv_CF(FD, 'Gross fixed capital formation', VAact, 'Operating surplus: Consumption of fixed capital')
print("HIOToriginal", HIOT_original.table.shape)
print("HIOT", HIOT.table.shape)
print("FD", FD.table.shape)  # FD is still the same

print(HIOT_original.table.iloc[31:34,0:4])
print(HIOT.table.iloc[31:34,0:4])

HIOT_original.table.iloc[31:34,0:4] == HIOT.table.iloc[31:34,0:4]
# Good, it worked