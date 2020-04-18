#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pandas as pd
import numpy as np

MVret = pd.read_table('SRFR_Amnthlyr.csv',encoding='utf-16')
MVret.loc[:,'Trdmnt'] = pd.to_datetime(MVret.loc[:,'Trdmnt'])
MVret.columns=['Stkcd','Time','MV','Ret']
MVret['MV'] = MVret['MV'].apply(np.log)
minMV = MVret['MV'].min()
maxMV = MVret['MV'].max()
MVret['MV'] = MVret['MV'].apply(lambda x:(x-minMV)/(maxMV-minMV))
MVret_count = MVret.loc[:,'Stkcd'].value_counts()
MVret = MVret[MVret['Stkcd'].isin(MVret_count[MVret_count == 120].index) == True]
MVret.to_csv("MVret.csv")