#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pandas as pd
from pandas.plotting import scatter_matrix
import statsmodels.formula.api as smf
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
import statsmodels.api as sm

data = pd.read_csv("../data/data_num.csv")

# 描述性统计
with open('../result/data_describe.txt','w') as f:
    print(data.describe().T,file=f)

# 相关系数矩阵
# scatter_matrix(
#     data.loc[,["Ret","MV","RM","BM","ROE","Inv"]],
#     figsize=(10,10),diagonal = 'kid'
# )
with open('../result/correlation.txt','w') as f:
    print(data[["Ret","MV","RM","BM","ROE","Inv"]].corr(),file=f)

# 计算五个变量的VIF
params = ["MV","RM","BM","ROE","Inv"]
VIF = {i:0 for i in params}
for i in range(5):
    x = params[:i] + params[i+1:]
    y = params[i]
    res = sm.OLS(data[y], data[x]).fit()
    VIF[y] = 1 / (1 - res.rsquared)
with open('../result/VIF.txt','w') as f:
    print(VIF,file=f)

# pooled 回归
x = data[["MV","RM","BM","ROE","Inv"]]
y = data["Ret"]
results = sm.OLS(y, x).fit()
with open('../result/pooled_reg.txt','w') as f:
    print(results.summary(),file=f)

# 固定效应回归
data['Time'] = pd.to_datetime(data['Time'])
data = data.set_index(['Stkcd','Time'])
dependent = data.Ret
exog = sm.add_constant(data[['MV','BM','RM','ROE','Inv']])
mod = PanelOLS(dependent, exog, entity_effects=True)
res = mod.fit(cov_type='clustered')
with open('../result/fixed_effects.txt','w') as f:
    print(res,file=f)

# 控制行业回归
data = pd.read_csv("../data/data_all.csv")
data['Time'] = pd.to_datetime(data['Time'])
data = data.set_index(['Industry','Time'])
dependent = data.Ret
exog = sm.add_constant(data[['MV','BM','RM','ROE','Inv']])
mod = PanelOLS(dependent, exog, entity_effects=True)
res = mod.fit(cov_type='clustered')
with open('../result/industry_control.txt','w') as f:
    print(res,file=f)