# 高盈利上市公司会带来高股价回报吗？基于机器学习的样本结构分解

毕业论文代码实现，便于分析和复现。

## 安装包

使用 Python 来实现数据预处理。

```shell
pip install numpy
pip install pandas
pip install statsmodels
pip install linearmodels
```

使用 R  来进行 C-Lasso 分组回归

```
install.packages('devtools')
library(devtools)
devtools::install_github("zhan-gao/classo", INSTALL_opts=c("--no-multiarch"))
```

## 流程

1. 数据预处理
2. 数据合并
3. 多元线性回归
4. 加入 C-Lasso 的分组回归

进入上面的文件夹并严格遵循其中的 README.md，即可复现得到结果。