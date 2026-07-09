import streamlit as st
from PIL import Image
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

st.title("📈 用户增长分析")

image = Image.open(
    "reports/figures/growth_trend.png"
)

st.image(
    image,
    use_container_width=True
)