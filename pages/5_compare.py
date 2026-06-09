import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.data_processor import (
    load_dataframe, clean_dataframe, compare_dataframes
)
from utils.chart_builder import fig_to_png_bytes

st.set_page_config(
    page_title="Compare — InsightPilot", page_icon="⚖️", layout="wide"
)

st.markdown("# ⚖️ Comparative Analysis")
st.markdown("Upload two datasets and instantly see what changed between them.")
st.markdown("*Use case: this month vs last month, Region A vs Region B, before vs after a campaign.*")
st.markdown("---")

# ── Upload two files ───────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📁 Dataset 1")
    label1 = st.text_input("Label for Dataset 1", value="Dataset 1", key="label1")
    file1  = st.file_uploader("Upload first file", type=["csv", "xlsx"], key="file1")

with col2:
    st.markdown("### 📁 Dataset 2")
    label2 = st.text_input("Label for Dataset 2", value="Dataset 2", key="label2")
    file2  = st.file_uploader("Upload second file", type=["csv", "xlsx"], key="file2")

# ── Or use built-in demo ───────────────────────────────────
st.markdown("---")
if st.button("📦 Load Demo Comparison (split sample data into 2 halves)", type="secondary"):
    try:
        df_full = pd.read_csv("sample_data/sample_sales.csv")
        df_full = clean_dataframe(df_full)
        half    = len(df_full) // 2
        st.session_state["compare_df1"] = df_full.iloc[:half].copy()
        st.session_state["compare_df2"] = df_full.iloc[half:].copy()
        st.session_state["compare_label1"] = "First Half"
        st.session_state["compare_label2"] = "Second Half"
        st.success("✅ Demo loaded — comparing first 500 rows vs last 500 rows of sample data.")
    except Exception as e:
        st.error(f"Error: {e}")

# ── Load uploaded files ────────────────────────────────────
if file1 is not None:
    try:
        df1 = load_dataframe(file1)
        df1 = clean_dataframe(df1)
        st.session_state["compare_df1"]    = df1
        st.session_state["compare_label1"] = label1
        st.success(f"✅ {label1}: {df1.shape[0]:,} rows × {df1.shape[1]} columns")
    except Exception as e:
        st.error(f"Error loading file 1: {e}")

if file2 is not None:
    try:
        df2 = load_dataframe(file2)
        df2 = clean_dataframe(df2)
        st.session_state["compare_df2"]    = df2
        st.session_state["compare_label2"] = label2
        st.success(f"✅ {label2}: {df2.shape[0]:,} rows × {df2.shape[1]} columns")
    except Exception as e:
        st.error(f"Error loading file 2: {e}")

# ── Run comparison ─────────────────────────────────────────
if "compare_df1" in st.session_state and "compare_df2" in st.session_state:
    df1 = st.session_state["compare_df1"]
    df2 = st.session_state["compare_df2"]
    l1  = st.session_state.get("compare_label1", "Dataset 1")
    l2  = st.session_state.get("compare_label2", "Dataset 2")

    st.markdown("---")

    # Shape comparison
    st.markdown("## 📐 Shape Comparison")
    s1, s2, s3, s4 = st.columns(4)
    s1.metric(f"{l1} rows",    f"{df1.shape[0]:,}")
    s2.metric(f"{l2} rows",    f"{df2.shape[0]:,}",
              delta=f"{df2.shape[0] - df1.shape[0]:+,}")
    s3.metric(f"{l1} columns", df1.shape[1])
    s4.metric(f"{l2} columns", df2.shape[1],
              delta=f"{df2.shape[1] - df1.shape[1]:+}")

    # Run comparison
    comparison = compare_dataframes(df1, df2, l1, l2)

    if not comparison["numeric_compared"]:
        st.warning(
            "No common numeric columns found between the two datasets. "
            "Make sure both files have the same column names."
        )
    else:
        st.markdown("---")
        st.markdown("## 📊 Metric Comparison")
        st.caption(
            "Showing all common numeric columns sorted by absolute % change. "
            "Biggest differences at the top."
        )

        comp_df = pd.DataFrame(comparison["numeric_compared"])

        # Colour code the direction column
        st.dataframe(
            comp_df.style.applymap(
                lambda v: "color: green" if "▲" in str(v)
                else "color: red" if "▼" in str(v) else "",
                subset=["direction"]
            ),
            use_container_width=True,
            height=400
        )

        st.markdown("---")
        st.markdown("## 📈 Side-by-Side Charts")

        # Let user pick which column to compare
        compare_col = st.selectbox(
            "Select column to compare visually",
            [row["column"] for row in comparison["numeric_compared"]]
        )

        if compare_col:
            row = next(
                r for r in comparison["numeric_compared"]
                if r["column"] == compare_col
            )

            mean1_key = f"{l1}_mean"
            mean2_key = f"{l2}_mean"

            # Bar chart comparing means
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name=l1, x=[compare_col],
                y=[row[mean1_key]],
                marker_color="#4F81BD"
            ))
            fig.add_trace(go.Bar(
                name=l2, x=[compare_col],
                y=[row[mean2_key]],
                marker_color="#E05C5C"
            ))
            fig.update_layout(
                title=f"Mean {compare_col.replace('_', ' ').title()} — {l1} vs {l2}",
                barmode="group",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)

            # PNG download
            try:
                png_bytes = fig_to_png_bytes(fig)
                st.download_button(
                    label="⬇️ Download Comparison Chart as PNG",
                    data=png_bytes,
                    file_name=f"compare_{compare_col}.png",
                    mime="image/png"
                )
            except Exception:
                pass

            # Distribution comparison
            st.markdown("#### Distribution Comparison")
            fig2 = go.Figure()
            fig2.add_trace(go.Histogram(
                x=df1[compare_col].dropna(), name=l1,
                opacity=0.7, marker_color="#4F81BD", nbinsx=30
            ))
            fig2.add_trace(go.Histogram(
                x=df2[compare_col].dropna(), name=l2,
                opacity=0.7, marker_color="#E05C5C", nbinsx=30
            ))
            fig2.update_layout(
                barmode="overlay",
                title=f"Distribution of {compare_col.replace('_', ' ').title()}",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Notable differences summary
        st.markdown("---")
        st.markdown("## 🔍 Notable Differences")
        significant = [
            r for r in comparison["numeric_compared"]
            if abs(r["pct_change"]) > 5
        ]
        if not significant:
            st.success("No significant differences (>5% change) found between the datasets.")
        else:
            for row in significant[:5]:
                direction_icon = "📈" if row["pct_change"] > 0 else "📉"
                st.markdown(
                    f"{direction_icon} **{row['column'].replace('_', ' ').title()}** "
                    f"changed by **{row['pct_change']:+.1f}%** — "
                    f"from {row[f'{l1}_mean']} ({l1}) "
                    f"to {row[f'{l2}_mean']} ({l2})"
                )

else:
    st.markdown("---")
    st.info("Upload both datasets above, or click **Load Demo Comparison** to see how it works.")