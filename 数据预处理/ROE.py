#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pandas as pd

ROE = pd.read_table('FAR_Finidx.csv',encoding='utf-16')
ROE.loc[:,'Accper'] = pd.to_datetime(ROE.loc[:,'Accper'])
ROE_count = ROE.loc[:,'Stkcd'].value_counts()
ROE = ROE[ROE['Stkcd'].isin(ROE_count[ROE_count == 10].index) == True]
ROE.columns=['Stkcd','Time','ROE']
ROE.to_csv("ROE.csv")