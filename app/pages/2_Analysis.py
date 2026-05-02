import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Advanced Analysis", layout="wide")

st.title("🚀 Advanced Analytics Engine")

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/HHS_Unaccompanied_Alien_Children_Program.csv")

    df.columns = [
        "date",
        "cbp_apprehended",
        "cbp_in_custody",
        "cbp_transferred",
        "hhs_in_care",
        "hhs_discharged"
    ]

    # 🔥 SAFE DATE CONVERSION (FIX)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    for col in df.columns[1:]:
        df[col] = df[col].astype(str).str.replace(",", "")
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.ffill()

    # KPIs
    df["transfer_efficiency"] = df["cbp_transferred"] / df["cbp_in_custody"]
    df["discharge_effectiveness"] = df["hhs_discharged"] / df["hhs_in_care"]
    df["backlog"] = df["cbp_apprehended"] - df["hhs_discharged"]

    return df

df = load_data()

# -------------------------------
# SIDEBAR CONTROLS
# -------------------------------
st.sidebar.header("⚙️ Advanced Controls")

metric = st.sidebar.selectbox(
    "📊 Select KPI",
    [
        "cbp_apprehended",
        "cbp_transferred",
        "hhs_discharged",
        "backlog",
        "transfer_efficiency",
        "discharge_effectiveness"
    ]
)

window = st.sidebar.slider("📉 Rolling Average Window", 3, 30, 7)

freq = st.sidebar.selectbox(
    "⏳ Time Aggregation",
    ["Daily", "Weekly", "Monthly"]
)

# -------------------------------
# TIME AGGREGATION (FIXED)
# -------------------------------
df_copy = df.copy()

# clean dates
df_copy["date"] = pd.to_datetime(df_copy["date"], errors="coerce")
df_copy = df_copy.dropna(subset=["date"])

# set index
df_copy = df_copy.set_index("date")

# 🔥 FINAL FIX HERE
if freq == "Weekly":
    df_copy = df_copy.resample("W").mean(numeric_only=True).reset_index()
elif freq == "Monthly":
    df_copy = df_copy.resample("M").mean(numeric_only=True).reset_index()
else:
    df_copy = df_copy.reset_index()

# -------------------------------
# TREND + SMOOTHING
# -------------------------------
st.subheader("📈 Trend Analysis")

df_copy["rolling_avg"] = df_copy[metric].rolling(window).mean()

fig = px.line(
    df_copy,
    x="date",
    y=[metric, "rolling_avg"],
    title=f"{metric} Trend with Rolling Average",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# MULTI KPI COMPARISON
# -------------------------------
st.subheader("📊 Multi KPI Comparison")

multi_fig = px.line(
    df_copy,
    x="date",
    y=["cbp_transferred", "hhs_discharged"],
    title="Transfers vs Discharges",
    template="plotly_dark"
)

st.plotly_chart(multi_fig, use_container_width=True)

# -------------------------------
# CORRELATION HEATMAP
# -------------------------------
st.subheader("🔥 Correlation Heatmap")

corr = df_copy.select_dtypes(include=np.number).corr()

plt.figure(figsize=(10,6))
sns.heatmap(corr, annot=True, cmap="coolwarm")

st.pyplot(plt)

# -------------------------------
# ANOMALY DETECTION 🚨
# -------------------------------
st.subheader("🚨 Anomaly Detection")

mean = df_copy[metric].mean()
std = df_copy[metric].std()

df_copy["anomaly"] = (
    (df_copy[metric] > mean + 2 * std) |
    (df_copy[metric] < mean - 2 * std)
)

anomaly_fig = px.scatter(
    df_copy,
    x="date",
    y=metric,
    color="anomaly",
    title="Anomaly Detection",
    template="plotly_dark"
)

st.plotly_chart(anomaly_fig, use_container_width=True)

# -------------------------------
# DISTRIBUTION ANALYSIS
# -------------------------------
st.subheader("📊 Distribution Analysis")

col1, col2 = st.columns(2)

hist = px.histogram(
    df_copy,
    x=metric,
    nbins=40,
    title="Distribution",
    template="plotly_dark"
)

box = px.box(
    df_copy,
    y=metric,
    title="Spread",
    template="plotly_dark"
)

col1.plotly_chart(hist, use_container_width=True)
col2.plotly_chart(box, use_container_width=True)

# -------------------------------
# SMART INSIGHTS ENGINE 🧠
# -------------------------------
st.subheader("🧠 AI Insights")

if df["transfer_efficiency"].mean() > 0.6:
    st.success("🚀 Transfer system is efficient")
else:
    st.warning("⚠️ Transfer efficiency is low")

if df["backlog"].mean() > 0:
    st.error("🚨 Backlog is increasing")
else:
    st.success("✅ Backlog under control")

if df[metric].std() > df[metric].mean():
    st.warning("⚠️ High variability detected in selected metric")

# -------------------------------
# DATA PREVIEW
# -------------------------------
st.subheader("📋 Data Snapshot")
st.dataframe(df_copy.tail(20), use_container_width=True)