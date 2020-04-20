#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pandas as pd
import statsmodels.api as sm

# 合并组别信息
with open('../result/classified.csv', 'r') as f:
    info = f.read()
info = info.replace("\n"," ")
info = info.split()
info = list(map(int,info))
data = pd.read_csv("../data/data_num.csv")
stkcd = data['Stkcd'].unique()
newinfo = pd.DataFrame(stkcd,columns=["Stkcd"])
newinfo['Group'] = info
data = data.merge(newinfo)

# 提取组的信息
groups = [data[data['Group'] == i] for i in range(1,6)]

# 回归
reg_info = ""
for i,group in enumerate(groups):
    x = group[["MV","RM","BM","ROE","Inv"]]
    y = group["Ret"]
    results = sm.OLS(y, x).fit()
    reg_info += "Group " + str(i+1) + "\n" +str(results.summary()) + "\n\n\n"

with open('../result/group_reg.txt','w') as f:
    print(reg_info,file=f)