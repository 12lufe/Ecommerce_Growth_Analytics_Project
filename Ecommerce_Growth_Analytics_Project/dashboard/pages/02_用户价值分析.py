import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

st.title("👤 用户价值分析")

rfm = pd.read_csv(
    "data/processed/rfm_result.csv"
)

st.dataframe(
    rfm.head(20)
)

segment_count = (
    rfm["segment"]
    .value_counts()
)

st.bar_chart(segment_count)

high_value = rfm[
    rfm["segment"]
    == "高价值用户"
]

ratio = (

    len(high_value)

    /

    len(rfm)

)

st.metric(

    "高价值用户占比",

    f"{ratio:.2%}"

)

segment_count = (
    rfm["segment"]
    .value_counts()
)

fig = px.pie(

    values=segment_count.values,

    names=segment_count.index,

    title="用户价值分层"

)

st.plotly_chart(
    fig,
    use_container_width=True
)