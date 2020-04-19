import pandas as pd
import matplotlib
from pandas.plotting import scatter_matrix
import statsmodels.formula.api as smf
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
import statsmodels.api as sm
font = {
    'family':'SimHei'
}
matplotlib.rc('font',**font)

data = pd.read_csv("data.csv")

# 描述性统计
data.describe().T

# 相关系数矩阵
scatter_matrix(
    data.loc[:500,["Ret","MV","RM","BM","ROE","Inv"]],
    figsize=(10,10),diagonal = 'kid'
)
data[["Ret","MV","RM","BM","ROE","Inv"]].corr()

# 计算五个变量的VIF
params = ["MV","RM","BM","ROE","Inv"]
VIF = []
for i in range(5):
    x = params[:i] + params[i+1:]
    y = params[i]
    res = sm.OLS(data[y], data[x]).fit()
    VIF.append(1 / (1 - res.rsquared))
print(VIF)

# pooled 回归
x = data[["MV","RM","BM","ROE","Inv"]]
y = data["Ret"]
results = sm.OLS(y, x).fit()
results.summary()

# 固定效应回归
data = pd.read_csv("data.csv") 
data['Time'] = pd.to_datetime(data['Time'])
data = data.set_index(['Stkcd','Time'])
dependent = data.Ret
exog = sm.add_constant(data[['MV','BM','RM','ROE','Inv']])
mod = PanelOLS(dependent, exog, entity_effects=True)
res = mod.fit(cov_type='clustered')
print(res)