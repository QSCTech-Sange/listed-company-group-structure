#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pandas as pd

RF = pd.read_table('TRD_Nrrate.csv',encoding='utf-16')
RF['Clsdt'] = RF['Clsdt'].apply(lambda x:x[:7])
RF.drop_duplicates(subset='Clsdt',keep='first',inplace=True)
RF.loc[:,'Clsdt'] = pd.to_datetime(RF.loc[:,'Clsdt'])
RF.columns=['Time','RF']
RF.to_csv("RF.csv")