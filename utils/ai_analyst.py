import google.generativeai as genai
import json


def get_ai_insights(df, api_key, question=None):
    genai.configure(api_key=api_key)
    model   = genai.GenerativeModel("gemini-1.5-flash")
    summary = build_data_summary(df)

    if question:
        prompt = f"""You are an expert data analyst. A user uploaded a dataset and has a question.

DATASET SUMMARY:
{summary}

USER QUESTION: {question}

Answer clearly using specific numbers. Keep answer under 200 words."""
    else:
        prompt = f"""You are an expert data analyst. Analyse this dataset and give 5 key business insights.

DATASET SUMMARY:
{summary}

Return ONLY a valid JSON array of exactly 5 objects. Each must have:
- "title": short title (max 8 words)
- "insight": 2-3 sentence explanation with specific numbers
- "importance": "High", "Medium", or "Low"
- "recommendation": one actionable next step

Raw JSON only. No markdown, no backticks, no explanation before or after."""

    response = model.generate_content(prompt)
    return response.text


def build_data_summary(df):
    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    lines = [
        f"Shape: {df.shape[0]} rows x {df.shape[1]} columns",
        f"Columns: {list(df.columns)}",
        f"Numeric columns: {num_cols}",
        f"Categorical columns: {cat_cols}",
    ]

    if num_cols:
        lines.append("Numeric stats:")
        for col in num_cols[:5]:
            lines.append(
                f"  {col}: min={df[col].min():.2f}, "
                f"max={df[col].max():.2f}, "
                f"mean={df[col].mean():.2f}, "
                f"sum={df[col].sum():.2f}"
            )

    if cat_cols:
        lines.append("Top categorical values:")
        for col in cat_cols[:3]:
            top = df[col].value_counts().head(5).to_dict()
            lines.append(f"  {col}: {top}")

    return "\n".join(lines)


def parse_insights(raw_response):
    try:
        text = raw_response.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except:
        return None