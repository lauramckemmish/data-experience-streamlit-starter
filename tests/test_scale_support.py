"""Focused tests for the Data Playground's shared scale handling."""

import unittest

import pandas as pd

from charts import histogram, scatter
from data import scale_sample


class ScaleSampleTests(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame(
            {
                "x": [1.0, 0.0, -2.0, 4.0, None, 6.0],
                "y": [2.0, 3.0, 0.0, -1.0, 5.0, None],
                "group": ["a", "a", "b", "b", "a", "b"],
            }
        )

    def test_linear_sample_keeps_complete_rows(self):
        sample = scale_sample(self.data, ["x", "y"])
        self.assertEqual(len(sample.data), 4)
        self.assertEqual(sample.missing, 2)
        self.assertEqual(sample.log_excluded, 0)

    def test_log_x_excludes_only_non_positive_x_values(self):
        sample = scale_sample(self.data, ["x", "y"], log_x_field="x")
        self.assertEqual(len(sample.data), 2)
        self.assertEqual(sample.missing, 2)
        self.assertEqual(sample.log_x_excluded, 2)
        self.assertEqual(sample.log_y_excluded, 0)
        self.assertEqual(sample.log_excluded, 2)

    def test_log_y_excludes_only_non_positive_y_values(self):
        sample = scale_sample(self.data, ["x", "y"], log_y_field="y")
        self.assertEqual(len(sample.data), 2)
        self.assertEqual(sample.missing, 2)
        self.assertEqual(sample.log_x_excluded, 0)
        self.assertEqual(sample.log_y_excluded, 2)
        self.assertEqual(sample.log_excluded, 2)

    def test_log_log_reports_axis_reasons_and_union(self):
        sample = scale_sample(self.data, ["x", "y"], log_x_field="x", log_y_field="y")
        self.assertEqual(len(sample.data), 1)
        self.assertEqual(sample.missing, 2)
        self.assertEqual(sample.log_x_excluded, 2)
        self.assertEqual(sample.log_y_excluded, 2)
        self.assertEqual(sample.log_excluded, 3)

    def test_three_variable_missingness_is_separate_from_log_exclusions(self):
        sample = scale_sample(self.data, ["x", "y", "group"], log_x_field="x", log_y_field="y")
        self.assertEqual(sample.missing, 2)
        self.assertEqual(sample.log_excluded, 3)
        self.assertEqual(len(sample.data), 1)


class ChartScaleTests(unittest.TestCase):
    def test_histogram_defaults_to_linear_and_can_use_log_x(self):
        data = pd.DataFrame({"x": [1, 10, 100]})
        self.assertNotEqual(histogram(data, "x").layout.xaxis.type, "log")
        self.assertEqual(histogram(data, "x", log_x=True).layout.xaxis.type, "log")

    def test_scatter_supports_each_axis_combination(self):
        data = pd.DataFrame({"x": [1, 10], "y": [2, 20]})
        for log_x, log_y in ((False, False), (True, False), (False, True), (True, True)):
            figure = scatter(data, "x", "y", log_x=log_x, log_y=log_y)
            self.assertEqual(figure.layout.xaxis.type == "log", log_x)
            self.assertEqual(figure.layout.yaxis.type == "log", log_y)
