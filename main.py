"""
Economic Data Platform - Initial Version (v1.0)
Macroeconomic Analysis Dashboard
Author: Your Name
Date: 2025-05-01
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_processor import load_and_clean_data

# Page configuration
st.set_page_config(
    page_title="Economic Data Platform",
    layout="wide",
    page_icon="📊"
)

# Title
st.title("Macroeconomic Data Analysis Platform")
st.subheader("Version 1.0 - Initial Release")

# Load data
df = load_and_clean_data("./data/economic_data.csv")

# Display dataset overview
st.markdown("### 1. Dataset Overview")
st.dataframe(df.head(10), use_container_width=True)

# Interactive time series plot
st.markdown("### 2. Indicator Trend Analysis")
indicator = st.selectbox("Select Economic Indicator", df.columns[1:])
fig = px.line(df, x="date", y=indicator, title=f"Time Series: {indicator}")
st.plotly_chart(fig, use_container_width=True)

# Correlation heatmap
st.markdown("### 3. Indicator Correlation Matrix")
corr_matrix = df.set_index("date").corr()
fig_corr = px.imshow(
    corr_matrix,
    text_auto=True,
    title="Correlation Heatmap",
    color_continuous_scale="RdBu"
)
st.plotly_chart(fig_corr, use_container_width=True)