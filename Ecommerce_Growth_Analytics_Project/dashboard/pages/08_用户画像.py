import streamlit as st
import plotly.express as px
from src.database.data_loader import DataLoader
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

st.title("👤 用户画像分析")

loader = DataLoader()

users = loader.load_users()

# 年龄

fig1 = px.histogram(
    users,
    x="age",
    title="年龄分布"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# 性别

gender = (
    users["gender"]
    .value_counts()
)

fig2 = px.pie(
    values=gender.values,
    names=gender.index,
    title="性别占比"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# 会员等级

member = (
    users["member_level"]
    .value_counts()
)

fig3 = px.bar(
    member,
    title="会员等级分布"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)