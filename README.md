# 高盈利上市公司会带来高股价回报吗？基于机器学习的样本结构分解

毕业论文代码实现，便于分析和复现。

所有结果已经保存在 “result” 文件夹中，可以按照下面的指示进行复现。

## 安装包

使用 Python 来实现数据预处理和回归

```shell
pip install numpy
pip install pandas
pip install statsmodels
pip install linearmodels
```

使用 R  来进行 C-Lasso 分组

```
install.packages('devtools')
library(devtools)
devtools::install_github("zhan-gao/classo", INSTALL_opts=c("--no-multiarch"))
```

## 流程

1. 安装 Python 环境和 R 环境，安装上述包

2. 下载本仓库并进入本仓库文件夹

3. 数据来源于 csmar 数据库，由于数据存在版权原因不提供开放下载。请参考“data”文件夹下的 README.md 到 csmar 数据库下载相应数据。请准备好相应数据

4. 进入“代码”文件夹

   1. 执行 `clean_data.py`，会整理并合并出完整的数据，位于“data/data_all.csv”
   2. 执行 `reg.py`，会运行混合估计回归，固定效应回归以及控制行业的回归。在“result”文件夹里可以看到
      + correlation 相关系数矩阵
      + data_describe 描述性统计
      + fixed_effects 固定效应回归结果
      + industry_control 控制行业回归结果
      + pooled_reg 混合估计回归结果
      + VIF 用于判断多重共线性的 VIF 结果
5. 执行 `classify.R`，将调用 c-lasso 进行分组，分组结果保存在 “result/classified.csv”，这一步执行时间会比较长
6. 执行 `groupreg.py`，将调用分组结果进行回归，结果保存在 “result/group_reg.txt”
7. 执行 `ROE_group.py`，探索与盈利因子强相关的公司的特征，结果保存在 “result/ROE_group.txt”

> 所有的结果都是以 utf-8 编码储存