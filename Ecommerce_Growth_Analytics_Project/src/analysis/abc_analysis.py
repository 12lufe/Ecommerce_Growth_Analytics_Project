# src/analysis/abc_analysis.py

import pandas as pd
import os
from src.database.data_loader import DataLoader
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class ABCAnalysis:

    def __init__(self):
        loader = DataLoader()
        self.orders = loader.load_orders()
        self.products = loader.load_products()

    def _clean_columns(self, df):
        """去除列名中的 BOM 头（\ufeff）和前后空格"""
        df.columns = [col.replace("\ufeff", "").strip() for col in df.columns]
        return df

    def _convert_dtypes(self, df):
        """将数值列转为 pandas 数值类型"""
        numeric_cols = [
            'quantity', 'unit_price', 'total_amount',
            'discount', 'actual_payment', 'review_score',
            'price', 'sales_count'  # products 表中的数值列
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    def build_abc(self):

        self.orders = self._clean_columns(self.orders)
        self.products = self._clean_columns(self.products)
        self.orders = self._convert_dtypes(self.orders)
        self.products = self._convert_dtypes(self.products)

        print("清洗后 orders 列名:", list(self.orders.columns))
        print("清洗后 products 列名:", list(self.products.columns))

        product_sales = (

            self.orders

            .groupby("product_id")

            ["actual_payment"]

            .sum()

            .reset_index()

        )

        merged = pd.merge(

            product_sales,

            self.products,

            on="product_id"

        )

        merged = merged.sort_values(

            by="actual_payment",

            ascending=False

        )

        merged["cum_ratio"] = (

            merged["actual_payment"]

            .cumsum()

            /

            merged["actual_payment"]

            .sum()

        )

        merged["ABC"] = "C"

        merged.loc[
            merged["cum_ratio"] <= 0.8,
            "ABC"
        ] = "A"

        merged.loc[
            (merged["cum_ratio"] > 0.8)
            &
            (merged["cum_ratio"] <= 0.95),
            "ABC"
        ] = "B"

        return merged

    def summary(self, abc):

        result = abc.groupby(

            "ABC"

        ).agg(

            商品数量=("product_id","count"),

            销售额=("actual_payment","sum")

        )

        return result

    def run(self):

        abc = self.build_abc()

        print(self.summary(abc))

        os.makedirs("data/processed", exist_ok=True)
        abc.to_csv(
            "data/processed/abc_result.csv",
            encoding="utf-8-sig",
            index=False
        )