import streamlit as st

st.set_page_config(
    page_title="InsightPilot AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hero
st.title("InsightPilot AI")
st.subheader("Upload any CSV → AI insights, charts & PDF report in 90 seconds")
st.markdown("---")

# Status
if "df" in st.session_state:
    df = st.session_state["df"]
    st.success(f"✅ Dataset loaded: {df.shape[0]:,} rows × {df.shape[1]} columns — use the sidebar to continue.")
else:
    st.info("👈 Click **upload** in the sidebar to load your dataset.")

st.markdown("---")

# Feature cards
st.markdown("### What InsightPilot Does")
c1, c2, c3, c4 = st.columns(4)
c1.info("📁 **Upload & Profile**\n\nCSV or Excel. Auto-cleans and profiles your data instantly.")
c2.info("📊 **Auto Charts**\n\n5 charts generated automatically based on your data.")
c3.info("🤖 **Ask AI**\n\nAsk plain English questions powered by Google Gemini.")
c4.info("📄 **PDF Report**\n\nDownload a full analysis report with one click.")

st.markdown("---")

# How to use
st.markdown("### How to Use")
st.markdown("""
1. **Upload** — click *upload* in the sidebar → upload CSV or use sample data
2. **Visualise** — go to *visualise* to see auto-generated charts
3. **Ask AI** — go to *ask ai* → paste your Gemini API key → generate insights
4. **Report** — go to *report* → download your PDF
""")

st.markdown("---")

