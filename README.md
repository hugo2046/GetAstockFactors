# GetAstockFactors

获取经典的多因子模型数据
数据来源：https://www.factorwar.com/data/factor-models/

**使用说明**

```
from GetAstockFactors import Get_FactorWar_Data

# 获取CAPM模型
gfd = Get_FactorWar_Data()

# 获取经典算法 频率使用日频
capm_daily_df: pd.DataFrame = gfd.get_model_data('CAPM模型','经典模型','daily')

# 获取极简算法 频率使用月频
capm_monthly_df: pd.DataFrame = gfd.get_model_data('CAPM模型','极简算法','monthly')

# 获取BetaPlus1000指数数据
betaplus1000: pd.DataFrame = gfd.gfd.get_betaplus1000()
```

**使用get_model_data方法可以获取以下模型：**

1. CAPM模型
2. Fama-French三因子模型
3. Carhart四因子模型
4. French五因子模型,Novy-Marx四因子模型
5. Hou-Xue-Zhang四因子模型
6. Stambaugh-Yuan四因子模型
7. Daniel-Hirshleifer-Sun三因子模型
8. BetaPlusA股混合四因子模型
9. 全部多因子模型basisportfolios月均收益率

**使用get_betaplus1000方法可以获得BetaPlus1000指数数据**

BetaPlus 1000指数系列包括BetaPlus 1000基准指数和7个BetaPlus 1000因子指数，旨在反应A股市场整体以及常见风格的风险收益特征。其涵盖的因子包括价值、盈利、成长、红利、低波动、规模以及动量。具体编制方案见[算法说明](https://www.factorwar.com/wp-content/uploads/2020/08/BetaPlus_Indexes_MethodologyNote_20200813.pdf)。

**数据说明：**
1. 如无特殊说明，多因子模型中因子收益率的起始日期为：1995 年 1 月 1 日。
2. 股票范围：全部在市股票，包括深圳主板、中小板和创业板，上海主板和科创板。
3. 剔除股票：剔除黑名单股票和不可交易股票，其中黑名单包括新股（上市不满 12 个月）、风险警示股、待退市股和净资产为负股，不可交易股票包括停牌股票和一字涨跌停股票。
4. 无风险收益率：不同时间段采用不同数据，具体如表1所示。
   表一：
   |时间区间|数据来源|
   |--|--|
   |2002/08/06之前|三个月期定期银行存款利率|
   |2002/08/07至2006/10/07|三个月期中央银行票据的票面利率|
   |2006/10/08至今|上海银行间三个月同业拆放利率|

5. 股票价格数据：后复权收盘价。
6. 用来构建因子的变量：如表2所示。
   表二：
   |因子|变量|
   |--|--|
   |规模|总市值，即收盘价乘以总股本|
   |价值|账面市值比（Book-to-Market ratio，简称 BM），即净资产除以总市值|
   |动量|过去 12 个月（剔除最近 1 个月）累计收益率，其中一个月包含21个交易日|
   |盈利|营业利润除以净资产|
   |投资|总资产增长率或净资产增长率|
   
   *不同版本的模型中，投资因子将使用总资产增长率或净资产增长率为变量来构建。*
   
# 经典版本与极简版本

在针对 A 股的实证研究中，本文档提供经典版本和极简版本两个多因子模型版本。经典版本又称为学术界版本，它严格按照关于多因子模型的学术论文中描述的方法选择因子变量，构建因子投资组合，计算因子收益率。极简版本是在经典版本的基础上，针对 A 股市场特点而开发的简化版多因子模型，一边更好的适应 A 股市场。经典版本和极简版本的主要差异包括：（1）经典版本严格遵循学术界惯例，因此因子投资组合每年再平衡；极简版本则按照业界惯例，因此因子投资组合每月再平衡，从而更快地利用最新的因子变量取值。（2）经典版本在构建因子投资组合时，往往采用市值和目标变量的双重排序；但在极简版本中，将使用因子变量单变量排序构建因子投资组合。

# 详细算法说明

[因子模型构建细节](https://www.factorwar.com/wp-content/uploads/2021/09/BetaPlus_FactorModels_MethodologyNote_20210904.pdf)
  
