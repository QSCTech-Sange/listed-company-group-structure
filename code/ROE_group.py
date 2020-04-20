#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pandas as pd
import statsmodels.api as sm

with open('../result/classified.csv', 'r') as f:
    info = f.read()
info = info.replace("\n"," ")
info = info.split()
info = list(map(int,info))
data = pd.read_csv("../data/data_all.csv")
stkcd = data['Stkcd'].unique()
newinfo = pd.DataFrame(stkcd,columns=["Stkcd"])
newinfo['Group'] = info
data = data.merge(newinfo)


ROE_group = data[data['Group'] == 2]
other_group = data[data['Group'] != 2]

with open('../result/ROE_group.txt','w') as f:
    print("ROE Group describe" + "\n" + str(ROE_group.describe().T) + "\n\n\n",file=f)
    print("Other Group describe" + "\n" + str(other_group.describe().T) + "\n\n\n",file=f)
    print("ROE group company" + "\n" + str(pd.unique(ROE_group['Name'])) + "\n\n\n",file=f)
    print("ROE group industry" + "\n" + str(pd.unique(ROE_group['Name'])) + "\n\n\n",file=f)