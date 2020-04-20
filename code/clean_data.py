#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pandas as pd
import numpy as np

directory = "../data/"

# 总市值和个股回报率，每月
MVret = pd.read_table(directory+'TRD_Mnth.csv',encoding='utf-16')
MVret.columns=['Stkcd','Time','MV','Ret']
MVret['MV'] = MVret['MV'].apply(np.log)
minMV = MVret['MV'].min()
maxMV = MVret['MV'].max()
MVret['MV'] = MVret['MV'].apply(lambda x:(x-minMV)/(maxMV-minMV))
MVret_count = MVret.loc[:,'Stkcd'].value_counts()
MVret = MVret[MVret['Stkcd'].isin(MVret_count[MVret_count > 110].index) == True]

# 市场回报率，每月
RM = pd.read_table(directory+'TRD_Mont.csv',encoding='utf-16')
RM = RM[RM['Markettype'] == 1]
RM = RM.loc[:,['Trdmnt','Mretwdos']]
RM.columns=['Time','RM']

# 无风险利率，每月
RF = pd.read_table(directory+'TRD_Nrrate.csv',encoding='utf-16')
RF['Clsdt'] = RF['Clsdt'].apply(lambda x:x[:7])
RF.drop_duplicates(subset='Clsdt',keep='first',inplace=True)
RF.columns=['Time','RF']
RF['RF'] = RF['RF'] / 100 

# 账面市值比，以年为单位
BM = pd.read_table(directory+'SRFR_Finidx.csv',encoding='utf-16')
BM.columns=['Stkcd','Year','BM']
BM['Year'] = BM['Year'].apply(lambda x:x[:4])
BM_count = BM.loc[:,'Stkcd'].value_counts()
BM = BM[BM['Stkcd'].isin(BM_count[BM_count > 9].index) == True]

# ROE，一年四次
ROE = pd.read_table(directory+'FI_T5.csv',encoding='utf-16')
ROE = ROE[ROE['Typrep'] == 'A']
ROE.drop('Typrep',axis=1,inplace=True)
ROE.columns=['Stkcd','Season','ROE']
ROE['Season'] = ROE['Season'].apply(lambda x:x[:7])
ROE_count = ROE.loc[:,'Stkcd'].value_counts()
ROE = ROE[ROE['Stkcd'].isin(ROE_count[ROE_count > 35].index) == True]

# 总资产增长率，一年四次
Inv = pd.read_table(directory+'FI_T8.csv',encoding='utf-16')
Inv = Inv[Inv['Typrep'] == 'A']
Inv.drop('Typrep',axis=1,inplace=True)
Inv.columns=['Stkcd','Season','Inv']
Inv['Season'] = Inv['Season'].apply(lambda x:x[:7])
Inv_count = Inv.loc[:,'Stkcd'].value_counts()
Inv = Inv[Inv['Stkcd'].isin(Inv_count[Inv_count > 35].index) == True]

# 公司信息
company = pd.read_table(directory+"STK_ListedCoInfoAnl.csv",encoding='utf-16')
company.columns=['Stkcd','Name','Industry']
company.drop_duplicates(subset=['Stkcd'],inplace=True)

# 把MVret,RM,RF 按照时间合并，这三者都是月度数据，好合
allInfo = RM.merge(RF,on='Time')
allInfo = MVret.merge(allInfo,on='Time')

# 提取年的数据，来合 BM
allInfo['Year'] = allInfo['Time'].apply(lambda x:x[:4])
BM['Year'] = BM['Year'].apply(lambda x:str(x))
BM = BM.dropna(axis = 0)

# 合 BM
allInfo = allInfo.merge(BM,on=['Year','Stkcd'])

# 提取季度数据，来合 Inv 与 ROE
def getSeason(x):
    year,month = x.split('-')
    month = int(month)
    if month in [12,11,10]:
        new_month = '12'
    elif month in [9,8,7]:
        new_month = '09'
    elif month in [6,5,4]:
        new_month = '06'
    else:
        new_month = '03'
    return year + '-' + new_month

allInfo['Season'] = allInfo['Time'].apply(getSeason)

# 合并 Inv 合 ROE
allInfo = allInfo.merge(ROE,on=['Stkcd','Season'])
allInfo = allInfo.merge(Inv,on=['Stkcd','Season'])

# 减去无风险收益
allInfo['Ret'] = allInfo['Ret'] - allInfo['RF']
allInfo['RM'] = allInfo['RM'] - allInfo['RF']

# 删除无用变量
allInfo.drop(['Year','Season','RF'],axis=1, inplace=True)

# 筛选空数据过多的变量
allInfo.dropna(axis = 0,inplace=True)
value_count = allInfo['Stkcd'].value_counts()
allInfo = allInfo[allInfo['Stkcd'].isin(value_count[value_count == 120].index) == True]

# 保存
allInfo.to_csv(directory+"data_num.csv",index=False)

# 和公司基本信息merge
allInfo = allInfo.merge(company,on='Stkcd')

# 保存
allInfo.to_csv(directory+"data_all.csv",index=False)
