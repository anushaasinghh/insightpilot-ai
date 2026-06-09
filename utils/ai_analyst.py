import google.generativeai as genai
import json


def get_ai_insights(df, api_key, question=None):
    """
    Send dataframe summary + optional question to Gemini.
    - No question: returns 5 business insights as JSON string
    - With question: returns plain text answer
    """
    genai.configure(api_key=api_key)
    model   = genai.GenerativeModel("gemini-2.0-flash")
    summary = build_data_summary(df)

    if question:
        prompt = f"""You are an expert data analyst. A user uploaded a dataset and has a question.

DATASET SUMMARY:
{summary}

USER QUESTION: {question}

Answer clearly using specific numbers from the data. Keep answer under 200 words."""

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


def build_data_summary(df) -> str:
    """
    Build a compact, token-efficient summary of the DataFrame.
    Sent to the AI instead of raw data for privacy and cost reasons.
    """
    num_cols = df.select_dtypes(include="number").columns.tolist()
    # Exclude anomaly flag columns
    num_cols = [c for c in num_cols if not c.endswith("_is_anomaly")]
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


def parse_insights(raw_response) -> list:
    """
    Safely parse the JSON insights response from Gemini.
    Handles markdown code fences that Gemini sometimes adds.
    Returns list of dicts or None if parsing fails.
    """
    try:
        text = raw_response.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except Exception:
        return None


# ─────────────────────────────────────────────────────────
# NEW FEATURE — EXECUTIVE SUMMARY
# ─────────────────────────────────────────────────────────

def get_executive_summary(df, api_key, anomaly_info: str = "",
                          quality_score: int = None) -> str:
    """
    Generate a 3-5 sentence executive summary of the dataset.

    Different from insights — this is a single coherent paragraph
    written like a business analyst would write for a CEO briefing:
    - What the data covers
    - The single most important finding
    - One risk or anomaly if present
    - One recommended action

    Args:
        df: the cleaned DataFrame
        api_key: Gemini API key
        anomaly_info: optional string describing detected anomalies
        quality_score: optional int (0-100) from calculate_quality_score()
    """
    genai.configure(api_key=api_key)
    model   = genai.GenerativeModel("gemini-2.0-flash")
    summary = build_data_summary(df)

    # Build context additions
    extra_context = ""
    if quality_score is not None:
        extra_context += f"\nData Quality Score: {quality_score}/100"
    if anomaly_info:
        extra_context += f"\nAnomalies detected: {anomaly_info}"

    prompt = f"""You are a senior business analyst writing a briefing for a CEO.
Write a concise executive summary of this dataset in exactly 4 sentences.

DATASET SUMMARY:
{summary}
{extra_context}

Requirements:
- Sentence 1: What this dataset covers (what business process, time period, scale)
- Sentence 2: The single most important positive finding with a specific number
- Sentence 3: The most important risk, gap, or anomaly with a specific number
- Sentence 4: One clear recommended action

Write in plain business English. No jargon. No bullet points. Just 4 sentences as a paragraph.
Do not start with 'This dataset' — vary the opening."""

    response = model.generate_content(prompt)
    return response.text.strip()