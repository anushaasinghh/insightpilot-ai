import streamlit as st
import pandas as pd
from utils.data_processor import (
    load_dataframe, clean_dataframe,
    profile_dataframe, get_summary_stats
)

st.set_page_config(page_title="Upload — InsightPilot", page_icon="📁", layout="wide")

st.markdown("# 📁 Upload & Profile Your Data")
st.markdown("Upload a CSV or Excel file to get started. InsightPilot will automatically clean and profile it.")
st.markdown("---")

# ── Sidebar — API Key ──────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔑 API Key Status")

    # Load from secrets.toml silently
    default_key = ""
    try:
        default_key = st.secrets.get("GEMINI_API_KEY", "")
    except:
        pass

    if default_key:
        st.session_state["api_key"] = default_key
        st.success("✅ API key loaded")
    else:
        # Only show input if no key in secrets — for public demo users
        api_key = st.text_input(
            "Enter Gemini API Key",
            type="password",   # ← this hides it with dots
            placeholder="AIzaSy...",
            help="Get free key at aistudio.google.com/app/apikey"
        )
        if api_key:
            st.session_state["api_key"] = api_key
            st.success("✅ Key saved for this session")
        else:
            st.warning("Add Gemini API key to use AI features")

# ── Upload area ────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    uploaded = st.file_uploader(
        "Choose a CSV or Excel file",
        type=["csv", "xlsx", "xls"],
        help="Max file size: 50MB"
    )

with col2:
    st.markdown("#### Or try sample data")
    st.markdown("Don't have a file? Use our built-in sales dataset.")
    if st.button("📦 Load Sample Dataset", use_container_width=True, type="primary"):
        try:
            df = pd.read_csv("sample_data/sample_sales.csv")
            df = clean_dataframe(df)
            st.session_state["df"] = df
            st.success(f"✅ Loaded! {df.shape[0]:,} rows × {df.shape[1]} cols")
        except Exception as e:
            st.error(f"Error: {e}")

# ── Process uploaded file ──────────────────────────────────
if uploaded is not None:
    try:
        with st.spinner("Loading and cleaning your data..."):
            df = load_dataframe(uploaded)
            df = clean_dataframe(df)
            st.session_state["df"] = df
        st.success(f"✅ Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
    except Exception as e:
        st.error(f"Could not load file: {e}")

# ── Show profile if data is loaded ────────────────────────
if "df" in st.session_state:
    df = st.session_state["df"]
    profile = profile_dataframe(df)
    st.session_state["profile"] = profile

    st.markdown("---")
    st.markdown("## 📊 Data Profile")

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Rows",        f"{profile['rows']:,}")
    m2.metric("Columns",     profile["columns"])
    m3.metric("Missing %",   f"{profile['missing_pct']}%")
    m4.metric("Duplicates",  profile["duplicate_rows"])
    m5.metric("Size",        f"{profile['memory_kb']} KB")

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["🔍 Column Details", "📈 Summary Stats", "👀 Raw Data"])

    with tab1:
        col_df = pd.DataFrame(profile["column_details"])
        st.dataframe(col_df, use_container_width=True, height=400)

    with tab2:
        st.dataframe(get_summary_stats(df), use_container_width=True)

    with tab3:
        n = st.slider("Rows to preview", 5, 100, 20)
        st.dataframe(df.head(n), use_container_width=True)

    st.markdown("---")
    st.success("✅ Data loaded! Use the sidebar to navigate to **Visualise** next.")
else:
    st.markdown("---")
    st.markdown("### 📂 No data loaded yet")
    st.markdown("Upload a file above or click **Load Sample Dataset** to get started.")