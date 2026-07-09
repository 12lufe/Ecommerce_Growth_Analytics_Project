# src/analysis/business_overview.py

import pandas as pd
import os
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from src.database.data_loader import DataLoader


class BusinessOverview:

    def __init__(self):
        loader = DataLoader()
        # 加载原始数据
        orders_raw = loader.load_orders()
        products_raw = loader.load_products()
        # 强制清洗列名（去除 BOM 头和空格）
        self.orders = self._clean_columns(orders_raw)
        self.products = self._clean_columns(products_raw)
        # 关键：转换数据类型（将字符串转为数值）
        self.orders = self._convert_dtypes(self.orders)
        self.products = self._convert_dtypes(self.products)
        print("实际 orders 列名:", list(self.orders.columns))
        print("列名数量:", len(self.orders.columns))

    def _clean_columns(self, df):
        """去除列名中的 BOM 头（\ufeff）和前后空格"""
        df.columns = [col.replace("\ufeff", "").strip() for col in df.columns]
        return df

    def _convert_dtypes(self, df):
        """将数值列转为 pandas 数值类型（float/int），非数值保持原样"""
        # 针对 orders 表中的数值列
        numeric_cols = [
            'quantity', 'unit_price', 'total_amount',
            'discount', 'actual_payment', 'review_score'
        ]
        # 针对 products 表中的数值列
        if 'price' in df.columns:
            numeric_cols.append('price')
        if 'sales_count' in df.columns:
            numeric_cols.append('sales_count')

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    def calculate_kpi(self):

        paid_status = [
            "已付款",
            "已发货",
            "已收货",
            "已完成"
        ]

        paid_orders = self.orders[
            self.orders["order_status"].isin(paid_status)
        ]

        gmv = paid_orders["actual_payment"].sum()

        order_cnt = self.orders["order_id"].nunique()

        user_cnt = self.orders["user_id"].nunique()

        payment_rate = round(
            len(paid_orders) / len(self.orders) * 100,
            2
        )

        refund_rate = round(
            (self.orders["order_status"] == "已退款").mean() * 100,
            2
        )

        cancel_rate = round(
            (self.orders["order_status"] == "已取消").mean() * 100,
            2
        )

        aov = round(gmv / len(paid_orders), 2)

        print("GMV:", gmv)
        print("订单数:", order_cnt)
        print("用户数:", user_cnt)
        print("支付率:", payment_rate)
        print("退款率:", refund_rate)
        print("取消率:", cancel_rate)
        print("客单价:", aov)

    def monthly_gmv(self):

        self.orders["order_date"] = pd.to_datetime(
            self.orders["order_date"]
        )

        df = self.orders.copy()

        df["month"] = (
            df["order_date"]
            .dt.to_period("M")
            .astype(str)
        )

        result = (
            df.groupby("month")
            ["actual_payment"]
            .sum()
            .reset_index()
        )

        return result

    def top_products(self):

        merged = pd.merge(

            self.orders,

            self.products,

            on="product_id"

        )

        top10 = (
            merged
            .groupby("product_name")
            ["actual_payment"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        return top10

    def plot_gmv(self):
        trend = self.monthly_gmv()
        if trend.empty:
            print("没有月度数据可绘图")
            return

        latest_month = trend["month"].max()
        trend_filtered = trend[trend["month"] != latest_month]

        if trend_filtered.empty:
            print("过滤后没有完整月份数据可绘图")
            return

        plt.figure(figsize=(12, 5))
        plt.plot(trend_filtered["month"], trend_filtered["actual_payment"],
                 marker='o', linestyle='-', color='b', linewidth=2)
        plt.xticks(rotation=45)
        plt.title("Monthly GMV Trend (完整月份)", fontsize=14)
        plt.xlabel("月份", fontsize=12)
        plt.ylabel("GMV", fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()

        os.makedirs("reports/figures", exist_ok=True)
        save_path = "reports/figures/gmv_monthly_trend.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()

    def run(self):

        self.calculate_kpi()

        print("\nTop商品")

        print(self.top_products())

        self.plot_gmv()