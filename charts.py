"""Shared chart helpers.

Keep plotting and analysis logic here so experience modules can focus on the
learning sequence and wording.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def histogram(data: pd.DataFrame, field: str, *, log_x: bool = False):
    """Create a one-variable distribution with an optional logarithmic x-axis."""
    if not log_x:
        return px.histogram(data, x=field, title=f"Distribution of {field} · linear scale")

    values = data[field].to_numpy()
    low, high = np.log10(values.min()), np.log10(values.max())
    if low == high:
        low, high = low - 0.05, high + 0.05
    edges = np.logspace(low, high, 21)
    counts, edges = np.histogram(values, bins=edges)
    figure = go.Figure(go.Bar(x=np.sqrt(edges[:-1] * edges[1:]), y=counts, width=np.diff(edges)))
    figure.update_xaxes(type="log", title=field)
    figure.update_yaxes(title="count")
    figure.update_layout(title=f"Distribution of {field} · logarithmic scale", bargap=0.02)
    return figure


def scatter(
    data: pd.DataFrame,
    x: str,
    y: str,
    colour: str | None = None,
    *,
    log_x: bool = False,
    log_y: bool = False,
):
    """Create a scatterplot with independently selectable logarithmic axes."""
    return px.scatter(
        data,
        x=x,
        y=y,
        color=colour,
        hover_name=data.columns[0] if len(data.columns) else None,
        log_x=log_x,
        log_y=log_y,
    )
