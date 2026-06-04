import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

COLORS = ["#4F81BD", "#E05C5C", "#2ECC71", "#F39C12", "#9B59B6", "#1ABC9C"]


def auto_charts(df):
    charts = []
    num_cols  = df.select_dtypes(include="number").columns.tolist()
    cat_cols  = df.select_dtypes(include="object").columns.tolist()
    date_cols = df.select_dtypes(include="datetime").columns.tolist()

    if not num_cols:
        return charts

    # 1. Time series
    if date_cols and num_cols:
        date_col  = date_cols[0]
        value_col = num_cols[0]
        ts = df.groupby(date_col)[value_col].sum().reset_index()
        fig = px.line(ts, x=date_col, y=value_col,
                      title=f"{value_col.replace('_', ' ').title()} Over Time",
                      color_discrete_sequence=COLORS)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        charts.append(("Time Series", fig))

    # 2. Bar chart
    if cat_cols and num_cols:
        cat_col   = cat_cols[0]
        value_col = num_cols[0]
        bar_data  = df.groupby(cat_col)[value_col].sum().sort_values(ascending=False).head(10)
        fig = px.bar(bar_data,
                     title=f"{value_col.replace('_', ' ').title()} by {cat_col.replace('_', ' ').title()}",
                     color_discrete_sequence=COLORS)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        charts.append(("Category Breakdown", fig))

    # 3. Histogram
    if num_cols:
        col = num_cols[0]
        fig = px.histogram(df, x=col, nbins=30,
                           title=f"Distribution of {col.replace('_', ' ').title()}",
                           color_discrete_sequence=COLORS)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        charts.append(("Distribution", fig))

    # 4. Pie chart
    if len(cat_cols) >= 1 and num_cols:
        cat_col   = cat_cols[1] if len(cat_cols) > 1 else cat_cols[0]
        value_col = num_cols[0]
        pie_data  = df.groupby(cat_col)[value_col].sum().reset_index()
        fig = px.pie(pie_data, names=cat_col, values=value_col,
                     title=f"Share by {cat_col.replace('_', ' ').title()}",
                     color_discrete_sequence=COLORS)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        charts.append(("Share Breakdown", fig))

    # 5. Correlation heatmap
    if len(num_cols) >= 3:
        corr = df[num_cols].corr().round(2)
        fig  = go.Figure(go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale="Blues",
            text=corr.values,
            texttemplate="%{text}"
        ))
        fig.update_layout(title="Correlation Heatmap",
                          paper_bgcolor="rgba(0,0,0,0)")
        charts.append(("Correlations", fig))

    return charts


def custom_chart(df, chart_type, x_col, y_col, color_col=None):
    kwargs = dict(x=x_col, y=y_col, color=color_col,
                  color_discrete_sequence=COLORS)
    if chart_type == "Bar":
        fig = px.bar(df, **kwargs)
    elif chart_type == "Line":
        fig = px.line(df, **kwargs)
    elif chart_type == "Scatter":
        fig = px.scatter(df, **kwargs)
    elif chart_type == "Box":
        fig = px.box(df, **kwargs)
    else:
        fig = px.bar(df, **kwargs)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig