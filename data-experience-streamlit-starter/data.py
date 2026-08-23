"""Shared data-loading helpers.

For a new project, replace ``data/sample_data.csv`` or change DEFAULT_DATA_PATH.
Experience modules should receive a dataframe rather than loading data themselves.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = APP_DIR / "data" / "sample_data.csv"


@st.cache_data
def load_data(path: str | Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load the project dataset."""
    return pd.read_csv(path)


def column_profile(data: pd.DataFrame) -> dict[str, list[str]]:
    """Return simple column groups useful across generic experiences."""
    numeric = data.select_dtypes(include="number").columns.tolist()
    categorical = [column for column in data.columns if column not in numeric]
    return {"numeric": numeric, "categorical": categorical}
