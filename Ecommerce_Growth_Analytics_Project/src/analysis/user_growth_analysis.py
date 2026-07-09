# src/analysis/user_growth_analysis.py

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
import os
from src.database.data_loader import DataLoader


class UserGrowthAnalysis:

    def __init__(self):

        loader = DataLoader()

        # 加载原始数据
        users_raw = loader.load_users()
        orders_raw = loader.load_orders()

        # 清洗列名和转换类型
        self.users = self._clean_columns(users_raw)
        self.orders = self._clean_columns(orders_raw)
        self.users = self._convert_dtypes(self.users)
        self.orders = self._convert_dtypes(self.orders)

        self.prepare_data()

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

    # ======================
    # 日期处理
    # ======================

    def prepare_data(self):

        self.users["registration_date"] = (

            pd.to_datetime(

                self.users["registration_date"]

            )

        )

        self.orders["order_date"] = (

            pd.to_datetime(

                self.orders["order_date"]

            )

        )

    # ======================
    # 月新增用户
    # ======================

    def monthly_new_users(self):

        df = self.users.copy()

        df["month"] = (

            df["registration_date"]

            .dt.to_period("M")

            .astype(str)

        )

        result = (

            df.groupby("month")

            ["user_id"]

            .count()

            .reset_index()

        )

        result.columns = [

            "month",

            "new_users"

        ]

        return result

    # ======================
    # 月活跃用户
    # ======================

    def monthly_active_users(self):

        df = self.orders.copy()

        df["month"] = (

            df["order_date"]

            .dt.to_period("M")

            .astype(str)

        )

        result = (

            df.groupby("month")

            ["user_id"]

            .nunique()

            .reset_index()

        )

        result.columns = [

            "month",

            "active_users"

        ]

        return result

    # ======================
    # 月付费用户
    # ======================

    def monthly_paid_users(self):

        paid_status = [

            "已付款",

            "已发货",

            "已收货",

            "已完成"

        ]

        df = self.orders[

            self.orders["order_status"]

            .isin(paid_status)

        ]

        df["month"] = (

            df["order_date"]

            .dt.to_period("M")

            .astype(str)

        )

        result = (

            df.groupby("month")

            ["user_id"]

            .nunique()

            .reset_index()

        )

        result.columns = [

            "month",

            "paid_users"

        ]

        return result

    # ======================
    # 复购率
    # ======================

    def repurchase_rate(self):

        user_orders = (

            self.orders

            .groupby("user_id")

            ["order_id"]

            .count()

        )

        repeat_users = (

            user_orders > 1

        ).sum()

        total_users = len(user_orders)

        return round(

            repeat_users

            / total_users

            * 100,

            2

        )

    # ======================
    # 用户留存率
    # ======================

    def retention_rate(self):

        self.orders["month"] = (

            self.orders["order_date"]

            .dt.to_period("M")

        )

        user_month = self.orders[

            ["user_id", "month"]

        ].drop_duplicates()

        retention = []

        months = sorted(

            user_month["month"]

            .unique()

        )

        for i in range(

            len(months) - 1

        ):

            current_users = set(

                user_month[

                    user_month["month"]

                    == months[i]

                ]["user_id"]

            )

            next_users = set(

                user_month[

                    user_month["month"]

                    == months[i+1]

                ]["user_id"]

            )

            rate = (

                len(

                    current_users

                    &

                    next_users

                )

                /

                len(current_users)

            )

            retention.append(

                [

                    str(months[i]),

                    round(rate*100,2)

                ]

            )

        return pd.DataFrame(

            retention,

            columns=[

                "month",

                "retention_rate"

            ]

        )

    # ======================
    # 可视化
    # ======================

    def plot_growth(self):

        df = self.monthly_new_users()
        if df.empty:
            print("没有月度新增用户数据")
            return
        plt.figure(figsize=(10, 5))
        plt.plot(df["month"], df["new_users"], marker="o", linestyle='-')
        plt.xticks(rotation=45)
        plt.title("Monthly New Users")
        plt.xlabel("月份")
        plt.ylabel("新增用户数")
        plt.tight_layout()
        os.makedirs("reports/figures", exist_ok=True)
        save_path = "reports/figures/growth_trend.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()

    # ======================
    # 执行
    # ======================

    def run(self):

        print(

            self.monthly_new_users()

        )

        print(

            self.monthly_active_users()

        )

        print(

            self.monthly_paid_users()

        )

        print(

            "复购率:",

            self.repurchase_rate(),

            "%"

        )

        print(

            self.retention_rate()

        )

        self.plot_growth()


if __name__ == "__main__":

    UserGrowthAnalysis().run()