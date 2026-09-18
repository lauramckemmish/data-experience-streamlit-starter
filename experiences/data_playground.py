"""Capability-driven six-stage shared Data Playground."""

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
    playground_grouping_fields,
    playground_fields,
    playground_inventory,
    rejected_pair_reason,
    scale_sample,
)
from experiences import router
from ui_helpers import (
    facilitator_live_cue,
    graph_support,
    notice_prompt,
    page_header,
    response_box,
    sample_note,
    scroll_to_top_if_requested,
    soft_reveal,
    step_buttons,
    step_tabs,
    variable_card,
)


PLAYGROUND_LABELS = [
    "Start here",
    "Know your data",
    "One variable",
    "Two variables",
    "Another angle",
    "Follow it further",
]


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


def _render_start() -> None:
    st.header("Explore the data")
    st.write(
        "Understand the data, inspect one variable, compare two, look again from another angle, "
        "then decide what evidence to seek next."
    )


def _render_inventory(data: pd.DataFrame) -> None:
    st.header("Know your data")
    st.write("Before making a graph, inspect what each field represents and what is missing from the dataset.")
    st.caption("This inventory includes every configured field, including fields that are not graph choices.")
    fields = playground_inventory(data).to_dict("records")
    for row_start in range(0, len(fields), 2):
        columns = st.columns(2, gap="medium")
        for column, field in zip(columns, fields[row_start : row_start + 2]):
            with column:
                with st.container(border=True):
                    st.markdown(f"**{field['Variable']}** · {field['Kind / role']}")
                    st.write(field["What it represents"])
                    st.caption(f"Unit: {field['Unit']} · Missing: {field['Missing data']}")


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
    st.write("Choose a variable and inspect its distribution or categories.")
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


def _render_two_numeric(
    data: pd.DataFrame,
    x: str,
    y: str,
    *,
    key_prefix: str,
    grouping_field: str | None = None,
) -> None:
    log_x = _axis_scale_control("Horizontal axis scale", f"{key_prefix}_log_x", eligible=field_log_eligible(x))
    log_y = _axis_scale_control("Vertical axis scale", f"{key_prefix}_log_y", eligible=field_log_eligible(y))
    required = [x, y] + ([grouping_field] if grouping_field else [])
    sample = scale_sample(data, required, log_x_field=x if log_x else None, log_y_field=y if log_y else None)
    sample_note(len(sample.data), sample.total, missing=sample.missing, log_x_excluded=sample.log_x_excluded, log_y_excluded=sample.log_y_excluded, log_both_excluded=sample.log_both_excluded, log_excluded=sample.log_excluded, x_label=_field_label(x), y_label=_field_label(y))
    if sample.data.empty:
        st.info(_empty_chart_message(log_x, log_y))
    else:
        st.plotly_chart(
            scatter(
                sample.data,
                x,
                y,
                group=grouping_field,
                group_label=_field_label(grouping_field) if grouping_field else None,
                x_label=_field_label(x),
                y_label=_field_label(y),
                log_x=log_x,
                log_y=log_y,
            ),
            width="stretch",
        )
    if grouping_field:
        st.caption(f"Groups show {_field_label(grouping_field)} using both colour and marker shape.")
    graph_support(f"The horizontal axis shows {_field_label(x)}; the vertical axis shows {_field_label(y)}.", "Look for direction, shape, spread, clusters, gaps and points sitting apart.")


def _render_categorical_numeric(data: pd.DataFrame, category: str, numeric: str, *, key_prefix: str) -> None:
    log_y = _axis_scale_control("Numerical axis scale", f"{key_prefix}_grouped_log", eligible=field_log_eligible(numeric))
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


def _render_two_variable_relationship(
    data: pd.DataFrame,
    x: str,
    y: str,
    *,
    key_prefix: str,
    grouping_field: str | None = None,
) -> None:
    """Render the established type-aware relationship, optionally grouped for comparison."""
    x_kind, y_kind = field_metadata(x).kind, field_metadata(y).kind
    if grouping_field and not (x_kind == y_kind == "numeric"):
        raise ValueError("Categorical grouping is only supported for numeric two-variable relationships.")
    if x_kind == y_kind == "numeric":
        _render_two_numeric(data, x, y, key_prefix=key_prefix, grouping_field=grouping_field)
    elif x_kind == y_kind == "categorical":
        _render_categorical_pair(data, x, y)
    else:
        category, numeric = (x, y) if x_kind == "categorical" else (y, x)
        _render_categorical_numeric(data, category, numeric, key_prefix=key_prefix)


def _relationship_fields(data: pd.DataFrame, *, key_prefix: str) -> tuple[str, str] | None:
    """Select a configured two-variable relationship, retaining a prior choice where possible."""
    fields = playground_fields(data, eligibility="two_variable")
    if len(fields) < 2:
        st.info("This dataset has fewer than two configured variables for comparison.")
        return None
    prior_x = st.session_state.get("playground_two_x", fields[0])
    prior_y = st.session_state.get("playground_two_y", fields[1])
    x_index = fields.index(prior_x) if prior_x in fields else 0
    y_index = fields.index(prior_y) if prior_y in fields else min(1, len(fields) - 1)
    left, right = st.columns(2)
    x = left.selectbox("First variable", fields, index=x_index, format_func=_field_label, key=f"{key_prefix}_x")
    y = right.selectbox("Second variable", fields, index=y_index, format_func=_field_label, key=f"{key_prefix}_y")
    if x == y:
        st.info("Choose two different variables to compare.")
        return None
    rejection = rejected_pair_reason(x, y)
    if rejection:
        st.info(f"This pairing is not available here: {rejection}")
        return None
    return x, y


def _render_two_variables(data: pd.DataFrame) -> None:
    st.header("Two variables")
    st.write("Choose two variables. The graph changes to suit the data you selected.")
    selected = _relationship_fields(data, key_prefix="playground_two")
    if selected is None:
        return
    x, y = selected
    x_kind, y_kind = field_metadata(x).kind, field_metadata(y).kind
    _render_two_variable_relationship(data, x, y, key_prefix="playground_two")
    notice_prompt("What do you notice?")
    with soft_reveal("What could I look for?"):
        if x_kind == y_kind == "numeric":
            st.write("Look for direction, shape, spread, clusters, gaps and values sitting apart.")
        elif x_kind == y_kind == "categorical":
            st.write("Look for common, rare and absent combinations, and whether some rows or columns dominate.")
        else:
            st.write("Look for group differences, overlap, spread and the number of records in each group.")


def _subset_caption(field: str, selected: list[object], available: list[object]) -> str:
    """Describe the active filtering state without treating a full selection as a subset."""
    if not selected:
        return f"Active subset: no {_field_label(field)} categories selected (0 records)."
    if set(selected) == set(available):
        return f"Active subset: all records (all {_field_label(field)} categories selected)."
    selected_text = ", ".join(str(value) for value in selected)
    return f"Active subset: {_field_label(field)} — {selected_text}."


def _render_another_angle(data: pd.DataFrame) -> None:
    st.header("Another angle")
    st.write("Does the pattern look the same from another angle?")
    selected = _relationship_fields(data, key_prefix="playground_angle")
    if selected is None:
        return
    x, y = selected
    additional_fields = {x, y}
    grouping_fields = [field for field in playground_grouping_fields(data) if field not in additional_fields]
    filter_fields = [
        field
        for field in categorical_filter_fields(data, metadata=FIELD_METADATA)
        if field not in additional_fields
    ]
    routes: list[str] = []
    if field_metadata(x).kind == field_metadata(y).kind == "numeric" and grouping_fields:
        routes.append("Compare groups")
    if filter_fields:
        routes.append("Compare a subset")
    if not routes:
        st.info("This dataset has no configured additional angle for this comparison.")
        return
    route = routes[0] if len(routes) == 1 else st.selectbox(
        "Look again by", routes, key="playground_angle_route"
    )
    if route == "Compare groups":
        group = st.selectbox(
            "Group by", grouping_fields, format_func=_field_label, key="playground_angle_group"
        )
        _render_two_variable_relationship(data, x, y, key_prefix="playground_angle_group", grouping_field=group)
    else:
        field = st.selectbox(
            "Subset by", filter_fields, format_func=_field_label, key="playground_angle_filter_field"
        )
        available = categorical_values(data, field)
        selected_categories = st.multiselect(
            "Categories to include", available, default=available, key=f"playground_angle_filter_values_{field}"
        )
        st.caption(_subset_caption(field, selected_categories, available))
        filtered_data = filter_categorical_values(data, field, selected_categories)
        _render_two_variable_relationship(filtered_data, x, y, key_prefix="playground_angle_filter")
    notice_prompt("What do you notice?")
    with soft_reveal("What could I compare?"):
        st.write(
            "What stayed similar? What changed? Is the original pattern still visible? "
            "If you selected a subset, what evidence is no longer available?"
        )
    facilitator_live_cue(
        "FACILITATION NOTE",
        "Ask what changed before offering an explanation. Another variable may complicate a pattern without causing it.",
    )


def _render_follow_it_further() -> None:
    st.header("Follow it further")
    st.write("Use an observation to decide what you would investigate next.")
    st.caption("Talk through these with a partner, or jot down a few words.")
    response_box(
        "What is one pattern you noticed?",
        "playground_follow_observation",
        sentence_starters="I noticed…",
        label="Observation",
        height=68,
    )
    response_box(
        "What does that make you wonder?",
        "playground_follow_question",
        sentence_starters="I wonder whether…",
        label="Question",
        height=68,
    )
    response_box(
        "What evidence could help you investigate that?",
        "playground_follow_evidence",
        sentence_starters="It would help to know…",
        label="Next evidence",
        height=68,
    )
    st.info("The graph can show a pattern. It does not automatically explain why the pattern exists.")
    facilitator_live_cue(
        "FACILITATION NOTE",
        "Ask what evidence could distinguish possible explanations.",
    )


def render(data: pd.DataFrame) -> None:
    part = max(0, min(int(st.session_state.get("playground_part", 0)), len(PLAYGROUND_LABELS) - 1))
    page_header("Data Playground")
    st.warning(config.DATASET_SOURCE_NOTE)
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
        _render_one_variable(data)
    elif part == 3:
        _render_two_variables(data)
    elif part == 4:
        _render_another_angle(data)
    else:
        _render_follow_it_further()
    step_buttons(PLAYGROUND_LABELS, "playground_step_selector", "playground_part", "playground_scroll_to_top", part, "playground", terminal_action=router.go_home, terminal_label="Back to experiences")
