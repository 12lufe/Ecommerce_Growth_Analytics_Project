# src/analysis/rfm_analysis.py

import pandas as pd

from src.database.data_loader import DataLoader


class RFMAnalysis:

    def __init__(self):

        loader = DataLoader()
        self.orders = loader.load_orders()

    def _clean_columns(self, df):
        """去除列名中的 BOM 头（\ufeff）和前后空格"""
        df.columns = [col.replace("\ufeff", "").strip() for col in df.columns]
        return df

    def _convert_dtypes(self, df):
        """将数值列转为 pandas 数值类型"""
        numeric_cols = [
            'quantity', 'unit_price', 'total_amount',
            'discount', 'actual_payment', 'review_score'
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    def build_rfm(self):

        print("🔧 清洗前的列名:", list(self.orders.columns))
        self.orders = self._clean_columns(self.orders)
        self.orders = self._convert_dtypes(self.orders)
        print(" 清洗后的列名:", list(self.orders.columns))
        print(" 数据类型:\n", self.orders.dtypes)

        # 确保日期列存在且是 datetime
        if 'order_date' not in self.orders.columns:
            raise KeyError("列名中缺少 'order_date'，请检查清洗是否成功。")

        self.orders["order_date"] = pd.to_datetime(
            self.orders["order_date"]
        )

        snapshot_date = (
            self.orders["order_date"].max()
            + pd.Timedelta(days=1)
        )

        rfm = self.orders.groupby(
            "user_id"
        ).agg({

            "order_date":
                lambda x:
                (snapshot_date - x.max()).days,

            "order_id":
                "count",

            "actual_payment":
                "sum"

        })

        rfm.columns = [

            "Recency",

            "Frequency",

            "Monetary"

        ]

        return rfm

    def score_rfm(self, rfm):

        rfm["R_score"] = pd.qcut(
            rfm["Recency"],
            5,
            labels=[5,4,3,2,1]
        )

        rfm["F_score"] = pd.qcut(
            rfm["Frequency"].rank(
                method="first"
            ),
            5,
            labels=[1,2,3,4,5]
        )

        rfm["M_score"] = pd.qcut(
            rfm["Monetary"],
            5,
            labels=[1,2,3,4,5]
        )

        rfm["RFM_SCORE"] = (

            rfm["R_score"].astype(str)

            +

            rfm["F_score"].astype(str)

            +

            rfm["M_score"].astype(str)

        )

        return rfm

    def customer_segment(self, rfm):

        rfm["segment"] = "普通用户"

        rfm.loc[
            rfm["RFM_SCORE"] == "555",
            "segment"
        ] = "冠军用户"

        rfm.loc[
            rfm["Monetary"] >
            rfm["Monetary"].quantile(0.8),
            "segment"
        ] = "高价值用户"

        return rfm

    def run(self):
        rfm = self.build_rfm()
        rfm = self.score_rfm(rfm)
        rfm = self.customer_segment(rfm)
        print(rfm.head())

        import os
        os.makedirs("data/processed", exist_ok=True)
        rfm.to_csv("data/processed/rfm_result.csv", encoding="utf-8-sig")