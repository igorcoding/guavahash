import json
import os

import guavahash
import pytest


def load_test_cases():
    """Load test cases for parametrize decorator."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "testdata.json")) as f:
        return json.load(f)


class TestGuavaHash:
    """Test suite for guava consistent hashing."""

    @pytest.mark.parametrize("state,buckets,expected", load_test_cases())
    def test_all_cases(self, state, buckets, expected):
        """Test all guava hash cases from testdata.json."""
        result = guavahash.guava(state, buckets)
        assert result == expected, (
            f"guava({state}, {buckets}) = {result}, expected {expected}"
        )

    @pytest.mark.parametrize("state", [1, 2, -19])
    def test_negative_buckets_edge_case(self, state):
        """Test behavior with negative bucket count."""
        assert guavahash.guava(state, -1) == 0

    @pytest.mark.parametrize("state", [1, 2, 3, 34, -19, -199999999, 0, 1000000])
    def test_single_bucket_always_zero(self, state):
        """Test that single bucket always returns 0."""
        assert guavahash.guava(state, 1) == 0

    @pytest.mark.parametrize(
        "state,buckets",
        [(1, 10), (2, 50), (3, 100), (34, 1000), (-19, 25), (-199999999, 500)],
    )
    def test_result_within_bucket_range(self, state, buckets):
        """Test that results are always within valid bucket range."""
        result = guavahash.guava(state, buckets)
        assert 0 <= result < buckets, (
            f"Result {result} not in range [0, {buckets}) for state {state}"
        )
