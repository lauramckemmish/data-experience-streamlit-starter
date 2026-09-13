"""Shared data-loading helpers.

For a new project, replace the bundled demo CSV or change DEFAULT_DATA_PATH.
Experience modules should receive a dataframe rather than loading data themselves.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = APP_DIR / "data" / "taylor_swift_demo_dataset.csv"


@st.cache_data
def load_data(path: str | Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load the project dataset."""
    return pd.read_csv(path)


def column_profile(data: pd.DataFrame) -> dict[str, list[str]]:
    """Return simple column groups useful across generic experiences."""
    numeric = data.select_dtypes(include="number").columns.tolist()
    categorical = [column for column in data.columns if column not in numeric]
    return {"numeric": numeric, "categorical": categorical}


def categorical_filter_fields(data: pd.DataFrame, *, max_categories: int = 12) -> list[str]:
    """Return bounded categorical fields appropriate for the playground filter."""
    return [
        field
        for field in column_profile(data)["categorical"]
        if 2 <= data[field].nunique(dropna=True) <= max_categories
    ]


def categorical_values(data: pd.DataFrame, field: str) -> list[object]:
    """Return stable, present category values for one eligible filter field."""
    return sorted(data[field].dropna().unique().tolist(), key=str)


def filter_categorical_values(
    data: pd.DataFrame,
    field: str,
    selected: list[object],
) -> pd.DataFrame:
    """Filter one categorical field, treating all selected categories as unfiltered.

    Selected categories are combined by union. Selecting every available category
    deliberately retains rows with a missing value in the filter field too, so the
    full-dataset state remains identical to the unfiltered dataset.
    """
    available = categorical_values(data, field)
    if set(selected) == set(available):
        return data.copy()
    return data.loc[data[field].isin(selected)].copy()


def field_profile(data: pd.DataFrame, field: str) -> dict[str, int | str]:
    """Return neutral display metadata for one selected dataset field."""
    values = data[field]
    return {
        "field": field,
        "complete": int(values.notna().sum()),
        "missing": int(values.isna().sum()),
        "kind": "numeric" if pd.api.types.is_numeric_dtype(values) else "categorical/text",
    }


def usable_sample(data: pd.DataFrame, required: list[str]) -> tuple[int, int]:
    """Count rows complete for the fields needed by a displayed analysis."""
    complete = int(data[required].notna().all(axis=1).sum())
    return complete, len(data) - complete


@dataclass(frozen=True)
class ScaleSample:
    """Rows usable for an analysis, with missing and log-scale exclusions separate."""

    data: pd.DataFrame
    total: int
    missing: int
    log_x_excluded: int
    log_y_excluded: int
    log_both_excluded: int
    log_excluded: int


def scale_sample(
    data: pd.DataFrame,
    required: list[str],
    *,
    log_x_field: str | None = None,
    log_y_field: str | None = None,
) -> ScaleSample:
    """Prepare complete rows and remove values invalid for selected log axes.

    ``missing`` counts rows without a required value. ``log_x_excluded`` and
    ``log_y_excluded`` count the selected complete rows with invalid values on
    their respective axes; ``log_excluded`` is their non-overlapping union.
    A logarithmic axis can only display finite, positive values.
    """
    complete_mask = data[required].notna().all(axis=1)
    complete = data.loc[complete_mask]

    def invalid_for_log(field: str | None) -> pd.Series:
        if field is None:
            return pd.Series(False, index=complete.index)
        values = complete[field]
        return values.le(0) | ~pd.Series(np.isfinite(values), index=complete.index)

    log_x_mask = invalid_for_log(log_x_field)
    log_y_mask = invalid_for_log(log_y_field)
    log_mask = log_x_mask | log_y_mask
    return ScaleSample(
        data=complete.loc[~log_mask],
        total=len(data),
        missing=int((~complete_mask).sum()),
        log_x_excluded=int(log_x_mask.sum()),
        log_y_excluded=int(log_y_mask.sum()),
        log_both_excluded=int((log_x_mask & log_y_mask).sum()),
        log_excluded=int(log_mask.sum()),
    )
