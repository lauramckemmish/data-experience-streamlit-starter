"""Tests for the offline Data to Discovery portfolio manifest validator."""

from __future__ import annotations

import unittest
from pathlib import Path

from tools.portfolio_metadata_validator import load_manifest, validate_manifest


FIXTURES = Path(__file__).parent / "fixtures" / "portfolio_metadata"


class PortfolioMetadataValidatorTests(unittest.TestCase):
    def test_valid_synthetic_manifests_pass(self):
        for filename in (
            "valid_synthetic_exoplanets.json",
            "valid_synthetic_animal_traits.json",
            "valid_synthetic_frogid.json",
        ):
            with self.subTest(filename=filename):
                self.assertEqual(validate_manifest(load_manifest(FIXTURES / filename)), [])

    def test_invalid_synthetic_manifests_fail_for_their_intended_reasons(self):
        expected_errors = {
            "invalid_ids.json": "resource.resource_id must use lowercase kebab case",
            "invalid_duplicate_ids.json": "duplicates 'synthetic-duplicate/one'",
            "invalid_duration.json": "minimum must be less than or equal to",
            "invalid_controlled_values.json": "kind must be one of",
            "invalid_curriculum.json": "outcome_code must use official NESA outcome-code syntax",
        }
        for filename, expected_error in expected_errors.items():
            with self.subTest(filename=filename):
                errors = validate_manifest(load_manifest(FIXTURES / filename))
                self.assertTrue(any(expected_error in error for error in errors), errors)

    def test_relationship_targets_are_not_resolved_locally(self):
        manifest = load_manifest(FIXTURES / "valid_synthetic_frogid.json")
        experience = manifest["experiences"][0]
        experience["relationships"] = {
            "pairs_with": ["another-resource/future-experience"],
            "suggested_after": [],
        }
        self.assertEqual(validate_manifest(manifest), [])

    def test_relationship_self_reference_is_rejected(self):
        manifest = load_manifest(FIXTURES / "valid_synthetic_frogid.json")
        experience = manifest["experiences"][0]
        experience["relationships"] = {
            "pairs_with": [experience["experience_id"]],
        }
        errors = validate_manifest(manifest)
        self.assertTrue(any("must not self-reference" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
