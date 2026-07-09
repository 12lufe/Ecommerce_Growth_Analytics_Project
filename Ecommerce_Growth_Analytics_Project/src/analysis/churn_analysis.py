# src/analysis/churn_analysis.py

import pandas as pd
import numpy as np
import os
from src.database.data_loader import DataLoader
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class ChurnAnalysis:

    def __init__(self):

        loader = DataLoader()

        # 加载原始数据
        orders_raw = loader.load_orders()
        users_raw = loader.load_users()
        behaviors_raw = loader.load_user_behaviors()

        # 清洗列名和转换类型
        self.orders = self._clean_columns(orders_raw)
        self.users = self._clean_columns(users_raw)
        self.behaviors = self._clean_columns(behaviors_raw)
        self.orders = self._convert_dtypes(self.orders)
        self.users = self._convert_dtypes(self.users)
        self.behaviors = self._convert_dtypes(self.behaviors)

        self.preprocess()

    def _clean_columns(self, df):
        """去除列名中的 BOM 头（\ufeff）和前后空格"""
        df.columns = [col.replace("\ufeff", "").strip() for col in df.columns]
        return df

    def _convert_dtypes(self, df):
        """将数值列转为 pandas 数值类型"""
        numeric_cols = [
            'quantity', 'unit_price', 'total_amount',
            'discount', 'actual_payment', 'review_score',
            'price', 'sales_count', 'duration_seconds',
            'credit_score', 'account_balance'
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    # ==================================
    # 日期处理
    # ==================================

    def preprocess(self):

        self.orders["order_date"] = pd.to_datetime(
            self.orders["order_date"]
        )

        self.behaviors["behavior_time"] = pd.to_datetime(
            self.behaviors["behavior_time"]
        )

    # ==================================
    # 用户消费特征
    # ==================================

    def build_order_features(self):

        snapshot_date = self.orders[
            "order_date"
        ].max()

        order_feature = self.orders.groupby(
            "user_id"
        ).agg(

            total_spent=(
                "actual_payment",
                "sum"
            ),

            order_count=(
                "order_id",
                "count"
            ),

            avg_order_amount=(
                "actual_payment",
                "mean"
            ),

            last_order_date=(
                "order_date",
                "max"
            )

        ).reset_index()

        order_feature[
            "days_since_last_order"
        ] = (

            snapshot_date

            -

            order_feature[
                "last_order_date"
            ]

        ).dt.days

        return order_feature

    # ==================================
    # 用户行为特征
    # ==================================

    def build_behavior_features(self):

        behavior_feature = pd.pivot_table(

            self.behaviors,

            index="user_id",

            columns="behavior_type",

            values="behavior_id",

            aggfunc="count",

            fill_value=0

        )

        behavior_feature.reset_index(
            inplace=True
        )

        return behavior_feature

    # ==================================
    # 流失标签
    # ==================================

    def build_label(self, df):

        df["churn"] = np.where(

            df["days_since_last_order"]
            > 90,

            1,

            0

        )

        return df

    # ==================================
    # 构建训练集
    # ==================================

    def build_dataset(self):

        self.preprocess()

        order_feature = self.build_order_features()

        behavior_feature = self.build_behavior_features()

        dataset = pd.merge(

            order_feature,

            behavior_feature,

            on="user_id",

            how="left"

        )

        dataset.fillna(0, inplace=True)

        dataset = self.build_label(dataset)

        return dataset

    # ==================================
    # 保存数据
    # ==================================

    def save_dataset(self):
        dataset = self.build_dataset()
        # 确保目录存在
        os.makedirs("data/processed", exist_ok=True)
        save_path = "data/processed/churn_dataset.csv"
        dataset.to_csv(save_path, index=False, encoding="utf-8-sig")
        print(f"流失数据集已保存至: {save_path}")
        print("\n数据集预览（前5行）:")
        print(dataset.head())
        print(f"\n总样本量: {len(dataset)}")
        print(f"流失率: {dataset['churn'].mean() * 100:.2f}%")

    def run(self):

        self.save_dataset()


if __name__ == "__main__":

    ChurnAnalysis().run()