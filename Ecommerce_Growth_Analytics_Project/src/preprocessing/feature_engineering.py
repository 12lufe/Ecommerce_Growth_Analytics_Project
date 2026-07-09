# src/preprocessing/feature_engineering.py

import pandas as pd
import numpy as np

class FeatureEngineering:
    def __init__(

        self,

        users_df,

        orders_df,

        products_df,

        behaviors_df

    ):

        self.users = users_df

        self.orders = orders_df

        self.products = products_df

        self.behaviors = behaviors_df

    # =====================
    # 用户特征
    # =====================

    def build_user_features(self):

        snapshot_date = self.orders[
            "order_date"
        ].max()

        user_feature = self.orders.groupby(

            "user_id"

        ).agg(

            total_spent=("actual_payment", "sum"),

            order_count=("order_id", "count"),

            avg_order_amount=(

                "actual_payment",

                "mean"

            ),

            last_order_date=(

                "order_date",

                "max"

            )

        ).reset_index()

        user_feature["days_since_last_order"] = (

            snapshot_date -

            user_feature["last_order_date"]

        ).dt.days

        behavior_feature = self.behaviors.pivot_table(

            index="user_id",

            columns="behavior_type",

            values="behavior_id",

            aggfunc="count",

            fill_value=0

        ).reset_index()

        user_feature = user_feature.merge(

            behavior_feature,

            on="user_id",

            how="left"

        )

        user_feature.fillna(0, inplace=True)

        return user_feature

    # =====================
    # 商品特徵
    # =====================

    def build_product_features(self):

        product_feature = self.orders.groupby(

            "product_id"

        ).agg(

            total_revenue=(

                "actual_payment",

                "sum"

            ),

            total_sales=(

                "quantity",

                "sum"

            ),

            avg_review_score=(

                "review_score",

                "mean"

            )

        ).reset_index()

        behavior_feature = self.behaviors.pivot_table(

            index="product_id",

            columns="behavior_type",

            values="behavior_id",

            aggfunc="count",

            fill_value=0

        ).reset_index()

        product_feature = product_feature.merge(

            behavior_feature,

            on="product_id",

            how="left"

        )

        product_feature.fillna(0, inplace=True)

        return product_feature

    # =====================
    # 流失标签
    # =====================

    def build_churn_dataset(self):

        user_feature = self.build_user_features()

        user_feature["churn"] = np.where(

            user_feature[

                "days_since_last_order"

            ] > 90,

            1,

            0

        )

        return user_feature
