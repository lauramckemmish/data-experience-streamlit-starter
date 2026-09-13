"""Stable open-ended Data Playground shell.

The master pattern is deliberately simple: one variable, two variables and
three variables. Dataset-specific projects may add constrained filtering,
model fitting or other analysis without changing this experience structure.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
import config

from charts import histogram, scatter
from data import column_profile, field_profile, scale_sample
from experiences import router
from ui_helpers import (
    graph_support,
    page_header,
    sample_note,
    scroll_to_top_if_requested,
    step_buttons,
    step_tabs,
    variable_card,
)


PLAYGROUND_LABELS = [
    "One variable",
    "Two variables",
    "Three variables",
    "Dataset preview",
]


def _axis_scale_control(label: str, key: str) -> bool:
    """Return whether an axis should use logarithmic spacing."""
    return st.segmented_control(
        label,
        ["Linear", "Log"],
        default="Linear",
        key=key,
        required=True,
    ) == "Log"


def render(data: pd.DataFrame) -> None:
    part = int(st.session_state.get("playground_part", 0))
    part = max(0, min(part, len(PLAYGROUND_LABELS) - 1))
    page_header("Data Playground", teacher_control=False)
    st.warning(config.DATASET_SOURCE_NOTE)
    st.write(
        "Choose one, two or three variables. Inspect the evidence, then decide what it supports."
    )

    profile = column_profile(data)
    numeric = profile["numeric"]
    categorical = profile["categorical"]

    if not numeric:
        st.warning("The current dataset has no numeric columns to plot.")
        st.dataframe(data, use_container_width=True)
        return

    _, selected = step_tabs(PLAYGROUND_LABELS, "playground_step_selector", part)
    if selected != part:
        part = selected
        st.session_state["playground_part"] = part
        st.session_state["playground_scroll_to_top"] = True
    scroll_to_top_if_requested("playground_scroll_to_top")

    if part == 0:
        st.caption("Choose a variable, then look for its shape, spread, unusual values and missing data.")
        field = st.selectbox("Variable", numeric)
        details = field_profile(data, field)
        variable_card(
            field,
            f"A numeric field in this example dataset. Use its values to compare records and look for spread or unusual values.",
            scale_note=f"{details['missing']:,} of {len(data):,} records have no value for this field.",
        )
        log_x = _axis_scale_control("Horizontal axis scale", "playground_one_log_x")
        sample = scale_sample(data, [field], log_x_field=field if log_x else None)
        sample_note(
            len(sample.data),
            sample.total,
            label="records",
            missing=sample.missing,
            log_x_excluded=sample.log_x_excluded,
            log_excluded=sample.log_excluded,
            x_label=field,
        )
        st.plotly_chart(histogram(sample.data, field, log_x=log_x), width="stretch")
        st.caption("What does this distribution show? What cannot it tell you on its own?")

    elif part == 1:
        if len(numeric) < 2:
            st.info("Add at least two numeric variables to the dataset to use this mode.")
        else:
            x = st.selectbox("Horizontal axis", numeric, index=0)
            y = st.selectbox("Vertical axis", numeric, index=1)
            scale_x, scale_y = st.columns(2)
            with scale_x:
                log_x = _axis_scale_control("Horizontal axis scale", "playground_two_log_x")
            with scale_y:
                log_y = _axis_scale_control("Vertical axis scale", "playground_two_log_y")
            sample = scale_sample(
                data,
                [x, y],
                log_x_field=x if log_x else None,
                log_y_field=y if log_y else None,
            )
            sample_note(
                len(sample.data),
                sample.total,
                label="records",
                missing=sample.missing,
                log_x_excluded=sample.log_x_excluded,
                log_y_excluded=sample.log_y_excluded,
                log_excluded=sample.log_excluded,
                x_label=x,
                y_label=y,
            )
            st.plotly_chart(scatter(sample.data, x, y, log_x=log_x, log_y=log_y), width="stretch")
            graph_support(
                f"The horizontal axis shows {x}; the vertical axis shows {y}.",
                "Look for a relationship, clusters, outliers and places where data are missing.",
            )
    elif part == 2:
        if len(numeric) < 2:
            st.info("Add at least two numeric variables to the dataset to use this mode.")
        else:
            x = st.selectbox("Horizontal axis", numeric, index=0, key="three_x")
            y = st.selectbox("Vertical axis", numeric, index=1, key="three_y")
            colour_options = [*categorical, *[column for column in numeric if column not in {x, y}]]
            if not colour_options:
                st.info("Add a third usable variable to the dataset to use this mode.")
            else:
                colour = st.selectbox("Third variable — colour by", colour_options)
                scale_x, scale_y = st.columns(2)
                with scale_x:
                    log_x = _axis_scale_control("Horizontal axis scale", "playground_three_log_x")
                with scale_y:
                    log_y = _axis_scale_control("Vertical axis scale", "playground_three_log_y")
                sample = scale_sample(
                    data,
                    [x, y, colour],
                    log_x_field=x if log_x else None,
                    log_y_field=y if log_y else None,
                )
                sample_note(
                    len(sample.data),
                    sample.total,
                    label="records",
                    missing=sample.missing,
                    log_x_excluded=sample.log_x_excluded,
                    log_y_excluded=sample.log_y_excluded,
                    log_excluded=sample.log_excluded,
                    x_label=x,
                    y_label=y,
                )
                st.plotly_chart(
                    scatter(sample.data, x, y, colour, log_x=log_x, log_y=log_y),
                    width="stretch",
                )
                st.caption("Does colour reveal a pattern, or does it mostly add noise? Check before inferring an explanation.")
    else:
        st.dataframe(data, use_container_width=True, hide_index=True)

    step_buttons(
        PLAYGROUND_LABELS,
        "playground_step_selector",
        "playground_part",
        "playground_scroll_to_top",
        part,
        "playground",
        terminal_action=router.go_home,
        terminal_label="Back to experiences",
    )
