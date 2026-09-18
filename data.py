"""Shared data-loading helpers.

For a new project, replace the bundled demo CSV or change DEFAULT_DATA_PATH.
Experience modules should receive a dataframe rather than loading data themselves.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Mapping

import numpy as np
import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = APP_DIR / "data" / "taylor_swift_demo_dataset.csv"


FieldKind = Literal["numeric", "categorical", "identifier", "non-plottable"]
FIELD_KINDS = frozenset({"numeric", "categorical", "identifier", "non-plottable"})
FIELD_ROLES = frozenset({"identifier", "context", "measure", "descriptor", "provenance"})
DEFAULT_CATEGORICAL_CARDINALITY_LIMIT = 12


@dataclass(frozen=True)
class FieldMetadata:
    """Dataset-supplied metadata for shared Data Playground machinery.

    Eligibility is deliberately explicit: a pandas dtype can describe stored
    values, but cannot determine whether a field makes a useful or truthful
    learner-facing analysis choice.
    """

    name: str
    label: str
    kind: FieldKind
    meaning: str
    role: str
    one_variable: bool
    two_variable: bool
    unit: str | None = None
    log_eligible: bool = False
    filter_eligible: bool = False
    another_angle_eligible: bool = False
    category_limit: int | None = None
    category_order: tuple[str, ...] | None = None


# This small configuration is the starter's single source of field truth. A
# derived resource should replace it with its own scientifically and
# pedagogically justified choices rather than infer them from dataframe dtypes.
FIELD_METADATA: dict[str, FieldMetadata] = {
    "song_title": FieldMetadata(
        "song_title", "Song title", "identifier", "The title used to identify a song record.",
        "identifier", False, False,
    ),
    "album": FieldMetadata(
        "album", "Album", "categorical", "The album label associated with the song.",
        "context", True, True, filter_eligible=True, another_angle_eligible=True,
    ),
    "release_year": FieldMetadata(
        "release_year", "Release year", "numeric", "The year associated with the album release.",
        "context", True, True,
    ),
    "title_words": FieldMetadata(
        "title_words", "Title words", "numeric", "The number of words in the song title.",
        "measure", True, True,
    ),
    "title_characters": FieldMetadata(
        "title_characters", "Title characters", "numeric", "The number of characters in the song title.",
        "measure", True, True,
    ),
    "demo_duration_min": FieldMetadata(
        "demo_duration_min", "Demo duration", "numeric", "A synthetic demonstration duration value.",
        "measure", True, True, unit="minutes",
    ),
    "demo_energy_score": FieldMetadata(
        "demo_energy_score", "Demo energy score", "numeric", "A synthetic demonstration energy score.",
        "measure", True, True,
    ),
    "demo_danceability_score": FieldMetadata(
        "demo_danceability_score", "Demo danceability score", "numeric", "A synthetic demonstration danceability score.",
        "measure", True, True,
    ),
    "demo_streams_millions": FieldMetadata(
        "demo_streams_millions", "Demo streams", "numeric", "A synthetic demonstration streams value.",
        "measure", True, True, unit="millions", log_eligible=True,
    ),
    "demo_mood": FieldMetadata(
        "demo_mood", "Demo mood", "categorical", "A synthetic demonstration mood label.",
        "descriptor", True, True, filter_eligible=True, another_angle_eligible=True,
    ),
    "data_note": FieldMetadata(
        "data_note", "Data note", "non-plottable", "A note that identifies the synthetic demonstration data.",
        "provenance", False, False,
    ),
}

# A local experience may reject a misleading otherwise-valid pair with a
# canonical tuple and a short reason. Keep this empty unless the dataset needs
# it; generic type dispatch remains the default.
PLAYGROUND_PAIR_REJECTIONS: dict[tuple[str, str], str] = {}


def canonical_pair(first: str, second: str) -> tuple[str, str]:
    """Return a stable unordered-pair key for the lightweight escape hatch."""
    return tuple(sorted((first, second)))


def rejected_pair_reason(
    first: str,
    second: str,
    *,
    pair_rejections: Mapping[tuple[str, str], str] | None = None,
) -> str | None:
    """Return a locally configured reason to suppress an otherwise-valid pair."""
    rejections = PLAYGROUND_PAIR_REJECTIONS if pair_rejections is None else pair_rejections
    return rejections.get(canonical_pair(first, second))


def validate_field_metadata(metadata: Mapping[str, FieldMetadata] = FIELD_METADATA) -> None:
    """Raise ``ValueError`` when a field contract is incomplete or contradictory."""
    for configured_name, field in metadata.items():
        if configured_name != field.name:
            raise ValueError(f"Field metadata key {configured_name!r} must match its internal name.")
        if not field.label or not field.meaning or not field.role:
            raise ValueError(f"Field metadata for {field.name!r} requires label, meaning, and role.")
        if field.kind not in FIELD_KINDS:
            raise ValueError(f"Field metadata for {field.name!r} has an invalid kind: {field.kind!r}.")
        if field.role not in FIELD_ROLES:
            raise ValueError(f"Field metadata for {field.name!r} has an invalid role: {field.role!r}.")
        if field.kind in {"identifier", "non-plottable"} and (field.one_variable or field.two_variable):
            raise ValueError(f"{field.kind} field {field.name!r} cannot be a generic plot choice.")
        if field.log_eligible and field.kind != "numeric":
            raise ValueError(f"Only numeric field {field.name!r} can be log eligible.")
        if field.filter_eligible and field.kind != "categorical":
            raise ValueError(f"Only categorical field {field.name!r} can be filter eligible.")
        if field.category_limit is not None and field.category_limit < 2:
            raise ValueError(f"Field {field.name!r} needs a category limit of at least two.")


def playground_fields(data: pd.DataFrame, *, eligibility: Literal["one_variable", "two_variable"]) -> list[str]:
    """Return configured eligible fields present in this dataset, in source order."""
    validate_field_metadata()
    return [
        field.name
        for field in FIELD_METADATA.values()
        if field.name in data.columns and getattr(field, eligibility)
        and (
            field.kind != "categorical"
            or data[field.name].nunique(dropna=True)
            <= (field.category_limit or DEFAULT_CATEGORICAL_CARDINALITY_LIMIT)
        )
    ]


def playground_grouping_fields(data: pd.DataFrame) -> list[str]:
    """Return configured categorical fields suitable for a later grouping route."""
    validate_field_metadata()
    return [
        field.name
        for field in FIELD_METADATA.values()
        if field.name in data.columns and field.kind == "categorical" and field.another_angle_eligible
    ]


def field_metadata(field: str) -> FieldMetadata:
    """Return configured metadata for a field used by the Playground."""
    return FIELD_METADATA[field]


def fields_of_kind(
    data: pd.DataFrame,
    *,
    eligibility: Literal["one_variable", "two_variable"],
    kind: FieldKind,
) -> list[str]:
    """Return configured eligible fields of one learner-facing data kind."""
    return [
        field
        for field in playground_fields(data, eligibility=eligibility)
        if FIELD_METADATA[field].kind == kind
    ]


def field_log_eligible(field: str) -> bool:
    """Return configured log-display eligibility for one known field."""
    return FIELD_METADATA[field].log_eligible


def field_missingness(data: pd.DataFrame, field: str) -> dict[str, int | float]:
    """Calculate full-dataset missingness rather than storing it in metadata."""
    missing_count = int(data[field].isna().sum())
    total = len(data)
    return {
        "missing_count": missing_count,
        "missing_percentage": 0.0 if total == 0 else missing_count / total * 100,
    }


def playground_inventory(data: pd.DataFrame) -> pd.DataFrame:
    """Return a learner-facing full-dataset inventory from configured metadata."""
    rows = []
    for metadata in FIELD_METADATA.values():
        if metadata.name not in data.columns:
            continue
        missingness = field_missingness(data, metadata.name)
        rows.append(
            {
                "Variable": metadata.label,
                "Kind / role": f"{metadata.kind} · {metadata.role}",
                "What it represents": metadata.meaning,
                "Unit": metadata.unit or "—",
                "Missing data": (
                    f"{missingness['missing_count']:,} ({missingness['missing_percentage']:.1f}%)"
                ),
            }
        )
    return pd.DataFrame(rows)


def numeric_summary(data: pd.DataFrame, field: str) -> dict[str, float | int]:
    """Summarise raw numeric values without applying any display transformation."""
    values = pd.to_numeric(data[field], errors="coerce")
    usable = values.dropna()
    return {
        "usable": len(usable),
        "missing": int(values.isna().sum()),
        "minimum": float(usable.min()) if not usable.empty else np.nan,
        "median": float(usable.median()) if not usable.empty else np.nan,
        "mean": float(usable.mean()) if not usable.empty else np.nan,
        "maximum": float(usable.max()) if not usable.empty else np.nan,
    }


def category_counts(data: pd.DataFrame, field: str) -> pd.DataFrame:
    """Return raw category counts, retaining a configured preferred order when supplied."""
    values = data[field].dropna()
    counts = values.value_counts().rename_axis("Category").reset_index(name="Count")
    order = FIELD_METADATA[field].category_order
    if order:
        rank = {category: position for position, category in enumerate(order)}
        counts["_rank"] = counts["Category"].map(rank).fillna(len(rank))
        counts = counts.sort_values(["_rank", "Category"], kind="stable").drop(columns="_rank")
    return counts


@st.cache_data
def load_data(path: str | Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load the project dataset."""
    return pd.read_csv(path)


def column_profile(data: pd.DataFrame) -> dict[str, list[str]]:
    """Return simple column groups useful across generic experiences."""
    numeric = data.select_dtypes(include="number").columns.tolist()
    categorical = [column for column in data.columns if column not in numeric]
    return {"numeric": numeric, "categorical": categorical}


def categorical_filter_fields(
    data: pd.DataFrame,
    *,
    max_categories: int = DEFAULT_CATEGORICAL_CARDINALITY_LIMIT,
    metadata: Mapping[str, FieldMetadata] | None = None,
) -> list[str]:
    """Return bounded categorical filter fields.

    Supplying field metadata makes eligibility an explicit dataset decision. The
    dtype-only fallback remains for small generic helpers and test data that do
    not have an experience-specific field contract.
    """
    if metadata is not None:
        validate_field_metadata(metadata)
        return [
            field.name
            for field in metadata.values()
            if field.name in data.columns
            and field.kind == "categorical"
            and field.filter_eligible
            and 2 <= data[field.name].nunique(dropna=True) <= (field.category_limit or max_categories)
        ]
    return [
        field
        for field in column_profile(data)["categorical"]
        if 2 <= data[field].nunique(dropna=True) <= max_categories
    ]


def categorical_values(data: pd.DataFrame, field: str) -> list[object]:
    """Return stable, present category values for one eligible filter field."""
    return sorted(data[field].dropna().unique().tolist(), key=str)


def filter_categorical_values(
    data: pd.DataFrame,
    field: str,
    selected: list[object],
) -> pd.DataFrame:
    """Filter one categorical field, treating all selected categories as unfiltered.

    Selected categories are combined by union. Selecting every available category
    deliberately retains rows with a missing value in the filter field too, so the
    full-dataset state remains identical to the unfiltered dataset.
    """
    available = categorical_values(data, field)
    if set(selected) == set(available):
        return data.copy()
    return data.loc[data[field].isin(selected)].copy()


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


@dataclass(frozen=True)
class ScaleSample:
    """Rows usable for an analysis, with missing and log-scale exclusions separate."""

    data: pd.DataFrame
    total: int
    missing: int
    log_x_excluded: int
    log_y_excluded: int
    log_both_excluded: int
    log_excluded: int


def scale_sample(
    data: pd.DataFrame,
    required: list[str],
    *,
    log_x_field: str | None = None,
    log_y_field: str | None = None,
) -> ScaleSample:
    """Prepare complete rows and remove values invalid for selected log axes.

    ``missing`` counts rows without a required value. ``log_x_excluded`` and
    ``log_y_excluded`` count the selected complete rows with invalid values on
    their respective axes; ``log_excluded`` is their non-overlapping union.
    A logarithmic axis can only display finite, positive values.
    """
    complete_mask = data[required].notna().all(axis=1)
    complete = data.loc[complete_mask]

    def invalid_for_log(field: str | None) -> pd.Series:
        if field is None:
            return pd.Series(False, index=complete.index)
        values = complete[field]
        return values.le(0) | ~pd.Series(np.isfinite(values), index=complete.index)

    log_x_mask = invalid_for_log(log_x_field)
    log_y_mask = invalid_for_log(log_y_field)
    log_mask = log_x_mask | log_y_mask
    return ScaleSample(
        data=complete.loc[~log_mask],
        total=len(data),
        missing=int((~complete_mask).sum()),
        log_x_excluded=int(log_x_mask.sum()),
        log_y_excluded=int(log_y_mask.sum()),
        log_both_excluded=int((log_x_mask & log_y_mask).sum()),
        log_excluded=int(log_mask.sum()),
    )
