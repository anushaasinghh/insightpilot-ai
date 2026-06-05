import pytest
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from utils.chart_builder import auto_charts, custom_chart

@pytest.fixture
def full_df():
    return pd.DataFrame({
        "date":     pd.date_range("2024-01-01", periods=20, freq="D"),
        "product":  ["Laptop","Phone"] * 10,
        "region":   ["North","South","East","West"] * 5,
        "revenue":  [float(i * 100) for i in range(1, 21)],
        "quantity": list(range(1, 21))
    })

@pytest.fixture
def numeric_only_df():
    return pd.DataFrame({"a": [1,2,3], "b": [4,5,6], "c": [7,8,9]})

def test_auto_charts_returns_list(full_df):
    charts = auto_charts(full_df)
    assert isinstance(charts, list)

def test_auto_charts_not_empty_for_full_dataset(full_df):
    charts = auto_charts(full_df)
    assert len(charts) > 0

def test_auto_charts_each_item_is_tuple(full_df):
    charts = auto_charts(full_df)
    for item in charts:
        assert isinstance(item, tuple)
        assert len(item) == 2

def test_auto_charts_handles_numeric_only(numeric_only_df):
    """Should not crash on a dataset with no dates or categoricals."""
    charts = auto_charts(numeric_only_df)
    assert isinstance(charts, list)

def test_auto_charts_handles_empty_dataframe():
    df = pd.DataFrame()
    charts = auto_charts(df)
    assert charts == []

def test_custom_chart_bar_returns_figure(full_df):
    fig = custom_chart(full_df, "Bar", "product", "revenue")
    assert fig is not None

def test_custom_chart_line_returns_figure(full_df):
    fig = custom_chart(full_df, "Line", "date", "revenue")
    assert fig is not None

def test_custom_chart_with_color_col(full_df):
    fig = custom_chart(full_df, "Bar", "product", "revenue", color_col="region")
    assert fig is not None