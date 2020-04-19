import pandas as pd
import statsmodels.api as sm

# 合并组别信息
with open('classified.csv', 'r') as f:
    info = f.read()
info = info.replace("\n"," ")
info = info.split()
info = list(map(int,info))
data = pd.read_csv("data.csv")
stkcd = data['Stkcd'].unique()
newinfo = pd.DataFrame(stkcd,columns=["Stkcd"])
newinfo['Group'] = info
data = data.merge(newinfo)

# 提取组的信息
groups = [data[data['Group'] == i] for i in range(5)]

# 回归
for group in groups:
    x = group[["MV","RM","BM","ROE","Inv"]]
    y = group["Ret"]
    results = sm.OLS(y, x).fit()
    print(results.summary())