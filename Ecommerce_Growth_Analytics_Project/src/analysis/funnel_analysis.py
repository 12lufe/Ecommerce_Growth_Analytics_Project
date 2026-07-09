# src/analysis/funnel_analysis.py

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
import os
from src.database.data_loader import DataLoader


class FunnelAnalysis:

    def __init__(self):

        loader = DataLoader()

        # 加载原始数据
        behaviors_raw = loader.load_user_behaviors()
        orders_raw = loader.load_orders()

        # 清洗列名和转换类型
        self.behaviors = self._clean_columns(behaviors_raw)
        self.orders = self._clean_columns(orders_raw)
        self.behaviors = self._convert_dtypes(self.behaviors)
        self.orders = self._convert_dtypes(self.orders)

    def _clean_columns(self, df):
        """去除列名中的 BOM 头（\ufeff）和前后空格"""
        df.columns = [col.replace("\ufeff", "").strip() for col in df.columns]
        return df

    def _convert_dtypes(self, df):
        """将数值列转为 pandas 数值类型"""
        numeric_cols = [
            'quantity', 'unit_price', 'total_amount',
            'discount', 'actual_payment', 'review_score',
            'price', 'sales_count', 'duration_seconds'
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    # =====================
    # 漏斗统计
    # =====================

    def build_funnel(self):

        # 各阶段独立用户集合
        view = set(self.behaviors[self.behaviors["behavior_type"] == "浏览"]["user_id"])
        click = set(self.behaviors[self.behaviors["behavior_type"] == "点击"]["user_id"])
        favorite = set(self.behaviors[self.behaviors["behavior_type"] == "收藏"]["user_id"])
        cart = set(self.behaviors[self.behaviors["behavior_type"] == "加购"]["user_id"])

        order = set(self.orders["user_id"])
        paid = set(self.orders[self.orders["order_status"].isin(["已付款", "已发货", "已收货", "已完成"])]["user_id"])
        complete = set(self.orders[self.orders["order_status"] == "已完成"]["user_id"])

        # 路径漏斗：逐步取交集
        stage1_view = view  # 浏览
        stage2_click = view & click  # 浏览 → 点击
        stage3_favorite = view & click & favorite  # 浏览 → 点击 → 收藏
        stage4_cart = view & click & favorite & cart  # 浏览 → 点击 → 收藏 → 加购
        stage5_order = view & click & favorite & cart & order  # 浏览 → ... → 加购 → 下单
        stage6_paid = view & click & favorite & cart & order & paid  # +付款
        stage7_complete = view & click & favorite & cart & order & paid & complete  # +完成

        funnel = pd.DataFrame({
            "stage": ["浏览", "点击", "收藏", "加购", "下单", "付款", "完成"],
            "count": [
                len(stage1_view),
                len(stage2_click),
                len(stage3_favorite),
                len(stage4_cart),
                len(stage5_order),
                len(stage6_paid),
                len(stage7_complete)
            ]
        })

        return funnel

    # =====================
    # 转化率
    # =====================

    def calculate_conversion(self):

        funnel = self.build_funnel()

        funnel["conversion_rate"] = (

            funnel["count"]

            /

            funnel["count"].shift(1)

        )

        funnel.loc[0, "conversion_rate"] = 1

        funnel["conversion_rate"] = (

            funnel["conversion_rate"]

            * 100

        ).round(2)

        return funnel

    # =====================
    # 漏斗图
    # =====================

    def plot_funnel(self):

        funnel = self.calculate_conversion()
        plt.figure(figsize=(10, 6))
        plt.bar(funnel["stage"], funnel["count"], color='skyblue')
        plt.title("E-commerce Funnel Analysis")
        plt.xlabel("阶段")
        plt.ylabel("用户数")
        for i, v in enumerate(funnel["count"]):
            plt.text(i, v + 0.5, str(v), ha='center', va='bottom')
        plt.tight_layout()

        # 确保目录存在
        os.makedirs("reports/figures", exist_ok=True)
        save_path = "reports/figures/funnel_conversion.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()

    # =====================
    # 保存
    # =====================

    def save_result(self):

        funnel = self.calculate_conversion()

        os.makedirs("data/processed", exist_ok=True)
        save_path = "data/processed/funnel_result.csv"
        funnel.to_csv(save_path, index=False, encoding="utf-8-sig")

    # =====================
    # 执行
    # =====================

    def run(self):

        funnel = self.calculate_conversion()

        print(funnel)

        self.plot_funnel()

        self.save_result()


if __name__ == "__main__":

    FunnelAnalysis().run()