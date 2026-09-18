"""Focused tests for the capability-driven Playground stages."""

import inspect

import pandas as pd
import pytest

from charts import categorical_bar, count_heatmap, grouped_boxplot, histogram, scatter
from data import (
    FIELD_METADATA,
    categorical_filter_fields,
    categorical_values,
    filter_categorical_values,
    numeric_summary,
    playground_fields,
    playground_grouping_fields,
    playground_inventory,
    rejected_pair_reason,
    scale_sample,
)
from experiences import data_playground
from experiences.data_playground import PLAYGROUND_LABELS, _subset_caption


def test_full_playground_journey_is_in_the_canonical_order():
    assert PLAYGROUND_LABELS == [
        "Start here",
        "Know your data",
        "One variable",
        "Two variables",
        "Another angle",
        "Follow it further",
    ]


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


def test_configured_categorical_grouping_uses_colour_and_marker_shape():
    data = pd.DataFrame(
        {
            "x": [1.0, 2.0, 3.0, 4.0],
            "y": [2.0, 3.0, 4.0, 5.0],
            "group": ["A", "A", "B", "B"],
        }
    )

    figure = scatter(data, "x", "y", group="group", group_label="Group")

    assert {trace.name for trace in figure.data} == {"A", "B"}
    assert len({trace.marker.symbol for trace in figure.data}) == 2
    assert figure.layout.legend.title.text == "Group"


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


def test_another_angle_offers_only_configured_bounded_grouping_and_filter_fields():
    data = pd.DataFrame(
        {
            "album": ["A", "A", "B", "B"],
            "demo_mood": ["calm", "bright", "calm", "bright"],
            **{name: [1, 2, 3, 4] for name in FIELD_METADATA if name not in {"album", "demo_mood"}},
        }
    )

    assert playground_grouping_fields(data) == ["album", "demo_mood"]
    assert categorical_filter_fields(data, metadata=FIELD_METADATA) == ["album", "demo_mood"]
    assert "song_title" not in playground_grouping_fields(data)
    assert "data_note" not in categorical_filter_fields(data, metadata=FIELD_METADATA)


def test_another_angle_subset_state_and_usable_rows_follow_the_selected_population():
    data = pd.DataFrame(
        {
            "album": ["A", "A", "B", "B"],
            "x": [1.0, None, 3.0, 4.0],
            "y": [2.0, 3.0, None, 5.0],
        }
    )
    available = categorical_values(data, "album")
    filtered = filter_categorical_values(data, "album", ["A"])
    sample = scale_sample(filtered, ["x", "y"])

    assert _subset_caption("album", ["A"], available) == "Active subset: Album — A."
    assert len(filtered) == 2
    assert sample.total == 2
    assert sample.missing == 1
    assert len(sample.data) == 1


def test_global_filter_is_absent_from_earlier_stages_and_continuous_colour_is_not_implemented():
    render_source = inspect.getsource(data_playground.render)
    another_angle_source = inspect.getsource(data_playground._render_another_angle)

    assert "categorical_filter_fields" not in render_source
    assert "Filter records" not in inspect.getsource(data_playground._render_start)
    assert "continuous" not in another_angle_source.lower()


def test_another_angle_and_follow_it_further_keep_observation_separate_from_explanation():
    another_angle_source = inspect.getsource(data_playground._render_another_angle)
    follow_source = inspect.getsource(data_playground._render_follow_it_further)

    assert "What do you notice?" in another_angle_source
    assert "pattern exists" in follow_source
    assert all(key in follow_source for key in ("observation", "question", "evidence"))
    assert "completion_gate" not in follow_source
