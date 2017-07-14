#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 07:26:23 2017

@author: massimo
"""

# testing 'IOready.fromtable', 'IOready.frommultidf' and 'IOready.square' methods

import pandas as pd
import numpy as np
from IOready import IOready

mydata = pd.DataFrame([[np.NaN, np.NaN, np.NaN, 'IT', 'IT', 'FR', 'FR'],  # table in exiobase format
                       [np.NaN, np.NaN, np.NaN, 'act1', 'act2', 'act1', 'act2'],
                       ['IT', 'product1', 'tonnes', 1, 2, 3, 4],
                       ['IT', 'product2', 'euro', 5, 6, 7, 8],
                       ['IT', 'product3', 'euro', 9, 10, 11, 12],
                       ['FR', 'product1', 'tonnes', 13, 14, 15, 16],
                       ['FR', 'product2', 'euro', 17, 18, 19, 20],
                       ['FR', 'product3', 'euro', 21, 22, 23, 24]])

SUP = IOready().fromtable(mydata)
SUP.regs


print("\n\nProduct regions\n\n", SUP.table.index.get_level_values('Reg'),
      "\n\nProduct names\n\n", SUP.table.index.get_level_values('Prod'), 
      "\n\nProduct units\n\n", SUP.table.index.get_level_values('Unit'),
      "\n\nTable\n\n", SUP.table,
      "\n\nActivity regions\n\n", SUP.table.columns.get_level_values('Reg'),
      "\n\nActivity names\n\n", SUP.table.columns.get_level_values('Act'), 
      "\n\nNr of regions\n\n", SUP.regs)
SUP.table.info()

SUP2 = SUP.table.copy() # test 'IOready.frommultidf' method
SUP3 = IOready().frommultidf(SUP2)
SUP3.table
SUP3.regs

key = [1, 2, 2]  # This means the products 2 and 3 are outputs of activity 2
SUP.square(key)  # test 'IOready.square' method
SUP.table


# Test 'IOready.build' method
prods = ['product1', 'product2', 'product3', 'product1', 'product2', 'product3']
acts = ['act1', 'act2', 'act1', 'act2']
reg_acts = ['EU', 'EU', 'USA', 'USA']
reg_prods = ['EU', 'EU', 'EU', 'USA', 'USA', 'USA']
units = ['tonnes', 'euro', 'euro', 'tonnes', 'euro', 'euro']

tdata = pd.DataFrame([[1, 2, 3, 4],
                     [5, 6, 7, 8],
                     [9, 10, 11, 12],
                     [13, 14, 15, 16],
                     [17, 18, 19, 20],
                     [21, 21, 23, 24]])

SUP = IOready()
SUP.build(table=tdata, rows=prods, cols=acts, regcols=reg_acts, regrows=reg_prods, units=units)

SUP.regs
print("\n\nProduct regions\n\n", SUP.table.index.get_level_values('Reg'),
      "\n\nProduct names\n\n", SUP.table.index.get_level_values('Prod'), 
      "\n\nProduct units\n\n", SUP.table.index.get_level_values('Unit'),
      "\n\nTable\n\n", SUP.table,
      "\n\nActivity regions\n\n", SUP.table.columns.get_level_values('Reg'),
      "\n\nActivity names\n\n", SUP.table.columns.get_level_values('Act'), 
      "\n\nNr of regions\n\n", SUP.regs)

SUP.table.info()


key = [1, 2, 2]
SUP.square(key)
SUP.table