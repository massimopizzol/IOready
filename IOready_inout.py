#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 14:18:10 2017

@author: massimo

Straight import of exiobase data
"""


import pandas as pd
import numpy as np


def importing(filename, celltype):

    '''
    Args:
    'filename' [string] name of the file...
    'celltype' [type of file], three values allowed:
        
        'single': text file (maybe generated from a simple Excel file) format:
            row 1: text,  anything, e.g. "CountryCode_ActivityTypeName"
            column 1: text, anything, e.g. "CountryCode_ProductTypeName"
        
        'multi': text file (maybe generated from a complex Excel file) where:
            row 2: float, total output per sector
            row 4: text, CountryCode
            row 5: text, ActivityTypeName
            column 1: text, CountryCode
            column 2: text, ProductTypeName
            column 5: text, UnitCode
    
        'exiobase': text file in exiobase format (used for SUP, USE, FD, emissions, resources):
            row 1: text, CountryCode
            row 2: text, ActivityTypename
            column 1: text, CountryCode (or Comparment)
            column 2: text, ProductTypeName (or Substance)
            column 3: text, UnitCode
            
        Setting any other value allows importing 
        exiobase format used for factors and materials, which is:
            row 1: text, CountryCode
            row 2: text, ActivityTypename
            column 2: text, PhysicalTypeName (or FactorInputTypeNamey)
            column 3: text, UnitCode
            
            The factor name will be listed in the first index level
            
            
    '''

    
    if celltype == "single" and filename[-3:] == "txt":

        print('Importing singletxt...')
        MRtable = pd.read_table(filename, header=0, index_col=0)
        MRtable = MRtable.astype(float)
        print('Done, this is NOT a multi-index pd.DataFrame object')

    elif celltype == "single" and filename[-3:] == "csv":

        print('Importing singlecsv...')
        MRtable = pd.read_csv(filename, header=0, index_col=0, sep=';')
        MRtable = MRtable.astype(float)
        print('Done, this is NOT a multi-index pd.DataFrame object')

    elif celltype == "multi" and filename[-3:] == "txt":

        print('Importing multitxt...')
        MRtable = pd.read_table(filename, header=None, dtype = object)
        
        c_cindex = MRtable.iloc[3,5:]
        n_cindex = MRtable.iloc[4,5:]
        mydata = MRtable.iloc[7:,5:]
        c_rindex = MRtable.iloc[7:,0]
        n_rindex = MRtable.iloc[7:,1]
        u_rindex = MRtable.iloc[7:,4]

        mrindex = [np.array(c_rindex),
                   np.array(n_rindex),
                   np.array(u_rindex)]
        
        mcindex = [np.array(c_cindex),
                   np.array(n_cindex)]
        
        exio_format_table = pd.DataFrame(mydata.values, index = mrindex, columns = mcindex, dtype = float)
        #exio_format_table.index.names = ['Reg','Prod','Unit']
        #exio_format_table.columns.names = ['Reg','Act']
        
        tot_output = MRtable.iloc[1,5:]        
        supply = pd.DataFrame(data=tot_output.T.values, columns=["Supply"],
                                index=mcindex, dtype=float).T
        #supply.columns.names = ['Reg','Act']
        
        MRtable =  {'table': exio_format_table, 'diag': supply }
        print('Done, this is a dict of: "table", "diag"')
        print('"table" is a multi-index pd.DataFrame object!')

    elif celltype == "multi" and filename[-3:] == "csv":

        print('Importing multicsv...')
        MRtable = pd.read_csv(filename, header=None, sep=';', dtype = object)

        c_cindex = MRtable.iloc[3,5:]
        n_cindex = MRtable.iloc[4,5:]
        mydata = MRtable.iloc[7:,5:]
        c_rindex = MRtable.iloc[7:,0]
        n_rindex = MRtable.iloc[7:,1]
        u_rindex = MRtable.iloc[7:,4]

        mrindex = [np.array(c_rindex),
                   np.array(n_rindex),
                   np.array(u_rindex)]
        
        mcindex = [np.array(c_cindex),
                   np.array(n_cindex)]
        
        exio_format_table = pd.DataFrame(mydata.values, index = mrindex, columns = mcindex, dtype = float)
        #exio_format_table.index.names = ['Reg','Prod','Unit']
        #exio_format_table.columns.names = ['Reg','Act']
        
        tot_output = MRtable.iloc[1,5:]        
        supply = pd.DataFrame(data=tot_output.T.values, columns=["Supply"],
                                index=mcindex, dtype=float).T
        #supply.columns.names = ['Reg','Act']
        
        MRtable =  {'table': exio_format_table, 'diag': supply }
        print('Done, this is a dict of: "table", "diag"')
        print('"table" is a multi-index pd.DataFrame object!')
        
    elif celltype == 'exiobase' and filename[-3:] == "txt":

        print('Importing exiobasetxt file...')
        MRtable = pd.read_table(filename, header = [0,1], index_col = [0,1,2], dtype = object)
        MRtable = MRtable.astype(float) # didn't work with read_table
        #MRtable.index.names = ['Reg','Prod','Unit']
        #MRtable.columns.names = ['Reg','Act']
        print('Done, this is a multi-index pd.DataFrame object!')

    elif celltype == 'exiobase' and filename[-3:] == "csv": # semicolon as separator!

        print('Importing exiobasecsv file...')
        MRtable = pd.read_csv(filename, header = [0,1], index_col = [0,1,2], sep = ";", dtype = object)
        MRtable = MRtable.astype(float)
        #MRtable.index.names = ['Reg','Prod','Unit']
        #MRtable.columns.names = ['Reg','Act']
        print('Done, this is a multi-index pd.DataFrame object!')
        
    elif celltype != 'exiobase' and celltype != 'single' and celltype != 'multi' and filename[-3:] == "txt":

        print('Importing extensiontxt file...')
        MRtable = pd.read_table(filename, header = [0,1], index_col = [0,1], dtype = object)
        MRtable = pd.read_csv(filename, header = [0,1], index_col = [0,1], sep = ";", dtype = object)
        MRtable = MRtable.astype(float) # didn't work with read_table
        MRtable['extension'] = celltype
        MRtable.set_index('extension', append=True, inplace=True)
        MRtable = MRtable.reorder_levels(['extension', 0, 1])
        MRtable.index.names = [None, None, None]
        print('Done, this is a multi-index pd.DataFrame object!')

    elif celltype != 'exiobase' and celltype != 'single' and celltype != 'multi' and filename[-3:] == "csv": # semicolon as separator!

        print('Importing extensioncsv file...')
        MRtable = pd.read_csv(filename, header = [0,1], index_col = [0,1], sep = ";", dtype = object)
        MRtable = MRtable.astype(float) # didn't work with read_table
        MRtable['extension'] = celltype
        MRtable.set_index('extension', append=True, inplace=True)
        MRtable = MRtable.reorder_levels(['extension', 0, 1])
        MRtable.index.names = [None, None, None]
        print('Done, this is a multi-index pd.DataFrame object!')

    return MRtable

def exporting(df, filename, exio = 'iotable'):
    
    '''Function to export to exiobase format
    because standard to_csv does not handle well the multi-index
    (or at least I could not figure out how to do that)
    Args:
    'df' [multi-index pd.DataFrame object] in the IOready.table format
    'filename' [text, string] e.g. "myexport.csv"
    '''
    
    one = pd.DataFrame([[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan]])
    two = pd.DataFrame(df.columns.tolist()).T
    two.reset_index(drop=True, inplace=True)
    three = pd.DataFrame(df.index.tolist())
    three.reset_index(drop=True, inplace=True)
    four = pd.DataFrame(df.values)
    five = pd.concat([one, two], axis = 1)
    six = pd.concat([three, four], axis = 1)
    seven = pd.concat([five, six], axis = 0)
    
    
    if exio == 'extension':
        seven = seven.drop(0,1)
    else:
        next
    
    if filename[-3:] == "csv":
        seven.to_csv(filename, index = False, header = False, sep = ";")
    elif filename[-3:] == "txt":
        seven.to_csv(filename, index = False, header = False, sep = '\t', mode = 'a')  # perfect!
