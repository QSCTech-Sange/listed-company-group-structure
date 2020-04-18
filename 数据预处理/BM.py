#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pandas as pd
BM = pd.read_table('SRFR_Finidx.csv',encoding='utf-16')
BM.loc[:,'Accper'] = pd.to_datetime(BM.loc[:,'Accper'])
BM.columns=['Stkcd','Time','BM']
BM_count = BM['Stkcd'].value_counts()
BM = BM[BM['Stkcd'].isin(BM_count[BM_count == 10].index) == True]
BM.to_csv("BM.csv")