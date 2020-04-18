#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pandas as pd
RM = pd.read_table('IDX_Idxtrdmth.csv',encoding='utf-16')
RM.loc[:,'Month'] = pd.to_datetime(RM.loc[:,'Month'])
RM = RM[RM['Indexcd'] == '000002']
RM = RM.loc[:,'Month':'Idxrtn']
RM.columns=['Time','RM']
RM.to_csv("RM.csv")