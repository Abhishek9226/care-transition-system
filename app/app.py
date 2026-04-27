import streamlit as st

st.set_page_config(page_title="Care Transition System", layout="wide")

# -------------------------------
# 🎨 GLOBAL STYLE (SAFE CSS)
# -------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

.card {
    padding: 20px;
    border-radius: 16px;
    background: linear-gradient(145deg, #0f172a, #1e293b);
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 10px 30px rgba(56,189,248,0.3);
}

.big-title {
    font-size: 42px;
    font-weight: 700;
}

.sub-text {
    color: #9ca3af;
    font-size: 16px;
}

.section-title {
    font-size: 26px;
    font-weight: 600;
    margin-top: 20px;
}

.highlight-box {
    padding: 15px;
    border-radius: 10px;
    background: linear-gradient(90deg, #065f46, #064e3b);
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🚀 HERO HEADER
# -------------------------------
col1, col2 = st.columns([1, 6])

with col1:
    st.markdown("### 🚀")

with col2:
    st.markdown('<div class="big-title">Care Transition Intelligence Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">AI-powered monitoring, analytics & forecasting system</div>', unsafe_allow_html=True)

st.divider()

# -------------------------------
# 🔥 FEATURE CARDS (PREMIUM)
# -------------------------------
st.markdown('<div class="section-title">🔥 Explore Modules</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
        <h4>📊 Dashboard</h4>
        <p>Real-time KPIs, trends & system monitoring</p>
        <small>✔ Live metrics<br>✔ Filters<br>✔ Insights</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h4>📈 Analysis</h4>
        <p>Advanced analytics & deep insights</p>
        <small>✔ Trends<br>✔ Distribution<br>✔ Correlation</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h4>🤖 Predictions</h4>
        <p>AI-based forecasting engine</p>
        <small>✔ Future trends<br>✔ ML logic<br>✔ Planning</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <h4>🗄️ Data Manager</h4>
        <p>Full CRUD & data control</p>
        <small>✔ Add/Delete<br>✔ Edit<br>✔ Bulk operations</small>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# -------------------------------
# 🧠 ABOUT SYSTEM
# -------------------------------
st.markdown('<div class="section-title">🧠 About This System</div>', unsafe_allow_html=True)

st.markdown("""
This platform is designed to analyze and optimize the **care transition pipeline**
from CBP custody to HHS placement.

### 🎯 Key Capabilities:
- 📡 Real-time monitoring of system performance  
- 🚨 Detect bottlenecks & inefficiencies  
- 🤖 AI-based forecasting for decision making  
- 🗄️ Centralized data management system  
""")

st.divider()

# -------------------------------
# 📊 SYSTEM HIGHLIGHT (NEW ADD)
# -------------------------------
st.markdown('<div class="section-title">📊 System Highlights</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.metric("📈 Data Points", "1000+")
col2.metric("⚡ Processing Speed", "Real-time")
col3.metric("🧠 Intelligence Level", "Advanced AI")

st.divider()

# -------------------------------
# 🌟 PLATFORM OVERVIEW (PREMIUM)
# -------------------------------
st.markdown('<div class="section-title">🌟 Platform Overview</div>', unsafe_allow_html=True)

st.markdown("""
This system provides a **complete intelligence layer** over care transition operations,
helping organizations monitor, analyze, and optimize workflows in real-time.

It transforms raw operational data into **actionable insights**, enabling faster decisions,
better resource allocation, and improved system efficiency.
""")

st.markdown("")

col1, col2 = st.columns(2)

# LEFT SIDE - FEATURES
with col1:
    st.markdown("""
### ⚡ What Makes This System Powerful?

- 📊 Real-time KPI monitoring  
- 📈 Advanced analytics & visual insights  
- 🤖 AI-driven forecasting  
- 🧠 Intelligent bottleneck detection  
- 🗄️ Integrated data management system  
- ⚙️ Scalable & modular architecture  
""")

# RIGHT SIDE - VALUE
with col2:
    st.markdown("""
### 🎯 Business Value

- Improve operational efficiency  
- Reduce backlog & delays  
- Enable data-driven decision making  
- Identify hidden patterns & risks  
- Support long-term planning  
""")

st.divider()

# -------------------------------
# 🏁 FOOTER
# -------------------------------
st.caption("Built with Streamlit • Care Transition Intelligence System 🚀")