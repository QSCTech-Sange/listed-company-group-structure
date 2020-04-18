#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pandas as pd
import numpy as np

# 总市值和个股回报率，每月
MVret = pd.read_table('TRD_Mnth.csv',encoding='utf-16')
MVret.columns=['Stkcd','Time','MV','Ret']
MVret['MV'] = MVret['MV'].apply(np.log)
minMV = MVret['MV'].min()
maxMV = MVret['MV'].max()
MVret['MV'] = MVret['MV'].apply(lambda x:(x-minMV)/(maxMV-minMV))
MVret_count = MVret.loc[:,'Stkcd'].value_counts()
MVret = MVret[MVret['Stkcd'].isin(MVret_count[MVret_count > 110].index) == True]
MVret.to_csv("MVret.csv",index=False)

# 市场回报率，每月
RM = pd.read_table('TRD_Mont.csv',encoding='utf-16')
RM = RM[RM['Markettype'] == 1]
RM = RM.loc[:,['Trdmnt','Mretwdos']]
RM.columns=['Time','RM']
RM.to_csv("RM.csv",index=False)

# 无风险利率，每月
RF = pd.read_table('TRD_Nrrate.csv',encoding='utf-16')
RF['Clsdt'] = RF['Clsdt'].apply(lambda x:x[:7])
RF.drop_duplicates(subset='Clsdt',keep='first',inplace=True)
RF.columns=['Time','RF']
RF['RF'] = RF['RF'] / 100 
RF.to_csv("RF.csv",index=False)

# 账面市值比，以年为单位
BM = pd.read_table('SRFR_Finidx.csv',encoding='utf-16')
BM.columns=['Stkcd','Year','BM']
BM['Year'] = BM['Year'].apply(lambda x:x[:4])
BM_count = BM.loc[:,'Stkcd'].value_counts()
BM = BM[BM['Stkcd'].isin(BM_count[BM_count > 9].index) == True]
BM.to_csv('BM.csv',index=False)

# ROE，一年四次
ROE = pd.read_table('FI_T5.csv',encoding='utf-16')
ROE = ROE[ROE['Typrep'] == 'A']
ROE.drop('Typrep',axis=1,inplace=True)
ROE.columns=['Stkcd','Season','ROE']
ROE['Season'] = ROE['Season'].apply(lambda x:x[:7])
ROE_count = ROE.loc[:,'Stkcd'].value_counts()
ROE = ROE[ROE['Stkcd'].isin(ROE_count[ROE_count > 35].index) == True]
ROE.to_csv('ROE.csv',index=False)

# 总资产增长率，一年四次
Asset = pd.read_table('FI_T8.csv',encoding='utf-16')
Asset = Asset[Asset['Typrep'] == 'A']
Asset.drop('Typrep',axis=1,inplace=True)
Asset.columns=['Stkcd','Season','Inv']
Asset['Season'] = Asset['Season'].apply(lambda x:x[:7])
Asset_count = Asset.loc[:,'Stkcd'].value_counts()
Asset = Asset[Asset['Stkcd'].isin(Asset_count[Asset_count > 35].index) == True]
Asset.to_csv('Inv.csv',index=False)