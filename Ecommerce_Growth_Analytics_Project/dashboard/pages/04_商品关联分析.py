import streamlit as st
import pandas as pd
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

st.title("🔗 商品关联分析")

df = pd.read_csv(
    "data/processed/product_association.csv"
)

st.dataframe(
    df.head(30)
)