# -*- coding: utf-8 -*-
# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)
"""Tests for BaseAligner API points."""

__author__ = ["fkiraly"]

import numpy as np
import pandas as pd

from sktime.datatypes._check import check_raise
from sktime.tests.test_all_estimators import BaseFixtureGenerator, QuickTester
from sktime.utils._testing.series import _make_series

INVALID_X_INPUT_TYPES = [list(), tuple()]
INVALID_y_INPUT_TYPES = [list(), tuple()]


class AlignerFixtureGenerator(BaseFixtureGenerator):
    """Fixture generator for classifier tests.

    Fixtures parameterized
    ----------------------
    estimator_class: estimator inheriting from BaseObject
        ranges over estimator classes not excluded by EXCLUDE_ESTIMATORS, EXCLUDED_TESTS
    estimator_instance: instance of estimator inheriting from BaseObject
        ranges over estimator classes not excluded by EXCLUDE_ESTIMATORS, EXCLUDED_TESTS
        instances are generated by create_test_instance class method
    scenario: instance of TestScenario
        ranges over all scenarios returned by retrieve_scenarios
    """

    # note: this should be separate from TestAllAligners
    #   additional fixtures, parameters, etc should be added here
    #   TestAllAligners should contain the tests only

    estimator_type_filter = "aligner"


class TestAllAligners(AlignerFixtureGenerator, QuickTester):
    """Module level tests for all sktime aligners."""

    def test_get_alignment(self, estimator_instance):
        """Test that get_alignment returns an alignment (iloc)."""
        X = [_make_series(n_columns=2), _make_series(n_columns=2)]
        align = estimator_instance.fit(X).get_alignment()

        check_raise(align, mtype="alignment", scitype="Alignment")

        # todo: replace this by scenarios
        if estimator_instance.get_tag("capability:multivariate"):
            Xm = [_make_series(n_columns=2) for _ in range(3)]
            alignm = estimator_instance.fit(Xm).get_alignment()
            check_raise(alignm, mtype="alignment", scitype="Alignment")

    def test_get_alignment_loc(self, estimator_instance):
        """Test that get_alignment returns an alignment (loc)."""
        X = [_make_series(n_columns=2), _make_series(n_columns=2)]
        align = estimator_instance.fit(X).get_alignment_loc()

        check_raise(align, mtype="alignment_loc", scitype="Alignment")

    def test_get_alignment_loc(self, estimator_instance):
        """Test that get_alignment returns an alignment (loc)."""
        X = [_make_series(n_columns=2), _make_series(n_columns=2)]
        n = len(X)
        X_aligned = estimator_instance.fit(X).get_aligned()

        cls_name = type(estimator_instance.__name__)

        msg = f"{cls_name}.get_aligned must return list of pd.DataFrame"
        msg += ", same length as X in fit"
        col_msg = f"{cls_name}.get_aligned series must have same columns as in X"
        assert isinstance(X_aligned, list), msg
        assert len(X_aligned) == n, msg

        for i in range(n):
            Xi = X_aligned[i]
            assert isinstance(Xi, pd.DataFrame), msg
            assert set(Xi.columns) == set(X[i].columns), col_msg

    def test_get_distance(self, estimator_instance):
        """Test that get_distance returns an scalar."""
        if not estimator_instance.get_tag("capability:distance"):
            return None

        X = [_make_series(n_columns=2), _make_series(n_columns=2)]
        dist = estimator_instance.fit(X).get_distance()
        assert isinstance(dist, float)

    def test_get_distance_matrix(self, estimator_instance):
        """Test that get_distance_matrix returns an scalar."""
        if not estimator_instance.get_tag("capability:distance-matrix"):
            return None

        X = [_make_series(n_columns=2), _make_series(n_columns=2)]
        dist = estimator_instance.fit(X).get_distance()
        assert isinstance(dist, np.ndarray)
        assert dist.shape == (2, 2)
