# 📊 电商增长分析系统

> 基于 Python + MySQL + Streamlit 构建的电商用户增长与商品价值分析平台

![Python](https://img.shields.io/badge/Python-3.11-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Pandas](https://img.shields.io/badge/Pandas-2.x-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-yellow)

---

## 📖 项目简介

本项目模拟电商平台真实业务场景，基于 **Python + MySQL + Streamlit** 构建了一套完整的用户增长分析系统。项目覆盖了从数据仓库设计、ETL、特征工程，到多维度业务分析、机器学习建模及可视化看板的完整数据闭环。

核心目标：通过数据分析与建模，识别高价值用户、核心商品、转化瓶颈及流失风险，为运营策略提供量化决策依据。

---

## 🚀 技术栈

| 层级 | 技术 |
|------|------|
| 数据库 | MySQL 8.0 |
| 数据处理 | Python (Pandas, NumPy) |
| 可视化 | Matplotlib, Plotly, Streamlit |
| 机器学习 | Scikit-learn (Logistic Regression) |
| 分析模型 | RFM, ABC, 漏斗分析, 流失预测 |

---

## 📂 项目结构

```
Ecommerce_Growth_Analytics_Project/
│
├── data/
│   ├── processed/                # 分析结果数据集
│   │   ├── rfm_result.csv        # RFM 评分结果
│   │   ├── abc_result.csv        # ABC 商品分类结果
│   │   ├── funnel_result.csv     # 转化漏斗数据
│   │   ├── churn_dataset.csv     # 流失预测特征集
│   │   └── product_association.csv # 商品关联规则（示例）
│   └── raw/                      # 原始数据（模拟或从 MySQL 抽取）
│
├── src/
│   ├── database/                 # 数据库连接与数据加载
│   │   ├── config.py             # MySQL 配置
│   │   ├── mysql_connect.py      # 连接与查询封装
│   │   └── data_loader.py        # 统一数据加载器（清洗、类型转换）
│   │
│   ├── preprocessing/            # 预处理与特征工程
│   │   ├── clean_orders.py
│   │   ├── clean_users.py
│   │   └── feature_engineering.py
│   │
│   ├── analysis/                 # 业务分析模块
│   │   ├── business_overview.py  # 经营概览（GMV、KPI、趋势）
│   │   ├── rfm_analysis.py       # RFM 用户价值分层
│   │   ├── abc_analysis.py       # ABC 商品价值分类
│   │   ├── funnel_analysis.py    # 用户转化漏斗
│   │   ├── product_association_analysis.py  # 商品关联分析
│   │   └── user_growth_analysis.py # 用户增长（新增/留存/复购）
│   │
│   └── models/                   # 机器学习模型
│       ├── churn_analysis.py     # 流失特征构建
│       └── logistic_regression.py # 逻辑回归训练与评估
│
├── dashboard/                    # Streamlit 应用页面
│   ├── streamlit_app.py          # 主入口
│   ├── 01_经营概览.py
│   ├── 02_用户价值分析.py
│   ├── 03_商品分析.py
│   ├── 04_商品关联分析.py
│   ├── 05_漏斗分析.py
│   ├── 06_用户增长分析.py
│   ├── 07_流失预测.py
│   └── 08_用户画像.py
│
├── reports/                      # 输出图表
│   └── figures/
│       ├── gmv_monthly_trend.png
│       ├── funnel_conversion.png
│       ├── growth_trend.png
│       └── churn_roc_curve.png
│
├── screenshots/                  # 项目截图（自行添加）
│
├── requirements.txt
└── README.md
```

---

## 📊 数据分析流程

```
MySQL 数据仓库
       ↓
DataLoader（统一加载 + 清洗）
       ↓
特征工程（用户/商品特征构建）
       ↓
    ┌──┼──┐
    ↓  ↓  ↓
经营分析  RFM  ABC
    ↓  ↓  ↓
    └──┼──┘
       ↓
   漏斗分析
       ↓
用户流失预测（逻辑回归）
       ↓
Streamlit Dashboard（交互式看板）
```

---

## 📈 核心功能模块

### 1️⃣ 经营概览

- **核心 KPI**：GMV、订单数、用户数、客单价
- **趋势分析**：月度 GMV 趋势图
- **商品排行**：销售额 Top 20 商品
- **省份分布**：销售额 Top 10 省份

### 2️⃣ 用户价值分析（RFM）

基于 **近度 (Recency)**、**频度 (Frequency)**、**金额 (Monetary)** 三维度，对用户进行 5 分位评分，并自动划分为：
- 冠军用户（555）
- 高价值用户（Monetary > 80% 分位）
- 普通用户

输出：
- RFM 评分表
- 用户分层占比图

### 3️⃣ 商品 ABC 分析

根据商品累计销售额贡献度分类：
- **A 类**：累计占比 ≤ 80%（核心商品）
- **B 类**：累计占比 80%~95%（潜力商品）
- **C 类**：累计占比 > 95%（长尾商品）

### 4️⃣ 用户转化漏斗

构建完整转化路径：
```
浏览 → 点击 → 收藏 → 加购 → 下单 → 付款 → 完成
```
计算每步转化率，定位流失最严重的环节。

### 5️⃣ 用户增长分析

- 月度新增用户趋势
- 月度活跃/付费用户数
- 复购率
- 月留存率

### 6️⃣ 用户流失预测

- **特征**：消费金额、订单频次、平均客单价、末次下单间隔、行为数据（加购/收藏/浏览/点击）
- **模型**：逻辑回归（Logistic Regression）
- **评估**：准确率、精确率、召回率、F1、ROC-AUC（AUC ≈ 0.78）
- **输出**：高风险流失用户列表

### 7️⃣ 商品关联分析

基于用户共购行为，挖掘频繁同时购买的商品对，输出支持度（Support）指标，可用于交叉销售推荐。

### 8️⃣ 用户画像

- 年龄分布直方图
- 性别占比饼图
- 会员等级分布柱状图

---

## 🖼 项目截图

（请自行替换为实际运行截图）

### Dashboard 首页
![Dashboard](screenshots/dashboard.png)

### 经营概览
![Business](screenshots/business.png)

### RFM 用户分层
![RFM](screenshots/rfm.png)

### ABC 商品分类
![ABC](screenshots/abc.png)

### 转化漏斗
![Funnel](screenshots/funnel.png)

### 流失预测 ROC 曲线
![ROC](screenshots/roc.png)

---

## 💻 如何运行

### 1. 克隆项目
```bash
git clone https://github.com/your-username/Ecommerce_Growth_Analytics_Project.git
cd Ecommerce_Growth_Analytics_Project
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置 MySQL 数据库
修改 `src/database/config.py` 中的连接信息：
```python
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "your_username",
    "password": "your_password",
    "database": "taobao_analysis",
    "charset": "utf8mb4"
}
```

### 4. 运行分析模块（可选）
```bash
# 经营分析
python -m src.analysis.business_overview

# RFM 分析
python -m src.analysis.rfm_analysis

# ABC 分析
python -m src.analysis.abc_analysis

# 漏斗分析
python -m src.analysis.funnel_analysis

# 流失特征构建
python -m src.analysis.churn_analysis

# 流失预测模型
python -m src.models.logistic_regression
```

### 5. 启动 Streamlit Dashboard
```bash
streamlit run dashboard/streamlit_app.py
```
浏览器打开 `http://localhost:8501` 即可访问。

---

## 📌 项目亮点

- ✅ **完整数据闭环**：从数据库抽取 → 清洗 → 特征工程 → 多维度分析 → 可视化展示
- ✅ **经典分析模型**：RFM、ABC、漏斗分析、逻辑回归流失预测
- ✅ **工程化代码结构**：模块化设计，易于扩展和维护
- ✅ **交互式 Dashboard**：Streamlit 实现，方便业务人员自助分析
- ✅ **真实业务场景**：模拟电商用户、订单、商品、行为数据，贴近实战

---

## 📚 项目参考

CSDN 文章：[链接](https://blog.csdn.net/your_article_link)

---

## 👨‍💻 Author

**叶梦思**  
吉首大学 · 软件工程  
