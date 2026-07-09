import streamlit as st
import pandas as pd
import plotly.express as px

from src.database.data_loader import DataLoader

st.set_page_config(layout="wide")

st.title("📈 电商经营概览")

loader = DataLoader()

orders = loader.load_orders()
users = loader.load_users()

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

# ===================
# 时间筛选器
# ===================

start_date = orders["order_date"].min()

end_date = orders["order_date"].max()

date_range = st.date_input(
    "选择时间范围",
    [start_date, end_date]
)

if len(date_range) == 2:

    orders = orders[
        (
            orders["order_date"]
            >= pd.to_datetime(date_range[0])
        )
        &
        (
            orders["order_date"]
            <= pd.to_datetime(date_range[1])
        )
    ]

# ===================
# KPI
# ===================

gmv = orders["actual_payment"].sum()

order_cnt = orders["order_id"].nunique()

user_cnt = orders["user_id"].nunique()

aov = gmv / order_cnt

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "GMV",
    f"¥{gmv:,.0f}"
)

col2.metric(
    "订单数",
    order_cnt
)

col3.metric(
    "用户数",
    user_cnt
)

col4.metric(
    "客单价",
    round(aov,2)
)

# ===================
# GMV趋势
# ===================

monthly = (
    orders
    .groupby(
        orders["order_date"].dt.to_period("M")
    )
    ["actual_payment"]
    .sum()
    .reset_index()
)

monthly["order_date"] = (
    monthly["order_date"]
    .astype(str)
)

fig = px.line(
    monthly,
    x="order_date",
    y="actual_payment",
    title="GMV趋势"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

province_sales = (

    orders.merge(
        users,
        on="user_id"
    )

    .groupby("province")

    ["actual_payment"]

    .sum()

    .sort_values(
        ascending=False
    )

    .head(10)

)

fig2 = px.bar(

    province_sales,

    title="省份销售TOP10"

)

st.plotly_chart(
    fig2,
    use_container_width=True
)

products = loader.load_products()

top_products = (

    orders.groupby("product_id")

    ["actual_payment"]

    .sum()

    .reset_index()

    .merge(
        products,
        on="product_id"
    )

    .sort_values(
        "actual_payment",
        ascending=False
    )

    .head(20)

)

st.subheader("🏆 商品销售排行榜")

st.dataframe(
    top_products[
        [
            "product_name",
            "actual_payment"
        ]
    ]
)