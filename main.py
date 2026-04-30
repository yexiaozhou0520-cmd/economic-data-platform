import streamlit as st
import pandas as pd
import plotly.express as px
from metrics import calculate_key_metrics, get_latest_indicators

# -------------------------- 页面基础设置 --------------------------
st.set_page_config(
    page_title="宏观经济数据看板",
    page_icon="📊",
    layout="wide"
)

# 页面标题
st.title("📊 中国宏观经济数据可视化看板")
st.markdown("---")

# -------------------------- 数据加载与处理 --------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/economic_data.csv")
    df = calculate_key_metrics(df)
    return df

df = load_data()
latest_df = get_latest_indicators(df)

# -------------------------- 侧边栏筛选器 --------------------------
st.sidebar.header("⚙️ 筛选面板")

# 指标选择
indicator_list = df["indicator"].unique().tolist()
selected_indicator = st.sidebar.selectbox("选择经济指标", indicator_list)

# 年份范围筛选
df["year"] = pd.to_datetime(df["date"]).dt.year
min_year, max_year = df["year"].min(), df["year"].max()
selected_year = st.sidebar.slider("选择年份范围", min_year, max_year, (min_year, max_year))

# -------------------------- 数据筛选（联动所有图表） --------------------------
filtered_df = df[
    (df["indicator"] == selected_indicator) &
    (df["year"] >= selected_year[0]) &
    (df["year"] <= selected_year[1])
]

# -------------------------- 关键指标卡片 --------------------------
st.subheader("📌 核心指标概览")
latest_data = latest_df[latest_df["indicator"] == selected_indicator].iloc[0]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("最新值", round(latest_data["value"], 2))
with col2:
    st.metric("同比增速", f"{round(latest_data['同比增速(%)'], 2)}%")
with col3:
    st.metric("3月均线", round(latest_data["3月均线"], 2))
with col4:
    st.metric("运行状态", latest_data["运行状态"])

st.markdown("---")

# -------------------------- 多图表联动展示 --------------------------
col_left, col_right = st.columns(2)

# 左侧：趋势线图
with col_left:
    st.subheader(f"{selected_indicator} 趋势变化")
    fig_line = px.line(
        filtered_df,
        x="date",
        y="value",
        title=f"{selected_indicator} 时间序列",
        labels={"value": "数值", "date": "日期"},
        template="plotly_white"
    )
    fig_line.update_layout(height=400)
    st.plotly_chart(fig_line, use_container_width=True)

# 右侧：同比增速柱状图
with col_right:
    st.subheader(f"{selected_indicator} 同比增速")
    fig_bar = px.bar(
        filtered_df,
        x="date",
        y="同比增速(%)",
        title=f"{selected_indicator} 同比增速变化",
        labels={"同比增速(%)": "增速(%)", "date": "日期"},
        template="plotly_white"
    )
    fig_bar.update_layout(height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# -------------------------- 原始数据表格 --------------------------
st.subheader("📋 原始数据明细")
st.dataframe(filtered_df[["date", "indicator", "value", "同比增速(%)", "环比变化", "运行状态"]], use_container_width=True)
