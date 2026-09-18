"""Offline structural validation for Data to Discovery portfolio manifests.

The validator deliberately makes no network requests. URL reachability,
redirects, and hosting health are operational checks for a future portfolio.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from tools.portfolio_metadata_registry import GLOBAL_UMBRELLAS


SCHEMA_VERSION = "data-to-discovery/1.0"
ALLOWED_KINDS = {"guided_experience", "explore_resource"}
ALLOWED_STAGES = {
    "Early Stage 1",
    "Stage 1",
    "Stage 2",
    "Stage 3",
    "Stage 4",
    "Stage 5",
    "Stage 6",
}
ALLOWED_DELIVERY_MODES = {"facilitated", "classroom", "independent"}
ALLOWED_EVIDENCE_TYPES = {
    "observational_measurements",
    "scientific_catalogue",
    "curated_dataset",
    "derived_model",
    "simulation",
    "external_reference_data",
    "citizen_science",
}
ALLOWED_ALIGNMENTS = {"DIRECT", "PARTIAL", "POTENTIAL", "NOT_ADDRESSED"}

_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_EXPERIENCE_ID_PATTERN = re.compile(r"^([a-z0-9]+(?:-[a-z0-9]+)*)/([a-z0-9]+(?:-[a-z0-9]+)*)$")
_FOCUS_TOKEN_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_PROGRAMME_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*$")
_OUTCOME_CODE_PATTERN = re.compile(r"^[A-Z]{2,6}[0-9]+(?:-[A-Z0-9]+)+$")
_CONTENT_SUFFIX_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*$")

_RESOURCE_FIELDS = ("resource_id", "title", "summary", "repository", "app_url")
_EXPERIENCE_FIELDS = (
    "experience_id",
    "title",
    "summary",
    "kind",
    "published",
    "stages",
    "duration_minutes",
    "science_focus",
    "data_science_focus",
    "curriculum",
    "umbrellas",
    "delivery_modes",
    "programmes",
    "evidence_types",
    "launch",
)


def load_manifest(path: str | Path) -> Any:
    """Load a JSON manifest without performing any remote access."""
    with Path(path).open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


def validate_manifest(manifest: Any) -> list[str]:
    """Return structural contract errors for one parsed manifest."""
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["manifest must be an object"]

    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}")

    resource = manifest.get("resource")
    resource_id = _validate_resource(resource, errors)

    experiences = manifest.get("experiences")
    if not isinstance(experiences, list):
        errors.append("experiences must be a list")
        return errors

    seen_ids: set[str] = set()
    for index, experience in enumerate(experiences):
        path = f"experiences[{index}]"
        experience_id = _validate_experience(experience, resource_id, path, errors)
        if experience_id:
            if experience_id in seen_ids:
                errors.append(f"{path}.experience_id duplicates {experience_id!r}")
            seen_ids.add(experience_id)

    return errors


def _validate_resource(resource: Any, errors: list[str]) -> str | None:
    if not isinstance(resource, dict):
        errors.append("resource must be an object")
        return None
    _require_keys(resource, _RESOURCE_FIELDS, "resource", errors)
    resource_id = resource.get("resource_id")
    if not _is_nonblank_string(resource_id):
        errors.append("resource.resource_id must be a nonblank string")
        return None
    if not _ID_PATTERN.fullmatch(resource_id):
        errors.append("resource.resource_id must use lowercase kebab case")
    for field in ("title", "summary"):
        if not _is_nonblank_string(resource.get(field)):
            errors.append(f"resource.{field} must be a nonblank string")
    for field in ("repository", "app_url"):
        if not _is_https_url(resource.get(field)):
            errors.append(f"resource.{field} must be an HTTPS URL")
    return resource_id


def _validate_experience(
    experience: Any,
    resource_id: str | None,
    path: str,
    errors: list[str],
) -> str | None:
    if not isinstance(experience, dict):
        errors.append(f"{path} must be an object")
        return None
    _require_keys(experience, _EXPERIENCE_FIELDS, path, errors)
    experience_id = experience.get("experience_id")
    _validate_experience_id(experience_id, resource_id, path, errors)
    for field in ("title", "summary"):
        if not _is_nonblank_string(experience.get(field)):
            errors.append(f"{path}.{field} must be a nonblank string")

    if experience.get("kind") not in ALLOWED_KINDS:
        errors.append(f"{path}.kind must be one of {sorted(ALLOWED_KINDS)}")
    if not isinstance(experience.get("published"), bool):
        errors.append(f"{path}.published must be a boolean")

    _validate_string_list(experience.get("stages"), f"{path}.stages", errors, allowed=ALLOWED_STAGES)
    _validate_duration(experience.get("duration_minutes"), f"{path}.duration_minutes", errors)
    _validate_string_list(
        experience.get("science_focus"),
        f"{path}.science_focus",
        errors,
        token_pattern=_FOCUS_TOKEN_PATTERN,
        nonempty=True,
    )
    _validate_string_list(
        experience.get("data_science_focus"),
        f"{path}.data_science_focus",
        errors,
        token_pattern=_FOCUS_TOKEN_PATTERN,
        nonempty=True,
    )
    _validate_curriculum(experience.get("curriculum"), f"{path}.curriculum", errors)
    _validate_umbrellas(experience.get("umbrellas"), f"{path}.umbrellas", errors)
    _validate_string_list(
        experience.get("delivery_modes"),
        f"{path}.delivery_modes",
        errors,
        allowed=ALLOWED_DELIVERY_MODES,
    )
    _validate_string_list(
        experience.get("programmes"),
        f"{path}.programmes",
        errors,
        token_pattern=_PROGRAMME_PATTERN,
    )
    _validate_string_list(
        experience.get("evidence_types"),
        f"{path}.evidence_types",
        errors,
        allowed=ALLOWED_EVIDENCE_TYPES,
        nonempty=True,
    )
    _validate_launch(experience.get("launch"), experience.get("published"), f"{path}.launch", errors)
    _validate_thumbnail(experience.get("thumbnail"), f"{path}.thumbnail", errors)
    _validate_relationships(experience.get("relationships"), experience_id, f"{path}.relationships", errors)

    return experience_id if isinstance(experience_id, str) else None


def _validate_experience_id(value: Any, resource_id: str | None, path: str, errors: list[str]) -> None:
    if not _is_nonblank_string(value):
        errors.append(f"{path}.experience_id must be a nonblank string")
        return
    match = _EXPERIENCE_ID_PATTERN.fullmatch(value)
    if not match:
        errors.append(f"{path}.experience_id must be resource-id/experience-slug")
    elif resource_id and match.group(1) != resource_id:
        errors.append(f"{path}.experience_id must start with {resource_id!r}/")


def _validate_duration(value: Any, path: str, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        errors.append(f"{path} must be null or an object")
        return
    if set(value) != {"minimum", "maximum"}:
        errors.append(f"{path} must contain only minimum and maximum")
        return
    minimum = value.get("minimum")
    maximum = value.get("maximum")
    if not _is_positive_int(minimum) or not _is_positive_int(maximum):
        errors.append(f"{path}.minimum and {path}.maximum must be positive integers")
    elif minimum > maximum:
        errors.append(f"{path}.minimum must be less than or equal to {path}.maximum")


def _validate_curriculum(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{path} must be a list")
        return
    for index, framework_entry in enumerate(value):
        entry_path = f"{path}[{index}]"
        if not isinstance(framework_entry, dict):
            errors.append(f"{entry_path} must be an object")
            continue
        _require_keys(framework_entry, ("framework", "outcomes"), entry_path, errors)
        if not _is_nonblank_string(framework_entry.get("framework")):
            errors.append(f"{entry_path}.framework must be a nonblank string")
        outcomes = framework_entry.get("outcomes")
        if not isinstance(outcomes, list):
            errors.append(f"{entry_path}.outcomes must be a list")
            continue
        for outcome_index, outcome in enumerate(outcomes):
            outcome_path = f"{entry_path}.outcomes[{outcome_index}]"
            if not isinstance(outcome, dict):
                errors.append(f"{outcome_path} must be an object")
                continue
            _require_keys(outcome, ("outcome_code", "alignment", "detailed_content"), outcome_path, errors)
            outcome_code = outcome.get("outcome_code")
            if not _is_nonblank_string(outcome_code) or not _OUTCOME_CODE_PATTERN.fullmatch(outcome_code):
                errors.append(f"{outcome_path}.outcome_code must use official NESA outcome-code syntax")
            if outcome.get("alignment") not in ALLOWED_ALIGNMENTS:
                errors.append(f"{outcome_path}.alignment must be an allowed alignment")
            detailed_content = outcome.get("detailed_content")
            if not isinstance(detailed_content, list):
                errors.append(f"{outcome_path}.detailed_content must be a list")
                continue
            for content_index, content in enumerate(detailed_content):
                content_path = f"{outcome_path}.detailed_content[{content_index}]"
                if not isinstance(content, dict):
                    errors.append(f"{content_path} must be an object")
                    continue
                _require_keys(content, ("content_id", "alignment"), content_path, errors)
                content_id = content.get("content_id")
                expected_prefix = f"{outcome_code}." if isinstance(outcome_code, str) else ""
                if not _is_nonblank_string(content_id) or not content_id.startswith(expected_prefix):
                    errors.append(f"{content_path}.content_id must begin with its outcome code")
                elif not _CONTENT_SUFFIX_PATTERN.fullmatch(content_id.removeprefix(expected_prefix)):
                    errors.append(f"{content_path}.content_id has an invalid detailed-content suffix")
                if content.get("alignment") not in ALLOWED_ALIGNMENTS:
                    errors.append(f"{content_path}.alignment must be an allowed alignment")


def _validate_umbrellas(value: Any, path: str, errors: list[str]) -> None:
    _validate_string_list(value, path, errors, token_pattern=_ID_PATTERN)
    if isinstance(value, list):
        for umbrella in value:
            if isinstance(umbrella, str) and umbrella not in GLOBAL_UMBRELLAS:
                errors.append(f"{path} contains unregistered global umbrella {umbrella!r}")


def _validate_launch(value: Any, published: Any, path: str, errors: list[str]) -> None:
    if published is True:
        if not isinstance(value, dict):
            errors.append(f"{path} must be an object when published is true")
            return
        if not _is_https_url(value.get("url")):
            errors.append(f"{path}.url must be an HTTPS URL")
    elif published is False and value is not None:
        errors.append(f"{path} must be null when published is false")
    elif published is not True and published is not False:
        return


def _validate_thumbnail(value: Any, path: str, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        errors.append(f"{path} must be an object when present")
        return
    if not _is_https_url(value.get("url")):
        errors.append(f"{path}.url must be an HTTPS URL")
    if not _is_nonblank_string(value.get("alt")):
        errors.append(f"{path}.alt must be a nonblank string")
    if "caption" in value and value["caption"] is not None and not _is_nonblank_string(value["caption"]):
        errors.append(f"{path}.caption must be a nonblank string or null")


def _validate_relationships(value: Any, experience_id: Any, path: str, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        errors.append(f"{path} must be an object when present")
        return
    for relationship_name in ("pairs_with", "suggested_after"):
        if relationship_name not in value:
            continue
        relationship_path = f"{path}.{relationship_name}"
        references = value[relationship_name]
        _validate_string_list(references, relationship_path, errors)
        if isinstance(references, list):
            for reference in references:
                if isinstance(reference, str) and not _EXPERIENCE_ID_PATTERN.fullmatch(reference):
                    errors.append(f"{relationship_path} contains an invalid experience ID")
                if reference == experience_id:
                    errors.append(f"{relationship_path} must not self-reference")


def _validate_string_list(
    value: Any,
    path: str,
    errors: list[str],
    *,
    allowed: set[str] | None = None,
    token_pattern: re.Pattern[str] | None = None,
    nonempty: bool = False,
) -> None:
    if not isinstance(value, list):
        errors.append(f"{path} must be a list")
        return
    if nonempty and not value:
        errors.append(f"{path} must not be empty")
    seen: set[str] = set()
    for item in value:
        if not _is_nonblank_string(item):
            errors.append(f"{path} values must be nonblank strings")
            continue
        if item in seen:
            errors.append(f"{path} must not contain duplicate values")
        seen.add(item)
        if allowed is not None and item not in allowed:
            errors.append(f"{path} contains invalid value {item!r}")
        if token_pattern is not None and not token_pattern.fullmatch(item):
            errors.append(f"{path} contains invalid token {item!r}")


def _require_keys(value: dict[str, Any], keys: tuple[str, ...], path: str, errors: list[str]) -> None:
    for key in keys:
        if key not in value:
            errors.append(f"{path} is missing required key {key!r}")


def _is_nonblank_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _is_https_url(value: Any) -> bool:
    if not _is_nonblank_string(value) or any(character.isspace() for character in value):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc) and parsed.username is None and parsed.password is None
