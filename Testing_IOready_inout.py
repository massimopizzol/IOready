# -*- coding: utf-8 -*-
"""
testing importers
"""

import pandas as pd
import time
from IOready_inout import *


# singletxt
start = time.time()
MRtable = importing('/Users/massimo/Documents/AAU/Research/Databases/exiobase_vtext/MR_HUSE_2011_v3.3.11_final_SUP.txt', 'single')
print(start - time.time())
MRtable.info()
MRtable.iloc[0:3,0:3]
                        
# singlecsv
start = time.time()
MRtable = importing('/Users/massimo/Documents/AAU/Research/Databases/exiobase_vtext/MR_HUSE_2011_v3.3.11_final_SUP.csv', 'single')
print(start - time.time())
MRtable.info()
MRtable.iloc[0:3,0:3]

# multitxt
start = time.time()
MRtable = importing('/Users/massimo/Documents/AAU/Research/Databases/exiobase_vtext/MR_HIOT_2011_v3.3.11.txt', 'multi')
print(start - time.time())
type(MRtable)
MRtable['table'].info()
MRtable['table'].iloc[0:3,0:3]
MRtable['diag'].info()
MRtable['diag'].iloc[0:3]
  
# multicsv
start = time.time()
MRtable = importing('/Users/massimo/Documents/AAU/Research/Databases/exiobase_vtext/MR_HIOT_2011_v3.3.11.csv', 'multi')
print(start - time.time())
type(MRtable)
MRtable['table'].info()
MRtable['table'].iloc[0:3,0:3]
MRtable['diag'].info()
MRtable['diag'].iloc[0:3]

# Exiobasetxt
start = time.time()
MRtable = importing('/Users/massimo/Documents/AAU/Research/Databases/exiobase v2.2.2/mrSUT_version2.2.2/mrSupply_version2.2.2.txt', 'exiobase')
print(start - time.time())
MRtable.info()
MRtable.iloc[0:3,0:3]

# Exiobasecsv
start = time.time()
MRtable = importing('/Users/massimo/Documents/AAU/Research/Databases/exiobase_vtext/test_csv_in_exiobase_format.csv', 'exiobase')
print(start - time.time())
MRtable.info()
MRtable.iloc[0:4,0:4]


#Export
MRtable = importing('/Users/massimo/Documents/AAU/Research/Databases/exiobase_vtext/test_csv_in_exiobase_format.csv', 'exiobase')

exporting(MRtable, 'MRtable_test.csv')

MRtable_reimport = importing('MRtable_test.csv', 'exiobase')
MRtable_reimport == MRtable

exporting(MRtable, 'MRtable_test.txt')

MRtable_reimport = importing('MRtable_test.txt', 'exiobase')
MRtable_reimport == MRtable

