import streamlit as st
from PIL import Image
import sys
import os
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

st.title("🤖 用户流失预测")

img = Image.open(
    "reports/figures/churn_roc_curve.png"
)

st.image(
    img,
    use_container_width=True
)

st.success(
    "逻辑回归模型完成用户流失预测"
)

df = pd.read_csv(
    "data/processed/churn_dataset.csv"
)

churn_users = df[
    df["churn"] == 1
]

st.subheader(
    "高风险流失用户"
)

st.dataframe(
    churn_users.head(100)
)