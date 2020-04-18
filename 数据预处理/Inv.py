#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pandas as pd
Asset = pd.read_table('FI_t8.csv',encoding='utf-16')
Asset.loc[:,'Accper'] = pd.to_datetime(Asset.loc[:,'Accper'])
Asset_count = Asset.loc[:,'Stkcd'].value_counts()
Asset = Asset[Asset['Stkcd'].isin(Asset_count[Asset_count > 75].index) == True]
Asset.columns=['Stkcd','Time','Asset']
Asset.to_csv("Inv.csv")