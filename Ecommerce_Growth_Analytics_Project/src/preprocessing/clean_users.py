# src/preprocessing/clean_users.py

import pandas as pd
import numpy as np

class UserCleaner:
    def __init__(self, users_df):

        self.df = users_df.copy()

    def remove_duplicates(self):

        before = len(self.df)

        self.df = self.df.drop_duplicates()

        after = len(self.df)

        print(f"删除重复数据: {before-after}")

    def handle_missing_values(self):

        self.df["gender"] = self.df["gender"].fillna("未知")

        self.df["province"] = self.df["province"].fillna("未知")

        self.df["city"] = self.df["city"].fillna("未知")

        self.df["account_balance"] = self.df[
            "account_balance"
        ].fillna(0)

        self.df["credit_score"] = self.df[
            "credit_score"
        ].fillna(
            self.df["credit_score"].median()
        )

    def convert_datetime(self):

        self.df["registration_date"] = pd.to_datetime(

            self.df["registration_date"],

            errors="coerce"

        )

    def handle_age_outliers(self):

        self.df.loc[

            (self.df["age"] < 0)

            |

            (self.df["age"] > 100),

            "age"

        ] = np.nan

        self.df["age"] = self.df["age"].fillna(

            self.df["age"].median()

        )

    def clean(self):

        self.remove_duplicates()

        self.handle_missing_values()

        self.convert_datetime()

        self.handle_age_outliers()

        return self.df

