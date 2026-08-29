"""Shared data-loading helpers.

For a new project, replace the bundled demo CSV or change DEFAULT_DATA_PATH.
Experience modules should receive a dataframe rather than loading data themselves.
"""

from __future__ import annotations

from pathlib import Path

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
