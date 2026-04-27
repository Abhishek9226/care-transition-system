import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

st.set_page_config(page_title="AI Predictions", layout="wide")

st.title("🤖 Advanced AI Forecasting Engine")

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

    for col in df.columns[1:]:
        df[col] = df[col].astype(str).str.replace(",", "")
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.ffill()
    df["backlog"] = df["cbp_apprehended"] - df["hhs_discharged"]

    return df

df = load_data().sort_values("date")

# -------------------------------
# SIDEBAR CONTROLS
# -------------------------------
st.sidebar.header("⚙️ Prediction Controls")

target = st.sidebar.selectbox(
    "📊 Target Metric",
    ["cbp_transferred", "hhs_discharged", "backlog"]
)

model_type = st.sidebar.selectbox(
    "🤖 Model Type",
    ["Linear Regression", "Polynomial Regression"]
)

future_days = st.sidebar.slider("📅 Forecast Days", 7, 90, 30)

noise_level = st.sidebar.slider("📉 Confidence Band Width", 5, 50, 15)

# -------------------------------
# PREPARE DATA
# -------------------------------
df["time_index"] = np.arange(len(df))
X = df[["time_index"]]
y = df[target]

# -------------------------------
# MODEL SELECTION
# -------------------------------
if model_type == "Linear Regression":
    model = LinearRegression()
    model.fit(X, y)
    preds = model.predict(X)

else:
    poly = PolynomialFeatures(degree=3)
    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, y)
    preds = model.predict(X_poly)

# -------------------------------
# MODEL PERFORMANCE
# -------------------------------
score = r2_score(y, preds)

# -------------------------------
# FUTURE PREDICTIONS
# -------------------------------
future_index = np.arange(len(df), len(df) + future_days).reshape(-1, 1)

if model_type == "Polynomial Regression":
    future_index_transformed = poly.transform(future_index)
    future_preds = model.predict(future_index_transformed)
else:
    future_preds = model.predict(future_index)

future_dates = pd.date_range(
    start=df["date"].max(),
    periods=future_days + 1
)[1:]

# -------------------------------
# CONFIDENCE BAND
# -------------------------------
upper = future_preds + noise_level
lower = future_preds - noise_level

# -------------------------------
# SCENARIO SIMULATION 🔥
# -------------------------------
st.sidebar.subheader("🎯 Scenario Simulation")

impact = st.sidebar.slider(
    "📊 Apply Growth Adjustment (%)",
    -50, 50, 0
)

adjusted_preds = future_preds * (1 + impact / 100)

# -------------------------------
# VISUALIZATION
# -------------------------------
st.subheader("📈 Forecast Visualization")

fig = go.Figure()

# Actual
fig.add_trace(go.Scatter(
    x=df["date"],
    y=df[target],
    mode="lines",
    name="Actual",
    line=dict(color="blue")
))

# Predicted
fig.add_trace(go.Scatter(
    x=future_dates,
    y=adjusted_preds,
    mode="lines",
    name="Predicted",
    line=dict(color="orange")
))

# Confidence Band
fig.add_trace(go.Scatter(
    x=list(future_dates) + list(future_dates[::-1]),
    y=list(upper) + list(lower[::-1]),
    fill='toself',
    fillcolor='rgba(255,165,0,0.2)',
    line=dict(color='rgba(255,255,255,0)'),
    showlegend=True,
    name='Confidence Range'
))

fig.update_layout(
    template="plotly_dark",
    title=f"{target} Forecast",
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# MODEL INSIGHTS
# -------------------------------
st.subheader("🧠 Model Intelligence")

col1, col2 = st.columns(2)

col1.metric("Model Accuracy (R²)", round(score, 3))

trend = "Upward 📈" if np.mean(np.diff(future_preds)) > 0 else "Downward 📉"
col2.metric("Trend Direction", trend)

# -------------------------------
# FUTURE DATA TABLE
# -------------------------------
st.subheader("📋 Future Predictions Table")

future_df = pd.DataFrame({
    "date": future_dates,
    "prediction": adjusted_preds
})

st.dataframe(future_df, use_container_width=True)

# -------------------------------
# DOWNLOAD
# -------------------------------
csv = future_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download Forecast",
    data=csv,
    file_name="advanced_forecast.csv",
    mime="text/csv"
)

# -------------------------------
# SMART INSIGHTS
# -------------------------------
st.subheader("🚀 AI Insights")

if score > 0.8:
    st.success("High model reliability")
elif score > 0.5:
    st.warning("Moderate model reliability")
else:
    st.error("Low model reliability")

if impact > 0:
    st.info("Positive growth scenario applied")
elif impact < 0:
    st.warning("Negative scenario simulation")