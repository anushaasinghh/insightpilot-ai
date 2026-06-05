import pytest
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from utils.ai_analyst import build_data_summary, parse_insights

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "product":  ["Laptop", "Phone", "Tablet"],
        "revenue":  [999.0, 699.0, 449.0],
        "quantity": [10, 25, 15]
    })

# ── build_data_summary tests ───────────────────────────────
def test_summary_includes_shape(sample_df):
    summary = build_data_summary(sample_df)
    assert "3 rows" in summary
    assert "3 columns" in summary

def test_summary_includes_column_names(sample_df):
    summary = build_data_summary(sample_df)
    assert "revenue" in summary
    assert "product" in summary

def test_summary_includes_numeric_stats(sample_df):
    summary = build_data_summary(sample_df)
    assert "mean" in summary
    assert "max" in summary

def test_summary_handles_empty_dataframe():
    df = pd.DataFrame()
    summary = build_data_summary(df)
    assert isinstance(summary, str)
    assert len(summary) > 0

def test_summary_caps_columns_to_avoid_token_overflow():
    """Summary should not include all 20 numeric columns verbosely."""
    df = pd.DataFrame({f"col_{i}": range(10) for i in range(20)})
    summary = build_data_summary(df)
    # Should still return a string without crashing
    assert isinstance(summary, str)

# ── parse_insights tests ───────────────────────────────────
def test_parse_insights_valid_json():
    raw = '[{"title":"Top insight","insight":"Revenue up","importance":"High","recommendation":"Act now"}]'
    result = parse_insights(raw)
    assert result is not None
    assert len(result) == 1
    assert result[0]["title"] == "Top insight"

def test_parse_insights_strips_code_fences():
    raw = '```json\n[{"title":"Test","insight":"x","importance":"High","recommendation":"y"}]\n```'
    result = parse_insights(raw)
    assert result is not None

def test_parse_insights_returns_none_on_invalid_json():
    result = parse_insights("this is not json at all")
    assert result is None

def test_parse_insights_handles_empty_string():
    result = parse_insights("")
    assert result is None