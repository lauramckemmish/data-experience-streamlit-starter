"""Capability-driven first four stages of the shared Data Playground."""

from __future__ import annotations

import math

import pandas as pd
import streamlit as st

import config
from charts import boxplot, categorical_bar, count_heatmap, grouped_boxplot, histogram, scatter
from data import (
    FIELD_METADATA,
    category_counts,
    categorical_filter_fields,
    categorical_values,
    field_log_eligible,
    field_metadata,
    filter_categorical_values,
    numeric_summary,
    playground_fields,
    playground_inventory,
    rejected_pair_reason,
    scale_sample,
)
from experiences import router
from ui_helpers import graph_support, notice_prompt, page_header, sample_note, scroll_to_top_if_requested, soft_reveal, step_buttons, step_tabs, variable_card


PLAYGROUND_LABELS = ["Start here", "Know your data", "One variable", "Two variables"]


def _field_label(field: str) -> str:
    return field_metadata(field).label


def _axis_scale_control(label: str, key: str, *, eligible: bool) -> bool:
    if not eligible:
        return False
    return st.segmented_control(label, ["Linear", "Log"], default="Linear", key=key, required=True) == "Log"


def _format_number(value: float) -> str:
    return "—" if math.isnan(value) else f"{value:,.4g}"


def _empty_chart_message(log_x: bool, log_y: bool = False) -> str:
    if log_x or log_y:
        return "No records can be plotted with this logarithmic scale. Choose Linear or fields with positive values."
    return "No records have all of the values needed for this chart. Choose different fields."


def _render_categorical_filter(data: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    """Retain the existing bounded filter as a supporting, not central, control."""
    fields = categorical_filter_fields(data, metadata=FIELD_METADATA)
    if not fields:
        return data, False
    with st.expander("Filter records", expanded=False):
        filter_field = st.selectbox("Filter by category", fields, format_func=_field_label, key="playground_filter_field")
        categories = categorical_values(data, filter_field)
        selected = st.multiselect("Categories to include", categories, default=categories, key=f"playground_filter_values_{filter_field}")
    filtered = filter_categorical_values(data, filter_field, selected)
    full_selection = set(selected) == set(categories)
    st.caption(f"Current population: {'all ' if full_selection else ''}{len(filtered):,} of {len(data):,} records.")
    if filtered.empty:
        st.info("No records match these categories. Choose at least one category to explore data.")
    return filtered, not full_selection


def _render_start() -> None:
    st.header("Explore the data")
    st.write("Start by understanding the available data. Then inspect one variable and compare two to look for patterns worth investigating.")


def _render_inventory(data: pd.DataFrame) -> None:
    st.header("Know your data")
    st.write("Before making a graph, inspect what each field represents and what is missing from the dataset.")
    st.caption("Missing data are calculated for the full dataset, not the current filter.")
    st.dataframe(
        playground_inventory(data), hide_index=True, width="stretch",
        column_config={
            "Variable": st.column_config.TextColumn(width="small"),
            "Kind / role": st.column_config.TextColumn(width="small"),
            "What it represents": st.column_config.TextColumn(width="medium"),
            "Unit": st.column_config.TextColumn(width="small"),
            "Missing data": st.column_config.TextColumn(width="small"),
        },
    )


def _render_numeric_one_variable(data: pd.DataFrame, field: str) -> None:
    metadata = field_metadata(field)
    log_x = _axis_scale_control("Horizontal axis scale", "playground_one_log_x", eligible=metadata.log_eligible)
    sample = scale_sample(data, [field], log_x_field=field if log_x else None)
    if sample.data.empty:
        st.info(_empty_chart_message(log_x))
    else:
        st.plotly_chart(histogram(sample.data, field, label=metadata.label, log_x=log_x), width="stretch")
    summary = numeric_summary(data, field)
    st.caption(f"Usable values: {summary['usable']:,} · Missing: {summary['missing']:,}")
    unit_suffix = f" ({metadata.unit})" if metadata.unit else ""
    minimum, median, mean, maximum = st.columns(4)
    minimum.metric(f"Minimum{unit_suffix}", _format_number(summary["minimum"]))
    median.metric(f"Median{unit_suffix}", _format_number(summary["median"]))
    mean.metric(f"Mean{unit_suffix}", _format_number(summary["mean"]))
    maximum.metric(f"Maximum{unit_suffix}", _format_number(summary["maximum"]))
    with soft_reveal("Another way to summarise this distribution"):
        if sample.data.empty:
            st.caption("No records are available for this display scale.")
        else:
            st.plotly_chart(boxplot(sample.data, field, label=metadata.label, log_y=log_x), width="stretch")
            st.caption("The box contains the middle half of the displayed values; its width does not show how many records are there.")


def _render_categorical_one_variable(data: pd.DataFrame, field: str) -> None:
    metadata = field_metadata(field)
    counts = category_counts(data, field)
    st.plotly_chart(categorical_bar(counts, label=metadata.label), width="stretch")
    st.caption(f"Usable values: {int(counts['Count'].sum()):,} · Missing: {len(data) - int(counts['Count'].sum()):,}")


def _render_one_variable(data: pd.DataFrame) -> None:
    st.header("One variable")
    st.write("Choose one approved variable and inspect its distribution or categories.")
    fields = playground_fields(data, eligibility="one_variable")
    if not fields:
        st.info("This dataset has no configured variables for one-variable exploration.")
        return
    field = st.selectbox("Variable", fields, format_func=_field_label, key="playground_one_field")
    metadata = field_metadata(field)
    variable_card(metadata.label, metadata.meaning, unit=metadata.unit)
    if metadata.kind == "numeric":
        _render_numeric_one_variable(data, field)
    else:
        _render_categorical_one_variable(data, field)
    notice_prompt("What do you notice?")
    with soft_reveal("What could I look for?"):
        if metadata.kind == "numeric":
            st.write("Look for where values cluster, how spread out they are, gaps, uneven shape, and values that sit apart.")
        else:
            st.write("Look for common and rare categories, imbalance, and how much of this field is missing.")


def _render_two_numeric(data: pd.DataFrame, x: str, y: str) -> None:
    log_x = _axis_scale_control("Horizontal axis scale", "playground_two_log_x", eligible=field_log_eligible(x))
    log_y = _axis_scale_control("Vertical axis scale", "playground_two_log_y", eligible=field_log_eligible(y))
    sample = scale_sample(data, [x, y], log_x_field=x if log_x else None, log_y_field=y if log_y else None)
    sample_note(len(sample.data), sample.total, missing=sample.missing, log_x_excluded=sample.log_x_excluded, log_y_excluded=sample.log_y_excluded, log_both_excluded=sample.log_both_excluded, log_excluded=sample.log_excluded, x_label=_field_label(x), y_label=_field_label(y))
    if sample.data.empty:
        st.info(_empty_chart_message(log_x, log_y))
    else:
        st.plotly_chart(scatter(sample.data, x, y, x_label=_field_label(x), y_label=_field_label(y), log_x=log_x, log_y=log_y), width="stretch")
    graph_support(f"The horizontal axis shows {_field_label(x)}; the vertical axis shows {_field_label(y)}.", "Look for direction, shape, spread, clusters, gaps and points sitting apart.")


def _render_categorical_numeric(data: pd.DataFrame, category: str, numeric: str) -> None:
    log_y = _axis_scale_control("Numerical axis scale", "playground_two_grouped_log", eligible=field_log_eligible(numeric))
    sample = scale_sample(data, [category, numeric], log_y_field=numeric if log_y else None)
    sample_note(len(sample.data), sample.total, missing=sample.missing, log_y_excluded=sample.log_y_excluded, log_excluded=sample.log_excluded, y_label=_field_label(numeric))
    if sample.data.empty:
        st.info(_empty_chart_message(False, log_y))
    else:
        st.plotly_chart(grouped_boxplot(sample.data, category, numeric, category_label=_field_label(category), numeric_label=_field_label(numeric), log_y=log_y), width="stretch")
    graph_support(f"Each group shows {_field_label(numeric)} for {_field_label(category)}.", "Look for group differences, overlap, spread and values sitting apart.")


def _render_categorical_pair(data: pd.DataFrame, x: str, y: str) -> None:
    sample = data.dropna(subset=[x, y])
    sample_note(len(sample), len(data), missing=len(data) - len(sample))
    if sample.empty:
        st.info(_empty_chart_message(False))
    else:
        st.plotly_chart(count_heatmap(sample, x, y, x_label=_field_label(x), y_label=_field_label(y)), width="stretch")
    graph_support(f"Each cell counts records with both {_field_label(x)} and {_field_label(y)}.", "Look for common, rare and absent combinations.")


def _render_two_variables(data: pd.DataFrame) -> None:
    st.header("Two variables")
    st.write("Choose two approved variables. The graph changes to suit the data you selected.")
    fields = playground_fields(data, eligibility="two_variable")
    if len(fields) < 2:
        st.info("This dataset has fewer than two configured variables for comparison.")
        return
    left, right = st.columns(2)
    x = left.selectbox("First variable", fields, format_func=_field_label, key="playground_two_x")
    y = right.selectbox("Second variable", fields, index=1 if len(fields) > 1 else 0, format_func=_field_label, key="playground_two_y")
    if x == y:
        st.info("Choose two different variables to compare.")
        return
    rejection = rejected_pair_reason(x, y)
    if rejection:
        st.info(f"This pairing is not available here: {rejection}")
        return
    x_kind, y_kind = field_metadata(x).kind, field_metadata(y).kind
    if x_kind == y_kind == "numeric":
        _render_two_numeric(data, x, y)
    elif x_kind == y_kind == "categorical":
        _render_categorical_pair(data, x, y)
    else:
        category, numeric = (x, y) if x_kind == "categorical" else (y, x)
        _render_categorical_numeric(data, category, numeric)
    notice_prompt("What do you notice?")
    with soft_reveal("What could I look for?"):
        if x_kind == y_kind == "numeric":
            st.write("Look for direction, shape, spread, clusters, gaps and values sitting apart.")
        elif x_kind == y_kind == "categorical":
            st.write("Look for common, rare and absent combinations, and whether some rows or columns dominate.")
        else:
            st.write("Look for group differences, overlap, spread and the number of records in each group.")


def render(data: pd.DataFrame) -> None:
    part = max(0, min(int(st.session_state.get("playground_part", 0)), len(PLAYGROUND_LABELS) - 1))
    page_header("Data Playground")
    st.warning(config.DATASET_SOURCE_NOTE)
    filtered_data, _ = _render_categorical_filter(data)
    _, selected = step_tabs(PLAYGROUND_LABELS, "playground_step_selector", part)
    if selected != part:
        part = selected
        st.session_state["playground_part"] = part
        st.session_state["playground_scroll_to_top"] = True
    scroll_to_top_if_requested("playground_scroll_to_top")
    if part == 0:
        _render_start()
    elif part == 1:
        _render_inventory(data)
    elif part == 2:
        _render_one_variable(filtered_data)
    else:
        _render_two_variables(filtered_data)
    step_buttons(PLAYGROUND_LABELS, "playground_step_selector", "playground_part", "playground_scroll_to_top", part, "playground", terminal_action=router.go_home, terminal_label="Back to experiences")
