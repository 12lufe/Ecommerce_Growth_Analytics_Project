# src/analysis/product_association_analysis.py

import pandas as pd
import os
from itertools import combinations
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from src.database.data_loader import DataLoader


class ProductAssociationAnalysis:

    def __init__(self):

        loader = DataLoader()
        # 加载原始数据
        orders_raw = loader.load_orders()
        products_raw = loader.load_products()

        # 清洗列名和转换类型
        self.orders = self._clean_columns(orders_raw)
        self.products = self._clean_columns(products_raw)
        self.orders = self._convert_dtypes(self.orders)
        self.products = self._convert_dtypes(self.products)

    def _clean_columns(self, df):
        """去除列名中的 BOM 头（\ufeff）和前后空格"""
        df.columns = [col.replace("\ufeff", "").strip() for col in df.columns]
        return df

    def _convert_dtypes(self, df):
        """将数值列转为 pandas 数值类型"""
        numeric_cols = [
            'quantity', 'unit_price', 'total_amount',
            'discount', 'actual_payment', 'review_score',
            'price', 'sales_count'
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    # ======================
    # 用户购买商品集合
    # ======================

    def build_user_product_set(self):

        user_product = (

            self.orders

            .groupby("user_id")["product_id"]

            .apply(set)

            .reset_index()

        )

        return user_product

    # ======================
    # 商品共购统计
    # ======================

    def generate_pairs(self):

        user_product = self.build_user_product_set()

        pair_count = {}

        for products in user_product["product_id"]:

            if len(products) < 2:

                continue

            for pair in combinations(
                sorted(products),
                2
            ):

                pair_count[pair] = (

                    pair_count.get(pair, 0) + 1

                )

        result = pd.DataFrame(

            [

                [k[0], k[1], v]

                for k, v in pair_count.items()

            ],

            columns=[

                "product_A",

                "product_B",

                "co_purchase_count"

            ]

        )

        return result

    # ======================
    # 支持度
    # ======================

    def calculate_support(self, df):

        total_users = self.orders[
            "user_id"
        ].nunique()

        df["support"] = (

            df["co_purchase_count"]

            / total_users

        )

        return df

    # ======================
    # 商品名称映射
    # ======================

    def add_product_name(self, df):

        product_map = dict(

            zip(

                self.products["product_id"],

                self.products["product_name"]

            )

        )

        df["product_A_name"] = (

            df["product_A"]

            .map(product_map)

        )

        df["product_B_name"] = (

            df["product_B"]

            .map(product_map)

        )

        return df

    # ======================
    # Top关联商品
    # ======================

    def top_pairs(self):

        result = self.generate_pairs()

        result = self.calculate_support(result)

        result = self.add_product_name(result)

        result = result.sort_values(

            by="co_purchase_count",

            ascending=False

        )

        return result.head(20)

    # ======================
    # 保存结果
    # ======================

    def save_result(self):

        result = self.top_pairs()

        os.makedirs("data/processed", exist_ok=True)
        result.to_csv(
            "data/processed/product_association.csv",
            index=False,
            encoding="utf-8-sig"
        )

    # ======================
    # 执行
    # ======================

    def run(self):

        result = self.top_pairs()

        print(result)

        self.save_result()


if __name__ == "__main__":

    ProductAssociationAnalysis().run()