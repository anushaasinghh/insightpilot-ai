import pandas as pd


def load_dataframe(uploaded_file):
    name = uploaded_file.name
    if name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Only CSV and Excel files supported.")
    return df


def clean_dataframe(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    for col in df.columns:
        if "date" in col or "time" in col:
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass
    for col in df.select_dtypes(include="object").columns:
        try:
            df[col] = pd.to_numeric(df[col].str.replace(",", "").str.replace("$", ""))
        except:
            pass
    return df


def profile_dataframe(df):
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
    return df.describe().round(2)


def detect_column_types(df):
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