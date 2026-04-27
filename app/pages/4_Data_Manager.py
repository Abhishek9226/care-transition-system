import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Data Manager", layout="wide")

st.title("🗄️ Advanced Data Management System")

# -------------------------------
# DB CONNECTION
# -------------------------------
conn = sqlite3.connect("care_data.db", check_same_thread=False)

# -------------------------------
# INIT TABLE
# -------------------------------
def init_db():
    conn.execute("""
    CREATE TABLE IF NOT EXISTS care_data (
        date TEXT,
        cbp_apprehended REAL,
        cbp_in_custody REAL,
        cbp_transferred REAL,
        hhs_in_care REAL,
        hhs_discharged REAL
    )
    """)
    conn.commit()

init_db()

# -------------------------------
# LOAD CSV (FIRST TIME)
# -------------------------------
@st.cache_data
def load_csv():
    df = pd.read_csv("data/HHS_Unaccompanied_Alien_Children_Program.csv")
    df.columns = [
        "date",
        "cbp_apprehended",
        "cbp_in_custody",
        "cbp_transferred",
        "hhs_in_care",
        "hhs_discharged"
    ]
    return df

# -------------------------------
# LOAD DATA FROM DB
# -------------------------------
def get_data():
    return pd.read_sql("SELECT rowid, * FROM care_data", conn)

# -------------------------------
# LOAD BUTTON
# -------------------------------
if st.button("📥 Load Initial Dataset"):
    df_csv = load_csv()
    df_csv.to_sql("care_data", conn, if_exists="replace", index=False)
    st.success("Dataset loaded successfully")

df = get_data()

# -------------------------------
# TABS UI
# -------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 View & Edit",
    "➕ Add Record",
    "🗑️ Delete",
    "📤 Upload/Download"
])

# -------------------------------
# TAB 1: EDITABLE TABLE 🔥
# -------------------------------
with tab1:
    st.subheader("📊 Edit Data Directly")

    if not df.empty:
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

        if st.button("💾 Save Changes"):
            edited_df.drop(columns=["rowid"], inplace=True)
            edited_df.to_sql("care_data", conn, if_exists="replace", index=False)
            st.success("Changes saved successfully 🔄")
    else:
        st.warning("No data found. Load dataset first.")

# -------------------------------
# TAB 2: ADD RECORD
# -------------------------------
with tab2:
    st.subheader("➕ Add New Record")

    date = st.date_input("Date", key="date")
    a = st.number_input("CBP Apprehended", min_value=0.0, key="a")
    b = st.number_input("CBP In Custody", min_value=0.0, key="b")
    c = st.number_input("CBP Transferred", min_value=0.0, key="c")
    d = st.number_input("HHS In Care", min_value=0.0, key="d")
    e = st.number_input("HHS Discharged", min_value=0.0, key="e")

    if st.button("➕ Add Record"):
        try:
            conn.execute("""
                INSERT INTO care_data 
                (date, cbp_apprehended, cbp_in_custody, cbp_transferred, hhs_in_care, hhs_discharged)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (str(date), a, b, c, d, e))

            conn.commit()

            st.success("✅ Record Added Successfully!")
            st.write("Inserted values:", date, a, b, c, d, e)

            st.rerun()

        except Exception as e:
            st.error(f"Error: {e}")

# -------------------------------
# TAB 3: DELETE RECORD
# -------------------------------
with tab3:
    st.subheader("🗑️ Bulk Delete Records")

    df = pd.read_sql("SELECT rowid, * FROM care_data", conn)

    if not df.empty:

        col1, col2 = st.columns(2)

        start_id = col1.number_input(
            "Start Row ID",
            min_value=int(df["rowid"].min()),
            max_value=int(df["rowid"].max()),
            value=int(df["rowid"].min())
        )

        end_id = col2.number_input(
            "End Row ID",
            min_value=int(df["rowid"].min()),
            max_value=int(df["rowid"].max()),
            value=int(df["rowid"].min())
        )

        st.warning(f"⚠️ This will delete records from ID {start_id} to {end_id}")

        # 🔥 CONFIRMATION
        confirm = st.checkbox("I confirm deletion")

        if confirm and st.button("🚨 Delete Selected Range"):
            conn.execute(
                "DELETE FROM care_data WHERE rowid BETWEEN ? AND ?",
                (start_id, end_id)
            )
            conn.commit()

            st.success(f"✅ Deleted records from ID {start_id} to {end_id}")

            st.rerun()

    else:
        st.warning("No data available")
# -------------------------------
# TAB 4: UPLOAD / DOWNLOAD
# -------------------------------
with tab4:
    st.subheader("📤 Upload New Dataset")

    uploaded = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded:
        new_df = pd.read_csv(uploaded)
        new_df.to_sql("care_data", conn, if_exists="replace", index=False)
        st.success("New dataset uploaded 🚀")

    st.subheader("⬇️ Download Current Data")

    if not df.empty:
        csv = df.drop(columns=["rowid"]).to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Dataset",
            data=csv,
            file_name="care_data.csv",
            mime="text/csv"
        )