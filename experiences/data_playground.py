"""Stable open-ended Data Exploration Playground shell.

The master pattern is deliberately simple: one variable, two variables and
three variables. Dataset-specific projects may add constrained filtering,
model fitting or other analysis without changing this experience structure.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from charts import histogram, scatter
from data import column_profile
from ui_helpers import page_header


def render(data: pd.DataFrame) -> None:
    page_header("Data Exploration Playground", teacher_control=False)
    st.write(
        "Explore the dataset by changing how many variables you are looking at. "
        "Use dataset-specific filters or modelling tools only when they help answer a scientific question."
    )

    profile = column_profile(data)
    numeric = profile["numeric"]
    categorical = profile["categorical"]

    if not numeric:
        st.warning("The current dataset has no numeric columns to plot.")
        st.dataframe(data, use_container_width=True)
        return

    mode = st.radio(
        "How many variables do you want to explore?",
        ["1 variable", "2 variables", "3 variables"],
        horizontal=True,
    )

    if mode == "1 variable":
        field = st.selectbox("Variable", numeric)
        st.plotly_chart(histogram(data, field), use_container_width=True)
        st.caption("Look at the distribution, spread, unusual values and missing data for one variable.")

    elif mode == "2 variables":
        if len(numeric) < 2:
            st.info("Add at least two numeric variables to the dataset to use this mode.")
            return
        x = st.selectbox("Horizontal axis", numeric, index=0)
        y = st.selectbox("Vertical axis", numeric, index=1)
        st.plotly_chart(scatter(data, x, y), use_container_width=True)
        st.caption("Look for a relationship, clusters, outliers and places where data are missing.")
        with st.expander("Dataset-specific analysis tools"):
            st.write(
                "A topic-specific app may add constrained filters, fitted models, scale controls or other tools here. "
                "Keep the underlying calculations outside this experience module."
            )

    else:
        if len(numeric) < 2:
            st.info("Add at least two numeric variables to the dataset to use this mode.")
            return
        x = st.selectbox("Horizontal axis", numeric, index=0, key="three_x")
        y = st.selectbox("Vertical axis", numeric, index=1, key="three_y")
        colour_options = [*categorical, *[column for column in numeric if column not in {x, y}]]
        if not colour_options:
            st.info("Add a third usable variable to the dataset to use this mode.")
            return
        colour = st.selectbox("Third variable — colour by", colour_options)
        st.plotly_chart(scatter(data, x, y, colour), use_container_width=True)
        st.caption("Use colour to ask whether a third variable helps explain the pattern between the first two.")

    with st.expander("Dataset preview"):
        st.dataframe(data, use_container_width=True, hide_index=True)
