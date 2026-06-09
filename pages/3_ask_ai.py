import streamlit as st
from utils.ai_analyst import get_ai_insights, parse_insights

st.set_page_config(page_title="Ask AI: InsightPilot", page_icon="🤖", layout="wide")

st.markdown("# 🤖 Ask AI About Your Data")

if "df" not in st.session_state:
    st.warning("⚠️ No data loaded. Go to the **Upload** page first.")
    st.stop()

if not st.session_state.get("api_key"):
    st.warning("⚠️ No API key found. Go to the **Upload** page and paste your Gemini API key in the sidebar.")
    st.stop()

df      = st.session_state["df"]
api_key = st.session_state["api_key"]

# ── Auto insights ──────────────────────────────────────────
st.markdown("## 💡 Auto-Generate Business Insights")
st.caption("One click: AI analyses your data and returns 5 actionable business insights.")

if st.button("✨ Generate 5 Insights", type="primary", use_container_width=False):
    with st.spinner("Gemini is analysing your data... (5–10 seconds)"):
        try:
            raw      = get_ai_insights(df, api_key)
            insights = parse_insights(raw)
            if insights:
                st.session_state["insights"] = insights
                st.success("✅ Insights generated!")
            else:
                st.error("Couldn't parse AI response. Try again.")
                st.code(raw)
        except Exception as e:
            st.error(f"API error: {e}")

if "insights" in st.session_state:
    for i, ins in enumerate(st.session_state["insights"]):
        importance = ins.get("importance", "Medium")
        color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(importance, "⚪")
        with st.expander(f"{color} {ins.get('title', f'Insight {i+1}')}", expanded=(i==0)):
            st.markdown(f"**Finding:** {ins.get('insight', '')}")
            st.info(f"💡 **Recommendation:** {ins.get('recommendation', '')}")
            st.caption(f"Importance: {importance}")

st.markdown("---")

# ── Q&A Chat ───────────────────────────────────────────────
st.markdown("## 💬 Ask a Question")
st.caption("Examples: 'Which product has the highest revenue?' · 'What is the average quantity?' · 'Which region performs worst?'")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask anything about your data...")

if question:
    st.session_state["chat_history"].append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = get_ai_insights(df, api_key, question=question)
                st.write(answer)
                st.session_state["chat_history"].append(
                    {"role": "assistant", "content": answer}
                )
            except Exception as e:
                st.error(f"Error: {e}")