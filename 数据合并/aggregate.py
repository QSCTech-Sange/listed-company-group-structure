#! usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd

# 读数据
BM = pd.read_csv("BM.csv")
Inv = pd.read_csv("Inv.csv")
MVret = pd.read_csv("MVret.csv")
ROE = pd.read_csv("ROE.csv")
RM = pd.read_csv("RM.csv")
RF = pd.read_csv("RF.csv")

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
allInfo.to_csv("data.csv",index=False)