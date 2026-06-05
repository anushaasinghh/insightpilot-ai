import pytest
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from utils.data_processor import clean_dataframe, profile_dataframe, detect_column_types

# ── Fixtures ───────────────────────────────────────────────
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "date":     ["2024-01-01", "2024-01-02", "2024-01-03"],
        "product":  ["Laptop", "Phone", "Laptop"],
        "revenue":  [999.0, 699.0, 999.0],
        "quantity": [1, 2, 1],
        "returned": [False, False, True]
    })

@pytest.fixture
def messy_df():
    return pd.DataFrame({
        " Product Name ": ["Laptop", "Phone", None],
        "Revenue ($)":    ["$999", "$699", "$449"],
        "  Date  ":       ["2024-01-01", "2024-01-02", "2024-01-03"]
    })

# ── clean_dataframe tests ──────────────────────────────────
def test_clean_strips_column_whitespace(messy_df):
    cleaned = clean_dataframe(messy_df)
    assert " Product Name " not in cleaned.columns
    assert "product_name" in cleaned.columns

def test_clean_lowercases_columns(messy_df):
    cleaned = clean_dataframe(messy_df)
    for col in cleaned.columns:
        assert col == col.lower(), f"Column '{col}' is not lowercase"

def test_clean_parses_date_columns(messy_df):
    cleaned = clean_dataframe(messy_df)
    date_col = [c for c in cleaned.columns if "date" in c][0]
    assert pd.api.types.is_datetime64_any_dtype(cleaned[date_col])

# ── profile_dataframe tests ────────────────────────────────
def test_profile_returns_correct_row_count(sample_df):
    profile = profile_dataframe(sample_df)
    assert profile["rows"] == 3

def test_profile_returns_correct_column_count(sample_df):
    profile = profile_dataframe(sample_df)
    assert profile["columns"] == 5

def test_profile_detects_no_missing_in_clean_df(sample_df):
    profile = profile_dataframe(sample_df)
    assert profile["missing_cells"] == 0

def test_profile_detects_missing_values():
    df = pd.DataFrame({"a": [1, None, 3], "b": ["x", "y", None]})
    profile = profile_dataframe(df)
    assert profile["missing_cells"] == 2

def test_profile_detects_duplicates():
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})
    profile = profile_dataframe(df)
    assert profile["duplicate_rows"] == 1

def test_profile_column_details_has_mean_for_numeric(sample_df):
    profile = profile_dataframe(sample_df)
    revenue_detail = next(c for c in profile["column_details"] if c["name"] == "revenue")
    assert "mean" in revenue_detail
    assert revenue_detail["mean"] == pytest.approx(899.0, rel=1e-2)

# ── detect_column_types tests ──────────────────────────────
def test_detect_identifies_numeric_columns(sample_df):
    types = detect_column_types(sample_df)
    assert "revenue" in types["numeric"]
    assert "quantity" in types["numeric"]

def test_detect_identifies_categorical_columns(sample_df):
    types = detect_column_types(sample_df)
    assert "product" in types["categorical"]

def test_detect_identifies_boolean_columns(sample_df):
    types = detect_column_types(sample_df)
    assert "returned" in types["boolean"]

def test_detect_handles_empty_dataframe():
    df = pd.DataFrame()
    types = detect_column_types(df)
    assert all(len(v) == 0 for v in types.values())