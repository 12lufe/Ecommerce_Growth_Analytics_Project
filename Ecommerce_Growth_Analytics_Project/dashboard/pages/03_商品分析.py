import streamlit as st
import pandas as pd
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

st.title("📦 商品ABC分析")

abc = pd.read_csv(
    "data/processed/abc_result.csv"
)

st.dataframe(
    abc.head(20)
)

st.bar_chart(
    abc["ABC"]
    .value_counts()
)