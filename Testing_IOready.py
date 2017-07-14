#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 00:36:13 2017

@author: massimo
"""

import pandas as pd
import numpy as np
import os
from IOready import IOready
from IOready_inout import *

# Test 'IOready.build' method
prods = ['product1', 'product2', 'product3', 'product1', 'product2', 'product3']
acts = ['act1', 'act2', 'act1', 'act2']
reg_acts = ['EU', 'EU', 'USA', 'USA']
reg_prods = ['EU', 'EU', 'EU', 'USA', 'USA', 'USA']
units = ['tonnes', 'euro', 'euro', 'tonnes', 'euro', 'euro']

tdata = pd.DataFrame([[1, 2, 3, 4],  # this could be imported from a file
                     [5, 6, 7, 8],
                     [9, 10, 11, 12],
                     [13, 14, 15, 16],
                     [17, 18, 19, 20],
                     [21, 21, 23, 24]])

SUP = IOready()
SUP.build(table=tdata, rows=prods, cols=acts, regcols=reg_acts, regrows=reg_prods, units=units)

SUP.regs
print("\n\nProduct regions\n\n", SUP.table.index.get_level_values(0),
      "\n\nProduct names\n\n", SUP.table.index.get_level_values(1), 
      "\n\nProduct units\n\n", SUP.table.index.get_level_values(2),
      "\n\nTable\n\n", SUP.table,
      "\n\nActivity regions\n\n", SUP.table.columns.get_level_values(0),
      "\n\nActivity names\n\n", SUP.table.columns.get_level_values(1), 
      "\n\nNr of regions\n\n", SUP.regs)

SUP.table.info()


key = [1, 2, 2]  # This means the products 2 and 3 are outputs of activity 2
SUP.square(key)  # test 'IOready.square' method
SUP.table


# testing 'IOready.fromtable', and 'IOready.square' methods
# Let's assume we have a dataframe already in exiobase format
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
print("\n\nProduct regions\n\n", SUP.table.index.get_level_values(0),
      "\n\nProduct names\n\n", SUP.table.index.get_level_values(1), 
      "\n\nProduct units\n\n", SUP.table.index.get_level_values(2),
      "\n\nTable\n\n", SUP.table,
      "\n\nActivity regions\n\n", SUP.table.columns.get_level_values(0),
      "\n\nActivity names\n\n", SUP.table.columns.get_level_values(1), 
      "\n\nNr of regions\n\n", SUP.regs)

SUP.table.info()

key = [1, 2, 2]  # This means the products 2 and 3 are outputs of activity 2
SUP.square(key)  # test 'IOready.square' method
SUP.table


# Last, test 'IOready.frommultidf' method as well as IOready_inout import export
# we have a file in exiobase format
mydata2 = importing((os.getcwd()+'/Test_data/mydata_exioformat.csv'), 'exiobase')
SUP2 = IOready().frommultidf(mydata2)
SUP2.table
SUP2.regs
exporting(SUP2.table, 'SUP2table.csv')

extensions = importing((os.getcwd()+'/Test_data/exio_extensions_format_test.csv'), 'factor')
exts = IOready().frommultidf(extensions)
exts.table
exts.regs
exporting(exts.table, 'ext_export.csv', exio = 'extension')  # need to specify this

