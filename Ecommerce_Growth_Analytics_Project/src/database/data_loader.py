import pandas as pd
from src.database.mysql_connect import read_sql_data

class DataLoader:
    def __init__(self):
        pass

    def _clean_columns(self, df):
        df.columns = [col.replace("\ufeff", "").strip() for col in df.columns]
        return df

    def _convert_dtypes(self, df):
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

    def load_users(self):
        sql = "SELECT * FROM users"
        df = read_sql_data(sql)
        df = self._clean_columns(df)
        df = self._convert_dtypes(df)
        return df

    def load_orders(self):
        sql = "SELECT * FROM orders"
        df = read_sql_data(sql)
        df = self._clean_columns(df)
        df = self._convert_dtypes(df)
        return df

    def load_products(self):
        sql = "SELECT * FROM products"
        df = read_sql_data(sql)
        df = self._clean_columns(df)
        df = self._convert_dtypes(df)
        return df

    def load_user_behaviors(self):
        sql = "SELECT * FROM user_behaviors"
        df = read_sql_data(sql)
        df = self._clean_columns(df)
        df = self._convert_dtypes(df)
        return df

    def load_user_features(self):
        sql = "SELECT * FROM user_features"
        df = read_sql_data(sql)
        df = self._clean_columns(df)
        df = self._convert_dtypes(df)
        return df

    def load_product_features(self):
        sql = "SELECT * FROM product_features"
        df = read_sql_data(sql)
        df = self._clean_columns(df)
        df = self._convert_dtypes(df)
        return df

    def load_all(self):
        return {
            "users": self.load_users(),
            "orders": self.load_orders(),
            "products": self.load_products(),
            "user_behaviors": self.load_user_behaviors(),
            "user_features": self.load_user_features(),
            "product_features": self.load_product_features()
        }

    def data_summary(self):
        data = self.load_all()
        summary = {}
        for name, df in data.items():
            summary[name] = {
                "rows": df.shape[0],
                "columns": df.shape[1]
            }
        return summary