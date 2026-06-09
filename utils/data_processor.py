import pandas as pd
import numpy as np
from scipy import stats


def load_dataframe(uploaded_file):
    """Load CSV or Excel file into a DataFrame."""
    name = uploaded_file.name
    if name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Only CSV and Excel files supported.")
    return df


def clean_dataframe(df):
    """
    Clean column names and attempt type coercion.
    - Strip whitespace, lowercase, replace spaces with underscores
    - Try to parse date columns automatically
    - Try to convert string columns that look numeric
    """
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    for col in df.columns:
        if "date" in col or "time" in col:
            try:
                df[col] = pd.to_datetime(df[col])
            except (ValueError, TypeError):
                pass

    for col in df.select_dtypes(include="object").columns:
        try:
            df[col] = pd.to_numeric(
                df[col].str.replace(",", "").str.replace("$", "")
            )
        except (ValueError, TypeError, AttributeError):
            pass

    return df


def profile_dataframe(df):
    """
    Generate a comprehensive data profile dictionary.
    Returns shape, missing data, duplicates, memory, and per-column stats.
    """
    profile = {
        "rows":           len(df),
        "columns":        len(df.columns),
        "missing_cells":  int(df.isnull().sum().sum()),
        "missing_pct":    round(df.isnull().sum().sum() / df.size * 100, 2),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_kb":      round(df.memory_usage(deep=True).sum() / 1024, 1),
        "column_details": []
    }

    for col in df.columns:
        detail = {
            "name":   col,
            "dtype":  str(df[col].dtype),
            "nulls":  int(df[col].isnull().sum()),
            "unique": int(df[col].nunique()),
        }
        if pd.api.types.is_numeric_dtype(df[col]):
            detail.update({
                "min":  round(float(df[col].min()), 2),
                "max":  round(float(df[col].max()), 2),
                "mean": round(float(df[col].mean()), 2),
                "std":  round(float(df[col].std()), 2),
            })
        else:
            detail["top_values"] = df[col].value_counts().head(3).to_dict()
        profile["column_details"].append(detail)

    return profile


def get_summary_stats(df):
    """Return descriptive statistics for numeric columns."""
    return df.describe().round(2)


def detect_column_types(df):
    """Categorise columns into numeric, categorical, datetime, boolean."""
    types = {"numeric": [], "categorical": [], "datetime": [], "boolean": []}
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            types["datetime"].append(col)
        elif pd.api.types.is_bool_dtype(df[col]):
            types["boolean"].append(col)
        elif pd.api.types.is_numeric_dtype(df[col]):
            types["numeric"].append(col)
        else:
            types["categorical"].append(col)
    return types


# ─────────────────────────────────────────────────────────
# NEW FEATURE 1 — DATA QUALITY SCORE
# ─────────────────────────────────────────────────────────

def calculate_quality_score(df) -> dict:
    """
    Calculate a 0-100 Data Quality Score with breakdown.

    Scoring logic (penalties reduce from 100):
      - Missing data:    up to -30 points (proportional to % missing)
      - Duplicates:      up to -20 points (proportional to % duplicate rows)
      - Mixed types:     -5 per column that has mixed/inconsistent data
      - Low cardinality: -3 per numeric column with fewer than 5 unique values
                         (likely a flag column mislabelled as numeric)
      - High cardinality:-3 per categorical column where every value is unique
                         (likely an ID column — not useful for analysis)

    Returns a dict with 'score', 'grade', 'issues', and 'recommendations'.
    """
    score = 100
    issues = []
    recommendations = []

    total_cells = df.size
    rows = len(df)

    # ── Penalty 1: Missing data ────────────────────────────
    missing_pct = df.isnull().sum().sum() / total_cells * 100
    if missing_pct > 0:
        missing_penalty = min(30, missing_pct * 2)
        score -= missing_penalty
        issues.append(f"{missing_pct:.1f}% of cells are missing")
        if missing_pct > 10:
            recommendations.append(
                "High missing data — consider imputation (median for numeric, "
                "mode for categorical) or dropping columns with >50% missing."
            )
        else:
            recommendations.append(
                f"Minor missing data ({missing_pct:.1f}%) — safe to impute or drop rows."
            )

    # ── Penalty 2: Duplicate rows ──────────────────────────
    dup_count = df.duplicated().sum()
    dup_pct = dup_count / rows * 100
    if dup_pct > 0:
        dup_penalty = min(20, dup_pct * 3)
        score -= dup_penalty
        issues.append(f"{dup_count} duplicate rows ({dup_pct:.1f}%)")
        recommendations.append(
            f"Remove {dup_count} duplicate rows with df.drop_duplicates() before analysis."
        )

    # ── Penalty 3: Suspicious numeric columns ─────────────
    num_cols = df.select_dtypes(include="number").columns
    low_card_count = 0
    for col in num_cols:
        if df[col].nunique() < 5:
            low_card_count += 1
    if low_card_count > 0:
        score -= low_card_count * 3
        issues.append(
            f"{low_card_count} numeric column(s) have fewer than 5 unique values "
            f"— may be flag/boolean columns mislabelled as numeric."
        )
        recommendations.append(
            "Review low-cardinality numeric columns — they may need to be "
            "converted to categorical for correct analysis."
        )

    # ── Penalty 4: High-cardinality categoricals ───────────
    cat_cols = df.select_dtypes(include="object").columns
    high_card_count = 0
    for col in cat_cols:
        if df[col].nunique() == len(df):
            high_card_count += 1
    if high_card_count > 0:
        score -= high_card_count * 3
        issues.append(
            f"{high_card_count} categorical column(s) have all-unique values — "
            f"likely ID columns with no analytical value."
        )
        recommendations.append(
            "Drop or exclude all-unique categorical columns (IDs) from analysis "
            "to avoid distorting aggregations."
        )

    score = max(0, round(score))

    # ── Grade ──────────────────────────────────────────────
    if score >= 90:
        grade = "A — Excellent"
        grade_color = "green"
    elif score >= 75:
        grade = "B — Good"
        grade_color = "blue"
    elif score >= 60:
        grade = "C — Acceptable"
        grade_color = "orange"
    elif score >= 40:
        grade = "D — Poor"
        grade_color = "red"
    else:
        grade = "F — Unusable"
        grade_color = "red"

    return {
        "score":           score,
        "grade":           grade,
        "grade_color":     grade_color,
        "issues":          issues if issues else ["No major issues detected."],
        "recommendations": recommendations if recommendations else [
            "Data looks clean — proceed with analysis."
        ],
        "missing_pct":     round(missing_pct, 2),
        "duplicate_pct":   round(dup_pct, 2),
    }


# ─────────────────────────────────────────────────────────
# NEW FEATURE 2 — ANOMALY DETECTION
# ─────────────────────────────────────────────────────────

def detect_anomalies(df, z_threshold: float = 3.0) -> dict:
    """
    Detect anomalous values in numeric columns using Z-score method.

    Z-score = (value - mean) / standard_deviation
    A Z-score > 3 means the value is more than 3 standard deviations
    from the mean — statistically occurs in only 0.3% of normal data.

    Args:
        df: cleaned DataFrame
        z_threshold: how many std devs = anomaly (default 3.0)

    Returns:
        dict with:
          - 'summary': list of dicts per column with anomaly count
          - 'anomaly_df': copy of df with new boolean column per
                          numeric column: '{col}_is_anomaly'
          - 'total_anomalies': int
    """
    num_cols = df.select_dtypes(include="number").columns.tolist()

    if not num_cols:
        return {
            "summary": [],
            "anomaly_df": df.copy(),
            "total_anomalies": 0
        }

    anomaly_df = df.copy()
    summary = []

    for col in num_cols:
        col_data = df[col].dropna()

        if len(col_data) < 10:
            # Not enough data for meaningful Z-score analysis
            continue

        z_scores = np.abs(stats.zscore(col_data))

        # Create a boolean mask aligned with the original index
        is_anomaly = pd.Series(False, index=df.index)
        is_anomaly[col_data.index] = z_scores > z_threshold

        anomaly_df[f"{col}_is_anomaly"] = is_anomaly

        anomaly_count = int(is_anomaly.sum())
        anomaly_values = df.loc[is_anomaly, col].tolist()

        if anomaly_count > 0:
            summary.append({
                "column":          col,
                "anomaly_count":   anomaly_count,
                "anomaly_pct":     round(anomaly_count / len(df) * 100, 2),
                "anomaly_values":  [round(v, 2) for v in anomaly_values[:5]],
                "mean":            round(float(col_data.mean()), 2),
                "std":             round(float(col_data.std()), 2),
                "threshold_upper": round(float(col_data.mean() + z_threshold * col_data.std()), 2),
                "threshold_lower": round(float(col_data.mean() - z_threshold * col_data.std()), 2),
            })

    total = sum(s["anomaly_count"] for s in summary)

    return {
        "summary":          summary,
        "anomaly_df":       anomaly_df,
        "total_anomalies":  total
    }


# ─────────────────────────────────────────────────────────
# NEW FEATURE 3 — COMPARATIVE ANALYSIS HELPERS
# ─────────────────────────────────────────────────────────

def compare_dataframes(df1: pd.DataFrame, df2: pd.DataFrame,
                       label1: str = "Dataset 1",
                       label2: str = "Dataset 2") -> dict:
    """
    Compare two DataFrames that share common columns.
    Returns shape comparison, numeric column stats comparison,
    and a list of notable differences.
    """
    common_cols = list(set(df1.columns) & set(df2.columns))
    num_common = [
        c for c in common_cols
        if pd.api.types.is_numeric_dtype(df1[c])
        and pd.api.types.is_numeric_dtype(df2[c])
    ]

    comparison = []
    for col in num_common:
        mean1 = df1[col].mean()
        mean2 = df2[col].mean()
        pct_change = ((mean2 - mean1) / mean1 * 100) if mean1 != 0 else 0

        comparison.append({
            "column":     col,
            f"{label1}_mean": round(mean1, 2),
            f"{label2}_mean": round(mean2, 2),
            "pct_change": round(pct_change, 2),
            "direction":  "▲ Increased" if pct_change > 0 else
                          "▼ Decreased" if pct_change < 0 else "— No change",
        })

    # Sort by absolute % change — biggest differences first
    comparison.sort(key=lambda x: abs(x["pct_change"]), reverse=True)

    return {
        "common_columns":  common_cols,
        "numeric_compared": comparison,
        "label1_shape":    df1.shape,
        "label2_shape":    df2.shape,
        "label1":          label1,
        "label2":          label2,
    }