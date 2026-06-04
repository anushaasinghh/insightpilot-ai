import streamlit as st
from utils.chart_builder import auto_charts, custom_chart

st.set_page_config(page_title="Visualise — InsightPilot", page_icon="📊", layout="wide")

st.markdown("# 📊 Visualise Your Data")
st.markdown("Auto-generated charts based on your dataset's column types.")
st.markdown("---")

if "df" not in st.session_state:
    st.warning("⚠️ No data loaded. Go to the **Upload** page first.")
    st.stop()

df = st.session_state["df"]

st.markdown(f"**Dataset:** {df.shape[0]:,} rows × {df.shape[1]} columns")
st.markdown("---")

# ── Auto charts ────────────────────────────────────────────
st.markdown("## 🤖 Auto-Generated Charts")
st.caption("InsightPilot picks the most relevant chart types for your data automatically.")

with st.spinner("Building charts..."):
    charts = auto_charts(df)

if not charts:
    st.info("Not enough column variety to auto-generate charts. Try the custom builder below.")
else:
    for i in range(0, len(charts), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(charts):
                title, fig = charts[i + j]
                with cols[j]:
                    st.markdown(f"**{title}**")
                    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Custom chart builder ───────────────────────────────────
st.markdown("## 🛠️ Build Your Own Chart")
st.caption("Select columns and chart type to explore your own questions.")

all_cols = df.columns.tolist()
num_cols = df.select_dtypes(include="number").columns.tolist()

if not num_cols:
    st.warning("No numeric columns found for custom charts.")
else:
    c1, c2, c3, c4 = st.columns(4)
    chart_type = c1.selectbox("Chart Type", ["Bar", "Line", "Scatter", "Box"])
    x_col      = c2.selectbox("X Axis", all_cols)
    y_col      = c3.selectbox("Y Axis", num_cols)
    color_col  = c4.selectbox("Color by", ["None"] + all_cols)

    if st.button("✨ Generate Chart", type="primary"):
        try:
            fig = custom_chart(
                df, chart_type, x_col, y_col,
                None if color_col == "None" else color_col
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Chart error: {e}")