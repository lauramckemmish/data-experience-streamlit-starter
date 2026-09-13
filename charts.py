"""Shared chart helpers.

Keep plotting and analysis logic here so experience modules can focus on the
learning sequence and wording.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px


def histogram(data: pd.DataFrame, field: str, *, log_x: bool = False):
    """Create a one-variable distribution with an optional logarithmic x-axis."""
    scale = "logarithmic" if log_x else "linear"
    return px.histogram(data, x=field, log_x=log_x, title=f"Distribution of {field} · {scale} scale")


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
