"""Focused tests for the first four capability-driven Playground stages."""

import pandas as pd
import pytest

from charts import categorical_bar, count_heatmap, grouped_boxplot, histogram, scatter
from data import FIELD_METADATA, numeric_summary, playground_fields, playground_inventory, rejected_pair_reason
from experiences.data_playground import PLAYGROUND_LABELS


def test_first_four_playground_stages_are_in_the_canonical_order():
    assert PLAYGROUND_LABELS == ["Start here", "Know your data", "One variable", "Two variables"]


def test_inventory_includes_every_configured_field_and_source_missingness():
    data = pd.DataFrame({name: ["value", None] for name in FIELD_METADATA})

    inventory = playground_inventory(data)

    assert inventory["Variable"].tolist() == [field.label for field in FIELD_METADATA.values()]
    assert "Song title" in inventory["Variable"].tolist()
    assert "Data note" in inventory["Variable"].tolist()
    assert set(inventory["Missing data"]) == {"1 (50.0%)"}


def test_one_variable_chart_helpers_cover_numeric_and_categorical_routes():
    numeric = histogram(pd.DataFrame({"value": [1.0, 2.0, 3.0]}), "value", label="Value")
    categorical = categorical_bar(pd.DataFrame({"Category": ["A", "B"], "Count": [2, 1]}), label="Group")

    assert numeric.data[0].type == "histogram"
    assert categorical.data[0].type == "bar"


def test_raw_numeric_summary_does_not_depend_on_log_display():
    data = pd.DataFrame({"value": [0.1, 1.0, 10.0, None]})

    summary = numeric_summary(data, "value")
    assert summary == {
        "usable": 3,
        "missing": 1,
        "minimum": 0.1,
        "median": 1.0,
        "mean": pytest.approx(3.7),
        "maximum": 10.0,
    }


def test_two_variable_chart_helpers_dispatch_to_type_appropriate_representations():
    data = pd.DataFrame({"number": [1.0, 2.0, 3.0], "other": [2.0, 4.0, 6.0], "group": ["A", "A", "B"]})

    numeric_pair = scatter(data, "number", "other")
    grouped = grouped_boxplot(data, "group", "number", category_label="Group", numeric_label="Number")
    heatmap = count_heatmap(data, "group", "group", x_label="Group", y_label="Group")

    assert numeric_pair.data[0].type == "scatter"
    assert grouped.data[0].type == "box"
    assert heatmap.data[0].type == "heatmap"


def test_heatmap_annotations_make_counts_available_without_hover_and_keep_zeroes():
    data = pd.DataFrame({"x": ["A", "B"], "y": ["one", "two"]})

    figure = count_heatmap(data, "x", "y", x_label="X", y_label="Y")

    assert 0 in figure.data[0].z.flatten()
    assert "0" in {annotation.text for annotation in figure.layout.annotations}


def test_pair_rejection_is_available_to_the_two_variable_stage():
    rejected = {("album", "demo_mood"): "Use a different comparison."}

    assert rejected_pair_reason("demo_mood", "album", pair_rejections=rejected) == "Use a different comparison."


def test_identifier_and_non_plottable_fields_are_not_offered_by_either_analysis_stage():
    data = pd.DataFrame({name: [1] for name in FIELD_METADATA})

    fields = playground_fields(data, eligibility="one_variable") + playground_fields(data, eligibility="two_variable")
    assert "song_title" not in fields
    assert "data_note" not in fields
