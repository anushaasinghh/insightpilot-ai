import streamlit as st
from utils.pdf_generator import generate_report
import os

st.set_page_config(page_title="Report — InsightPilot", page_icon="📄", layout="wide")

st.markdown("# 📄 Export PDF Report")
st.markdown("Download a complete analysis report including data profile, stats, and AI insights.")
st.markdown("---")

if "df" not in st.session_state:
    st.warning("⚠️ No data loaded. Go to the **Upload** page first.")
    st.stop()

df      = st.session_state["df"]
profile = st.session_state.get("profile", {})
insights= st.session_state.get("insights", [])

# ── Report preview ─────────────────────────────────────────
st.markdown("## 📋 Your Report Will Include")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ✅ Dataset overview (rows, columns, missing data)
    
    ✅ Column-by-column profile
    
    ✅ Descriptive statistics table
    """)
with col2:
    st.markdown(f"""
    {"✅" if insights else "⚠️"} AI-generated insights ({len(insights)} found)
    
    ✅ Generation timestamp
    
    ✅ Professional formatting
    """)

if not insights:
    st.info("💡 Tip: Go to **Ask AI** and generate insights first — they'll be included in your report.")

st.markdown("---")

# ── Dataset summary ────────────────────────────────────────
st.markdown("## 📊 Dataset Summary")
if profile:
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Rows",    f"{profile.get('rows', 0):,}")
    m2.metric("Total Columns", profile.get("columns", 0))
    m3.metric("Missing Data",  f"{profile.get('missing_pct', 0)}%")

st.markdown("---")

# ── Generate button ────────────────────────────────────────
st.markdown("## ⬇️ Generate & Download")

if st.button("📥 Generate PDF Report", type="primary", use_container_width=False):
    with st.spinner("Generating your PDF report..."):
        try:
            path = generate_report(
                df, profile, insights,
                filename="insightpilot_report.pdf"
            )
            with open(path, "rb") as f:
                st.download_button(
                    label="⬇️ Click Here to Download Your Report",
                    data=f,
                    file_name="insightpilot_report.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
            st.success("✅ Report generated successfully!")
            st.balloons()
        except Exception as e:
            st.error(f"Error generating PDF: {e}")
            st.exception(e)