# src/preprocessing/clean_orders.py

import pandas as pd
import numpy as np

class OrderCleaner:
    def __init__(self, orders_df):
        self.df = orders_df.copy()

    def remove_duplicates(self):

        before = len(self.df)

        self.df = self.df.drop_duplicates()

        after = len(self.df)

        print(f"删除重复订单: {before-after}")

    def handle_missing_values(self):

        num_cols = [

            "quantity",

            "unit_price",

            "total_amount",

            "discount",

            "actual_payment"

        ]

        for col in num_cols:

            self.df[col] = self.df[col].fillna(0)

        self.df["review_score"] = self.df[

            "review_score"

        ].fillna(

            self.df["review_score"].median()

        )

        self.df["review_content"] = self.df[

            "review_content"

        ].fillna("无评价")

    def convert_datetime(self):

        date_cols = [

            "order_date",

            "delivery_date",

            "receive_date"

        ]

        for col in date_cols:

            self.df[col] = pd.to_datetime(

                self.df[col],

                errors="coerce"

            )

    def handle_price_outliers(self):

        q1 = self.df["actual_payment"].quantile(0.25)

        q3 = self.df["actual_payment"].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr

        self.df = self.df[

            (self.df["actual_payment"] >= lower)

            &

            (self.df["actual_payment"] <= upper)

        ]

    def clean(self):

        self.remove_duplicates()

        self.handle_missing_values()

        self.convert_datetime()

        self.handle_price_outliers()

        return self.df
