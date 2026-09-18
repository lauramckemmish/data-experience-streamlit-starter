"""Focused checks for the starter's explicit Data Playground field contract."""

import pandas as pd

from data import (
    FIELD_KINDS,
    FIELD_METADATA,
    FieldMetadata,
    categorical_filter_fields,
    field_log_eligible,
    field_missingness,
    load_data,
    playground_fields,
    rejected_pair_reason,
    validate_field_metadata,
)


def test_every_configured_field_has_complete_valid_required_metadata():
    validate_field_metadata()
    assert set(FIELD_METADATA) == {field.name for field in FIELD_METADATA.values()}
    assert set(FIELD_METADATA) == set(load_data().columns)
    for field in FIELD_METADATA.values():
        assert field.kind in FIELD_KINDS
        assert field.label
        assert field.meaning
        assert field.role


def test_identifier_and_non_plottable_fields_cannot_be_generic_plot_choices():
    data = pd.DataFrame({name: [1] for name in FIELD_METADATA})
    one_variable = playground_fields(data, eligibility="one_variable")
    two_variable = playground_fields(data, eligibility="two_variable")

    assert "song_title" not in one_variable + two_variable
    assert "data_note" not in one_variable + two_variable


def test_plot_eligibility_is_configured_not_inferred_from_dataframe_dtype():
    data = pd.DataFrame({name: [1] for name in FIELD_METADATA})

    assert "release_year" in playground_fields(data, eligibility="one_variable")
    assert "song_title" not in playground_fields(data, eligibility="one_variable")
    assert FIELD_METADATA["album"].kind == "categorical"
    assert FIELD_METADATA["album"].one_variable


def test_log_eligibility_is_explicit_and_not_a_numeric_default():
    assert FIELD_METADATA["demo_streams_millions"].log_eligible
    assert not FIELD_METADATA["title_words"].log_eligible
    assert field_log_eligible("demo_streams_millions")
    assert not field_log_eligible("title_words")


def test_filter_eligibility_is_independent_of_categorical_plot_eligibility():
    data = pd.DataFrame(
        {
            "album": ["A", "B"],
            "demo_mood": ["calm", "bright"],
            **{name: [1, 2] for name in FIELD_METADATA if name not in {"album", "demo_mood"}},
        }
    )

    fields = categorical_filter_fields(data, metadata=FIELD_METADATA)

    assert fields == ["album", "demo_mood"]
    assert FIELD_METADATA["album"].one_variable
    assert FIELD_METADATA["demo_mood"].two_variable


def test_current_playground_choices_are_configured_for_each_supported_route():
    data = load_data()

    one_variable = playground_fields(data, eligibility="one_variable")
    two_variable = playground_fields(data, eligibility="two_variable")
    assert "song_title" not in one_variable + two_variable
    assert "data_note" not in one_variable + two_variable
    assert {"album", "demo_mood"}.issubset(one_variable)
    assert {"album", "demo_mood"}.issubset(two_variable)
    assert categorical_filter_fields(data, metadata=FIELD_METADATA) == ["album", "demo_mood"]


def test_categorical_plot_eligibility_respects_the_shared_cardinality_guardrail():
    data = load_data().copy()
    data["album"] = [f"album-{index}" for index in range(len(data))]

    assert "album" not in playground_fields(data, eligibility="one_variable")
    assert "demo_mood" in playground_fields(data, eligibility="one_variable")


def test_missingness_is_derived_from_source_data():
    data = pd.DataFrame({"demo_streams_millions": [1.0, None, None, 4.0]})

    assert field_missingness(data, "demo_streams_millions") == {
        "missing_count": 2,
        "missing_percentage": 50.0,
    }


def test_a_local_experience_can_reject_one_otherwise_valid_pair():
    rejected = {("demo_duration_min", "release_year"): "This comparison would mislead learners."}

    assert rejected_pair_reason("release_year", "demo_duration_min", pair_rejections=rejected) == (
        "This comparison would mislead learners."
    )
    assert rejected_pair_reason("release_year", "title_words", pair_rejections=rejected) is None


def test_invalid_identifier_plot_configuration_is_rejected():
    invalid = FieldMetadata(
        "record_id", "Record", "identifier", "An identifier.", "identifier", True, False
    )

    try:
        validate_field_metadata({"record_id": invalid})
    except ValueError as error:
        assert "cannot be a generic plot choice" in str(error)
    else:
        raise AssertionError("Invalid identifier plot eligibility was accepted.")
