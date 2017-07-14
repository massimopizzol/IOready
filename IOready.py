#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 6 2017

@author: massimo
"""

import pandas as pd
import numpy as np


class IOready(object):

    """ Class for handling of Multi-Regional tables in Exiobase format

    Terminology
    ----------
    SUP : product (row) by activity (column) supply table
    USE : product (row) by activity (column) use table
    FD : product (row) by demand category (column) final demand table

    SUPsq : square supply table (same nr of products and activities)
    USEsq : square use table (same nr of products and activities)
    FDsq : final demand table with same nr of product rows as SUPsq and USEsq

    """


    def __init__(self, table=None, key=None, regs=None):
        """ Basic initialisation method

        Args:
            'table' (Dataframe, float): pd dataframe sized m * n
            'key' (list, int): m values for squaring e.g. [1,1,2,2,3]
            'regs' (int, int): nr of regions e.g. 47

       """

        self.table = table
        self.key = key
        self.regs = regs


    def indexing(self, mydata, c_rindex, n_rindex, u_rindex, c_cindex, n_cindex):
        
        mrindex = [np.array(c_rindex),
                   np.array(n_rindex),
                   np.array(u_rindex)]
        
        mcindex = [np.array(c_cindex),
                   np.array(n_cindex)]
        
        exio_format_table = pd.DataFrame(mydata.values, index = mrindex, columns = mcindex, dtype = float)
        exio_format_table.index.names = ['Reg','Prod','Unit']
        exio_format_table.columns.names = ['Reg','Act']

        return exio_format_table
    
    
    def build(self, table, rows, cols, units, regrows, regcols):

        """ Use this if the data are given in separate lists:
        country codes, product names, activities name, etc.
        Args:
            'table' (Dataframe, float): pd dataframe sized m * n
            'rows' (list, str): m names of rows e.g. ['barley','coal',..]
            'cols' (list, str): n names of columns e.g. ['barley production', ..]
            'units' (list, str): m units e.g. ['tonnes’,’euro’]
            'regrows' (list, str): m regions for rows e.g. ['AU','AU','AT',..]
            'regcols' (list, str): n regions for cols e.g. ['AU','AU','AT',..]

        Result: self.table is a multi-index dataframe

        """

        c_rindex = regrows
        n_rindex = rows
        u_rindex = units
        c_cindex = regcols
        n_cindex = cols
        mydata = table
        
        exio_format_table = self.indexing(mydata, c_rindex, n_rindex, u_rindex, c_cindex, n_cindex)
        
        self.table = exio_format_table
        
        if len(np.unique(self.table.index.get_level_values('Reg'))) == len(np.unique(self.table.columns.get_level_values('Reg'))):
            print("same nr regions in each dimension")
            self.regs = len(np.unique(self.table.index.get_level_values('Reg')))

        print(self.build.__name__, "IO table:",
              len(self.table.index.get_level_values('Reg')), "rows;",
              len(self.table.columns.get_level_values('Reg')), "columns")
        
        return self


    def fromtable(self, table):

        """  Use this if the 'table' is a pd.DataFrame object in Exiobase format:

        row 1: text, CountryCode
        row 2: text, IndustryTypename (or FinalDemandTypeName)
        column 1: text, CountryCode
        column 2: text, IndustryTypeName (or FinalDemandTypeName)
        column 3: text, UnitCode

        Result: self.table is a multi-index dataframe

        """

        c_rindex = table.iloc[2:,0]
        n_rindex = table.iloc[2:,1]
        u_rindex = table.iloc[2:,2]
        c_cindex = table.iloc[0,3:]
        n_cindex = table.iloc[1,3:]
        mydata = table.iloc[2:,3:]
        
        exio_format_table = self.indexing(mydata, c_rindex, n_rindex, u_rindex, c_cindex, n_cindex)
        
        self.table = exio_format_table
        
        if len(np.unique(self.table.index.get_level_values('Reg'))) == len(np.unique(self.table.columns.get_level_values('Reg'))):
            print("same nr regions in each dimension")
            self.regs = len(np.unique(self.table.index.get_level_values('Reg')))

        print(self.fromtable.__name__, "IO table:",
              len(self.table.index.get_level_values('Reg')), "rows;",
              len(self.table.columns.get_level_values('Reg')), "columns")
        
        return self
    
    def frommultidf(self, table):

        """  Use this if the 'table' is already a multi-index pd.DataFrame object 
        in the desired format 

        """
    
        self.table = table
        
        if len(np.unique(self.table.index.get_level_values('Reg'))) == len(np.unique(self.table.columns.get_level_values('Reg'))):
            print("same nr regions in each dimension")
            self.regs = len(np.unique(self.table.index.get_level_values('Reg')))

        print(self.frommultidf.__name__, "IO table:",
              len(self.table.index.get_level_values('Reg')), "rows;",
              len(self.table.columns.get_level_values('Reg')), "columns")
        
        return self


    def square(self, key):

        """ Use this after using the 'build' method (or 'fromtable')
        The original table is aggregated based on a key to give a smaller table
        The methos keeps columns fixed and aggregates rows
        e.g. aggregates from 12x10 to 10x10.
        However, it can also convert from 10x10 to 8x10 given the right key
        Thus, the result is not necessarily "square", just aggregated.

        Args:
            'key' (list, int): e.g. [1, 2, 2, 3, 4, 4, 5] defines groups of co-products
            e.g. 2 and 2 will be aggregated together and same for 4 and 4.

        WARNING: the new product name for the aggregated category is
        the name of the first product in the group of co-products

        WARNING: self.regs MUST be specified to use this method

        """
        # Square version of the product labels
        key = np.asarray(key)
        key_long = []
        while len(key_long) < len(key) * self.regs:
            key = key + len(key)
            key_long.extend(key)

        st_copy = self.table.copy()
        
        indf = pd.DataFrame(list(st_copy.index))
        indf['key'] = key_long
        indf = indf.drop_duplicates('key')
        
        st_copy['key'] = key_long
        st_copy.set_index('key', append=True, inplace=True)
        st_copy = st_copy.groupby(level='key', as_index = False).sum()
        #st_copy = st_copy.groupby('key').sum()
        nmrindex = [np.array(indf[0]),
                   np.array(indf[1]),
                   np.array(indf[2])]
        st_copy.index = nmrindex
        st_copy.index.names = ['Reg','Prod','Unit']
        
        self.table = st_copy

        print(self.square.__name__, "IO table:",
              len(self.table.index.get_level_values('Reg')), "rows;",
              len(self.table.columns.get_level_values('Reg')), "columns")
        
        return self

    
    def capital_gooding_CF(self, FD, capfor, FDpos, actpos):

        """A function to prepare table for integration of investments
        using the 'capital formation' method

         Args:
            'FD' (Class object): FD table
            'FDpos' (int): indicates the position
            of the finald demand category used for capital formation
            e.g. FDpos = 1 means second category
            'capfor' is the row in the VA extensinos table reporting the
            capital formation info, (e.g. the category 'w04a')
            'actpos' list with the positions of the region's columns

        WARNING: self.regs MUST be specified to use this method

        """

        # get section of capfor vector (i.e. one row of VA extension table)
        capfor_reg = np.array(capfor)[actpos].tolist()

        # get section of FD matrix (i.e. one country)
        FD_reg = FD.table[FDpos]

        # get section of USE matrix (i.e. one country)
        USE_reg = self.table[actpos]

        # get share of capital formation
        capfor_reg_share = np.array(capfor_reg)/np.array(sum(capfor_reg))
        capfor_reg_share = pd.DataFrame(capfor_reg_share, columns=['capfor_share'], index=USE_reg.columns).T

        # get investment matrix (GFCF * share of capital formation)
        Invest_reg = pd.DataFrame(np.dot(FD_reg, capfor_reg_share), columns=USE_reg.columns, index=USE_reg.index)

        # get USE matrix corrected for capital goods (USE + Investment)
        USEcg_reg = USE_reg + Invest_reg

        return USEcg_reg


    def integrate_inv_CF(self, FD, FDcat, VAact, VAname):

        """Integrate investments in the USE matrix using the 'capital formation' method

        Args:
            'FD' (Class object): FD table
            'FDcat' (string): indicates the name of the finald demand category used for capital formation
            'VAact' (Class object): VA extensions table (z factors * n activities)
            'VAname' (string) name of VA extension reporting the capital formation info, (e.g. the category 'w04a')

        Result: a new IOready object correcd for investments

        WARNING: self.regs MUST be specified to use this method

        """
        # get final demand cols of each region
        index_copy = VAact.table.index.copy()
        index_df = pd.DataFrame(index_copy.tolist()) 
        position = np.where(index_df[1] == VAname)
        capfor = VAact.table.loc[VAact.table.index[position[0][0]]]

        FDpos = FD.table.columns.get_level_values(1).unique().tolist().index(FDcat)
        FDpos = [FDpos]
        regs_FDpos = []
        Nr_FD_cats = len(FD.table.columns)//FD.regs
        while FDpos[-1] < len(FD.table.columns):
        
            regs_FDpos.append(FDpos)  # List of lists
            FDpos = [x + Nr_FD_cats for x in FDpos]
        
        # get activities of each region
        regs_actpos = []
        actpos = list(range(len(self.table.columns)//self.regs))  # // is integer division
        while actpos[-1] < len(self.table.columns):
        
            regs_actpos.append(actpos)  # List of lists
            actpos = [x + len(self.table.columns)//self.regs for x in actpos]

        # loop the capital gooding for each region, then put all together
        reg_list = []
        for FDpos, actpos in zip(regs_FDpos, regs_actpos):

            USEcg_sel = self.capital_gooding_CF(FD, capfor, FDpos, actpos)
            reg_list.append(USEcg_sel)

        USEcg = pd.concat(reg_list, axis=1)
        self.table = USEcg  # ;print(len(reg_list), 'regions') # Debug

        print(self.integrate_inv_CF.__name__, "IO table:",
              len(self.table.index.get_level_values('Reg')), "rows;",
              len(self.table.columns.get_level_values('Reg')), "columns")
        
        return self
