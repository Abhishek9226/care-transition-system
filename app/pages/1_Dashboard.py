import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", layout="wide")

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

    df["date"] = pd.to_datetime(df["date"], format="%B %d, %Y")

    cols = df.columns[1:]
    for col in cols:
        df[col] = df[col].astype(str).str.replace(",", "")
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.ffill()

    # KPIs
    df["transfer_efficiency"] = df["cbp_transferred"] / df["cbp_in_custody"]
    df["discharge_effectiveness"] = df["hhs_discharged"] / df["hhs_in_care"]
    df["backlog"] = df["cbp_apprehended"] - df["hhs_discharged"]
    df["total_load"] = df["cbp_in_custody"] + df["hhs_in_care"]

    return df

df = load_data()

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("⚙️ Control Panel")

start_date = st.sidebar.date_input("Start Date", df["date"].min())
end_date = st.sidebar.date_input("End Date", df["date"].max())

metric_option = st.sidebar.selectbox(
    "📊 Select Metric for Trend",
    ["backlog", "cbp_transferred", "hhs_discharged"]
)

# FILTER
df = df[(df["date"] >= pd.to_datetime(start_date)) &
        (df["date"] <= pd.to_datetime(end_date))]

# -------------------------------
# HEADER
# -------------------------------
st.title("📊 Care Transition Intelligence Dashboard")

# -------------------------------
# KPI CARDS
# -------------------------------
st.markdown("## 📌 Key Metrics")

def card(title, value, color):
    return f"""
    <div style="background:{color};padding:20px;border-radius:12px">
        <h4>{title}</h4>
        <h2>{value}</h2>
    </div>
    """

col1, col2, col3, col4 = st.columns(4)

col1.markdown(card("Transfer Efficiency", f"{df['transfer_efficiency'].mean():.2f}", "#1f77b4"), unsafe_allow_html=True)
col2.markdown(card("Discharge Effectiveness", f"{df['discharge_effectiveness'].mean():.2f}", "#2ca02c"), unsafe_allow_html=True)
col3.markdown(card("Avg Backlog", int(df["backlog"].mean()), "#ff7f0e"), unsafe_allow_html=True)
col4.markdown(card("Total Load", int(df["total_load"].mean()), "#9467bd"), unsafe_allow_html=True)

# -------------------------------
# INSIGHTS
# -------------------------------
st.markdown("### 📊 Smart Insights")

if df["transfer_efficiency"].mean() > 0.6:
    st.success("🚀 Transfer process is efficient")
else:
    st.warning("⚠️ Transfer efficiency needs improvement")

# -------------------------------
# TABS
# -------------------------------
tab1, tab2, tab3 = st.tabs(["📈 Trends", "📊 Distribution", "📋 Data"])

# -------------------------------
# TAB 1 (FIXED 🔥)
# -------------------------------
with tab1:
    colA, colB = st.columns(2)

    fig1 = px.line(
        df,
        x="date",
        y=metric_option,
        title=f"{metric_option} Trend",
        template="plotly_dark"
    )
    fig1.update_traces(line=dict(width=3))
    colA.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(
        df,
        x="date",
        y="cbp_transferred",
        title="Transfers Over Time",
        template="plotly_dark"
    )
    fig2.update_traces(line=dict(width=3))
    colB.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# TAB 2
# -------------------------------
with tab2:
    colC, colD = st.columns(2)

    fig3 = px.histogram(
        df,
        x=metric_option,
        nbins=50,
        title=f"{metric_option} Distribution",
        template="plotly_dark"
    )
    colC.plotly_chart(fig3, use_container_width=True)

    fig4 = px.box(
        df,
        y=metric_option,
        title=f"{metric_option} Spread",
        template="plotly_dark"
    )
    colD.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# TAB 3
# -------------------------------
with tab3:
    st.dataframe(df.tail(20), use_container_width=True)

# DOWNLOAD FEATURE 🔥
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Data",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

# -------------------------------
# SYSTEM STATUS
# -------------------------------
st.markdown("## ⚠️ System Health")

if df["backlog"].mean() > 0:
    st.error("🚨 Backlog increasing — Immediate action needed")
else:
    st.success("✅ System operating efficiently")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.caption("Built with Streamlit • Advanced Analytics Dashboard 🚀")