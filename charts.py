"""Shared chart helpers.

Keep plotting and analysis logic here so experience modules can focus on the
learning sequence and wording.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px


def histogram(data: pd.DataFrame, field: str):
    return px.histogram(data, x=field, title=f"Distribution of {field}")


def scatter(data: pd.DataFrame, x: str, y: str, colour: str | None = None):
    return px.scatter(data, x=x, y=y, color=colour, hover_name=data.columns[0] if len(data.columns) else None)
