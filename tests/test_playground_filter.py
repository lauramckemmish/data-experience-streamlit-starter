"""Focused tests for the Data Playground's bounded categorical filter."""

import unittest

import pandas as pd

from data import (
    categorical_filter_fields,
    categorical_values,
    filter_categorical_values,
    scale_sample,
)


class PlaygroundFilterTests(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame(
            {
                "category": ["A", "A", "A", "B", "B", "C"],
                "x": [1.0, 0.0, None, 4.0, 5.0, 6.0],
                "y": [2.0, 3.0, 4.0, 0.0, 5.0, 6.0],
                "colour": ["red", "red", None, "red", "blue", "red"],
                "identifier": ["one", "two", "three", "four", "five", "six"],
                "note": ["same"] * 6,
            }
        )

    def test_only_bounded_categorical_fields_are_filter_candidates(self):
        self.assertEqual(categorical_filter_fields(self.data, max_categories=3), ["category", "colour"])

    def test_full_selection_keeps_the_full_dataset(self):
        categories = categorical_values(self.data, "category")
        filtered = filter_categorical_values(self.data, "category", categories)
        self.assertTrue(filtered.equals(self.data))

    def test_one_category_filters_to_matching_rows(self):
        filtered = filter_categorical_values(self.data, "category", ["A"])
        self.assertEqual(len(filtered), 3)
        self.assertTrue(filtered["category"].eq("A").all())

    def test_multiple_categories_use_union_within_the_chosen_field(self):
        filtered = filter_categorical_values(self.data, "category", ["A", "C"])
        self.assertEqual(len(filtered), 4)
        self.assertEqual(filtered["category"].tolist(), ["A", "A", "A", "C"])

    def test_empty_selection_is_an_empty_population(self):
        filtered = filter_categorical_values(self.data, "category", [])
        self.assertTrue(filtered.empty)

    def test_chart_samples_are_calculated_from_the_filtered_population(self):
        filtered = filter_categorical_values(self.data, "category", ["A"])

        one_variable = scale_sample(filtered, ["x"], log_x_field="x")
        two_variables = scale_sample(filtered, ["x", "y"], log_x_field="x")
        three_variables = scale_sample(filtered, ["x", "y", "colour"], log_x_field="x")

        self.assertEqual(one_variable.total, 3)
        self.assertEqual(one_variable.missing, 1)
        self.assertEqual(one_variable.log_excluded, 1)
        self.assertEqual(two_variables.missing, 1)
        self.assertEqual(two_variables.log_excluded, 1)
        self.assertEqual(three_variables.missing, 1)
        self.assertEqual(three_variables.log_excluded, 1)
        self.assertEqual(len(filtered), 3)  # Dataset preview receives this same subset.


if __name__ == "__main__":
    unittest.main()
