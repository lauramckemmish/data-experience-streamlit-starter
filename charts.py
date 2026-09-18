"""Shared chart helpers.

Keep plotting and analysis logic here so experience modules can focus on the
learning sequence and wording.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def histogram(data: pd.DataFrame, field: str, *, label: str | None = None, log_x: bool = False):
    """Create a one-variable distribution with an optional logarithmic x-axis."""
    label = label or field
    if not log_x:
        return px.histogram(data, x=field, title=f"Distribution of {label} · linear scale")

    values = data[field].to_numpy()
    low, high = np.log10(values.min()), np.log10(values.max())
    if low == high:
        low, high = low - 0.05, high + 0.05
    edges = np.logspace(low, high, 21)
    counts, edges = np.histogram(values, bins=edges)
    figure = go.Figure(go.Bar(x=np.sqrt(edges[:-1] * edges[1:]), y=counts, width=np.diff(edges)))
    figure.update_xaxes(type="log", title=label)
    figure.update_yaxes(title="count")
    figure.update_layout(title=f"Distribution of {label} · logarithmic scale", bargap=0.02)
    return figure


def scatter(
    data: pd.DataFrame,
    x: str,
    y: str,
    colour: str | None = None,
    *,
    x_label: str | None = None,
    y_label: str | None = None,
    log_x: bool = False,
    log_y: bool = False,
):
    """Create a scatterplot with independently selectable logarithmic axes."""
    figure = px.scatter(
        data,
        x=x,
        y=y,
        color=colour,
        hover_name=data.columns[0] if len(data.columns) else None,
        log_x=log_x,
        log_y=log_y,
    )
    figure.update_layout(xaxis_title=x_label or x, yaxis_title=y_label or y)
    return figure


def boxplot(data: pd.DataFrame, field: str, *, label: str, log_y: bool = False):
    """Create a secondary one-variable boxplot without changing raw values."""
    figure = px.box(data, y=field, points="outliers", title=f"Another summary of {label}")
    figure.update_layout(yaxis_title=label, xaxis_title=None)
    if log_y:
        figure.update_yaxes(type="log")
    return figure


def categorical_bar(counts: pd.DataFrame, *, label: str):
    """Create a raw-count bar chart for an approved categorical variable."""
    figure = px.bar(counts, x="Count", y="Category", orientation="h", title=f"Counts for {label}")
    figure.update_layout(xaxis_title="Records", yaxis_title=label, showlegend=False)
    figure.update_yaxes(categoryorder="array", categoryarray=counts["Category"].tolist()[::-1])
    return figure


def grouped_boxplot(
    data: pd.DataFrame,
    category: str,
    numeric: str,
    *,
    category_label: str,
    numeric_label: str,
    log_y: bool = False,
):
    """Create side-by-side numeric distributions for approved category groups."""
    figure = px.box(data, x=category, y=numeric, points="outliers", title=f"{numeric_label} across {category_label}")
    figure.update_layout(xaxis_title=category_label, yaxis_title=numeric_label)
    if log_y:
        figure.update_yaxes(type="log")
    return figure


def count_heatmap(
    data: pd.DataFrame,
    x: str,
    y: str,
    *,
    x_label: str,
    y_label: str,
):
    """Create an annotated raw-count heatmap, including absent combinations."""
    table = pd.crosstab(data[y], data[x])
    counts = table.to_numpy()
    figure = go.Figure(
        go.Heatmap(
            z=counts,
            x=table.columns.tolist(),
            y=table.index.tolist(),
            colorscale="Blues",
            hovertemplate=f"{x_label}: %{{x}}<br>{y_label}: %{{y}}<br>Records: %{{z}}<extra></extra>",
        )
    )
    threshold = counts.max() * 0.45 if counts.size else 0
    for row_index, category_y in enumerate(table.index):
        for column_index, category_x in enumerate(table.columns):
            count = int(counts[row_index, column_index])
            figure.add_annotation(
                x=category_x,
                y=category_y,
                text=str(count),
                showarrow=False,
                font={"color": "white" if count >= threshold else "#1f2937", "size": 12},
            )
    figure.update_layout(title=f"Counts for {x_label} and {y_label}", xaxis_title=x_label, yaxis_title=y_label)
    return figure
