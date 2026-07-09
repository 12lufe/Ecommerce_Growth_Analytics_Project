import streamlit as st
import pandas as pd
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

st.title("🔻 漏斗分析")

funnel = pd.read_csv(
    "data/processed/funnel_result.csv"
)

st.dataframe(funnel)

st.bar_chart(
    funnel.set_index("stage")["count"]
)