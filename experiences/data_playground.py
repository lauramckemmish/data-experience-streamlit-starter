"""Open-ended data exploration experience.

This is deliberately separate from the guided CURIOUS sequence.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from charts import histogram, scatter
from data import column_profile
from ui_helpers import page_header


def render(data: pd.DataFrame) -> None:
    page_header("Data Playground", teacher_control=False)
    st.write("Explore the dataset freely. Put multivariate and parallel-coordinate tools here as the project develops.")

    profile = column_profile(data)
    numeric = profile["numeric"]
    categorical = profile["categorical"]

    if not numeric:
        st.warning("The current dataset has no numeric columns to plot.")
        st.dataframe(data, use_container_width=True)
        return

    mode = st.radio("Choose a graph", ["Histogram", "Scatter plot"], horizontal=True)
    if mode == "Histogram" or len(numeric) < 2:
        field = st.selectbox("Variable", numeric)
        st.plotly_chart(histogram(data, field), use_container_width=True)
    else:
        x = st.selectbox("Horizontal axis", numeric, index=0)
        y = st.selectbox("Vertical axis", numeric, index=1 if len(numeric) > 1 else 0)
        colour_options = ["None", *categorical]
        colour = st.selectbox("Colour by", colour_options)
        st.plotly_chart(scatter(data, x, y, None if colour == "None" else colour), use_container_width=True)

    with st.expander("Dataset preview"):
        st.dataframe(data, use_container_width=True, hide_index=True)
