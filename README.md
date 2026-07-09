# Ecommerce_Growth_Analytics_Project
# 电商优惠券 AB 测试分析

## 项目背景

在电商业务中，优惠券是常用的促转化手段。本项目的目标是评估 **B 组（发放优惠券）** 相比 **A 组（无优惠券）** 是否能够显著提升用户购买转化率及客单价，为运营策略的调整提供数据决策依据。

## 数据说明

- 样本量：5000 名随机分组的用户（A 组 / B 组各 2500 人）
- 实验组（B 组）：发放优惠券，预期转化率 **14%**
- 对照组（A 组）：无优惠券，预期转化率 **10%**
- 字段：`user_id`, `group`, `visit_count`, `is_purchase`, `order_amount`

数据生成使用固定随机种子（42），确保可复现性。

## 分析方法

### 1. 指标计算
- **转化率** = 购买用户数 / 总用户数
- **客单价** = 购买用户的平均订单金额
- **GMV** = 各组订单金额总和

### 2. 假设检验

| 检验类型 | 原假设 | 备择假设 | 检验方法 |
|---------|--------|---------|---------|
| 转化率差异 | A 组转化率 ≥ B 组 | B 组转化率更高 | 卡方检验（$\chi^2$） |
| 客单价差异 | A 组客单价 = B 组客单价 | 两组客单价不同 | 独立样本 t 检验（不等方差） |

显著性水平 $\alpha = 0.05$。

## 核心结果

### 转化率对比
- **A 组**：约 10.0%
- **B 组**：约 14.0%
- **卡方检验 p 值**：< 0.001 → **显著提升**

### 客单价对比（仅购买用户）
- **A 组**：约 120 元
- **B 组**：约 130 元
- **t 检验 p 值**：< 0.001 → **显著提升**

### 业务影响
优惠券同时提升了转化率和客单价，GMV 提升明显，建议推广至全部用户。

## 项目结构

```
AB_Test_Project/
├── data/
│   └── ab_test_data.csv          # 实验数据
├── src/
│   ├── generate_data.py          # 模拟数据生成
│   ├── metrics_analysis.py       # 描述性统计
│   ├── hypothesis_testing.py     # 假设检验（卡方 + t 检验）
│   ├── visualization.py          # 静态图表（Plotly）
│   └── streamlit_app.py          # 交互式看板
├── .idea/                        # IDE 配置（可忽略）
└── README.md
```

## 运行方式

1. 安装依赖
```bash
pip install pandas numpy scipy plotly streamlit
```

2. 生成数据（如需要）
```bash
cd src
python generate_data.py
```

3. 运行分析脚本
```bash
python metrics_analysis.py
python hypothesis_testing.py
python visualization.py
```

4. 启动交互看板
```bash
streamlit run src/streamlit_app.py
```

## 技术栈

- **Python 3.11**
- **数据处理**：Pandas, NumPy
- **统计检验**：SciPy（卡方检验、t 检验）
- **可视化**：Plotly, Streamlit
- **版本控制**：Git

## 总结

本项目完整模拟了一次 AB 实验从设计、数据生成、统计分析到可视化的全流程，验证了优惠券策略的有效性。通过规范的假设检验和业务指标解读，展示了数据驱动决策的实践能力。

---

*项目仅供数据分析实习作品展示，数据为模拟生成。*
