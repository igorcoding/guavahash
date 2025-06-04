import guavahash
import pytest


class TestGuavaHashEdgeCases:
    """Edge case tests for potential differences between C and Rust implementations."""

    @pytest.mark.parametrize(
        "state,buckets",
        [
            (9223372036854775807, 100),  # INT64_MAX
            (-9223372036854775808, 100),  # INT64_MIN
            (9223372036854775806, 50),  # INT64_MAX - 1
            (-9223372036854775807, 50),  # INT64_MIN + 1
            (9223372036854775805, 25),  # INT64_MAX - 2
            (-9223372036854775806, 25),  # INT64_MIN + 2
        ],
    )
    def test_extreme_int64_values(self, state, buckets):
        """Test behavior with extreme 64-bit integer values."""
        result = guavahash.guava(state, buckets)
        assert isinstance(result, int), f"Result should be int, got {type(result)}"
        assert 0 <= result < buckets, (
            f"Result {result} not in range [0, {buckets}) for extreme state {state}"
        )

    @pytest.mark.parametrize(
        "state,buckets",
        [
            (-4611686018427387904, 100),  # INT64_MIN/2
            (-2305843009213693952, 100),  # INT64_MIN/4
            (-1152921504606846976, 100),  # INT64_MIN/8
            (-576460752303423488, 100),  # INT64_MIN/16
            (-288230376151711744, 100),  # INT64_MIN/32
            (-144115188075855872, 50),  # INT64_MIN/64
            (-72057594037927936, 50),  # INT64_MIN/128
            (-36028797018963968, 25),  # INT64_MIN/256
        ],
    )
    def test_negative_bit_shift_edge_cases(self, state, buckets):
        """Test negative numbers that affect bit shifting behavior."""
        result = guavahash.guava(state, buckets)
        assert isinstance(result, int), f"Result should be int, got {type(result)}"
        assert 0 <= result < buckets, (
            f"Result {result} not in range [0, {buckets}) for negative state {state}"
        )

    @pytest.mark.parametrize(
        "state,buckets",
        [
            (2147483647, 100),  # INT32_MAX
            (-2147483648, 100),  # INT32_MIN
            (4294967295, 100),  # UINT32_MAX
            (8589934591, 100),  # 2^33 - 1 (affects state >> 33)
            (8589934592, 100),  # 2^33
            (17179869183, 100),  # 2^34 - 1
            (17179869184, 100),  # 2^34
            (34359738367, 100),  # 2^35 - 1
            (68719476735, 100),  # 2^36 - 1
        ],
    )
    def test_type_casting_boundaries(self, state, buckets):
        """Test values at type casting boundaries."""
        result = guavahash.guava(state, buckets)
        assert isinstance(result, int), f"Result should be int, got {type(result)}"
        assert 0 <= result < buckets, (
            f"Result {result} not in range [0, {buckets}) for boundary state {state}"
        )

    @pytest.mark.parametrize(
        "state,buckets",
        [
            (9223372036854775806, 10000),  # Forces multiple iterations with overflow
            (
                -9223372036854775807,
                10000,
            ),  # Forces multiple iterations with negative overflow
            (9223372036854775805, 5000),  # INT64_MAX - 2, large bucket count
            (-9223372036854775806, 5000),  # INT64_MIN + 2, large bucket count
            (4611686018427387903, 10000),  # INT64_MAX/2, large bucket count
            (-4611686018427387904, 10000),  # INT64_MIN/2, large bucket count
        ],
    )
    def test_multiple_iterations_with_overflow(self, state, buckets):
        """Test values that require multiple iterations and may trigger overflow."""
        result = guavahash.guava(state, buckets)
        assert isinstance(result, int), f"Result should be int, got {type(result)}"
        assert 0 <= result < buckets, (
            f"Result {result} not in range [0, {buckets}) for overflow-prone state {state}"
        )

    @pytest.mark.parametrize(
        "state,buckets",
        [
            (-9223372036854775808, 2),  # INT64_MIN
            (-9223372036854775808, 10),
            (-9223372036854775808, 100),
            (-9223372036854775808, 1000),
            (-4611686018427387904, 2),  # INT64_MIN/2
            (-4611686018427387904, 10),
            (-4611686018427387904, 100),
            (-4611686018427387904, 1000),
            (-2305843009213693952, 2),  # INT64_MIN/4
            (-2305843009213693952, 10),
            (-2305843009213693952, 100),
            (-2305843009213693952, 1000),
            (-1, 2),  # Simple negative
            (-1, 10),
            (-1, 100),
            (-1, 1000),
            (-100, 2),  # Small negative
            (-100, 10),
            (-100, 100),
            (-100, 1000),
            (-2147483648, 2),  # INT32_MIN
            (-2147483648, 10),
            (-2147483648, 100),
            (-2147483648, 1000),
            (-9223372036854775807, 2),  # INT64_MIN + 1
            (-9223372036854775807, 10),
            (-9223372036854775807, 100),
            (-9223372036854775807, 1000),
        ],
    )
    def test_negative_states_various_buckets(self, state, buckets):
        """Test negative state values with various bucket counts."""
        result = guavahash.guava(state, buckets)
        assert isinstance(result, int), f"Result should be int, got {type(result)}"
        assert 0 <= result < buckets, (
            f"Result {result} not in range [0, {buckets}) for negative state {state}"
        )

    @pytest.mark.parametrize(
        "state,buckets",
        [
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (0, 10),
            (0, 100),
            (0, 1000),
            (0, 10000),  # Zero
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (1, 10),
            (1, 100),
            (1, 1000),
            (1, 10000),  # Positive one
            (-1, 1),
            (-1, 2),
            (-1, 3),
            (-1, 4),
            (-1, 5),
            (-1, 10),
            (-1, 100),
            (-1, 1000),
            (-1, 10000),  # Negative one
            (2862933555777941757, 1),
            (2862933555777941757, 2),
            (2862933555777941757, 3),
            (2862933555777941757, 4),
            (2862933555777941757, 5),
            (2862933555777941757, 10),
            (2862933555777941757, 100),
            (2862933555777941757, 1000),
            (2862933555777941757, 10000),  # K constant value
            (-2862933555777941757, 1),
            (-2862933555777941757, 2),
            (-2862933555777941757, 3),
            (-2862933555777941757, 4),
            (-2862933555777941757, 5),
            (-2862933555777941757, 10),
            (-2862933555777941757, 100),
            (-2862933555777941757, 1000),
            (-2862933555777941757, 10000),  # Negative K
            (9223372036854775807, 1),
            (9223372036854775807, 2),
            (9223372036854775807, 3),
            (9223372036854775807, 4),
            (9223372036854775807, 5),
            (9223372036854775807, 10),
            (9223372036854775807, 100),
            (9223372036854775807, 1000),
            (9223372036854775807, 10000),  # INT64_MAX
            (-9223372036854775808, 1),
            (-9223372036854775808, 2),
            (-9223372036854775808, 3),
            (-9223372036854775808, 4),
            (-9223372036854775808, 5),
            (-9223372036854775808, 10),
            (-9223372036854775808, 100),
            (-9223372036854775808, 1000),
            (-9223372036854775808, 10000),  # INT64_MIN
        ],
    )
    def test_edge_states_with_various_buckets(self, state, buckets):
        """Test edge case states with different bucket counts."""
        result = guavahash.guava(state, buckets)
        assert isinstance(result, int), f"Result should be int, got {type(result)}"
        assert 0 <= result < buckets, (
            f"Result {result} not in range [0, {buckets}) for edge state {state}, buckets {buckets}"
        )

    def test_overflow_sequence_consistency(self):
        """Test that overflow sequences are consistent."""
        # Start with a value that will overflow in the first iteration
        state = 9223372036854775806  # INT64_MAX - 1
        buckets = 1000

        # Run multiple times to ensure consistent behavior
        results = []
        for _ in range(5):
            result = guavahash.guava(state, buckets)
            results.append(result)

        # All results should be identical
        assert all(r == results[0] for r in results), (
            f"Inconsistent results for overflow case: {results}"
        )
        assert 0 <= results[0] < buckets

    @pytest.mark.parametrize(
        "state,buckets",
        [
            (1, 2147483647),
            (-1, 2147483647),
            (42, 2147483647),
            (-42, 2147483647),
            (1000000, 2147483647),
            (-1000000, 2147483647),  # INT32_MAX buckets
            (1, 1000000000),
            (-1, 1000000000),
            (42, 1000000000),
            (-42, 1000000000),
            (1000000, 1000000000),
            (-1000000, 1000000000),  # 1 billion buckets
            (1, 100000000),
            (-1, 100000000),
            (42, 100000000),
            (-42, 100000000),
            (1000000, 100000000),
            (-1000000, 100000000),  # 100 million buckets
        ],
    )
    def test_large_bucket_counts(self, state, buckets):
        """Test with large bucket counts that might expose precision issues."""
        result = guavahash.guava(state, buckets)
        assert isinstance(result, int), f"Result should be int, got {type(result)}"
        assert 0 <= result < buckets, (
            f"Result {result} not in range [0, {buckets}) for state {state}, large buckets {buckets}"
        )

    @pytest.mark.parametrize(
        "state,buckets",
        [
            # Test values that could cause precision issues in floating point calculations
            (1, 1073741824),  # 2^30 buckets
            (-1, 1073741824),  # Negative state, 2^30 buckets
            (2862933555777941757, 2147483647),  # K value with INT32_MAX buckets
            (-2862933555777941757, 2147483647),  # -K value with INT32_MAX buckets
        ],
    )
    def test_floating_point_precision_edge_cases(self, state, buckets):
        """Test cases that might expose floating point precision differences."""
        result = guavahash.guava(state, buckets)
        assert isinstance(result, int), f"Result should be int, got {type(result)}"
        assert 0 <= result < buckets, (
            f"Result {result} not in range [0, {buckets}) for precision test state {state}"
        )

    @pytest.mark.parametrize(
        "state,buckets",
        [
            # Generate test cases for systematic boundary exploration
            # Base values: -2^i for i in range(32, 63)
            (-4294967296, 10),
            (-4294967296, 100),
            (-4294967296, 1000),  # -2^32
            (-8589934592, 10),
            (-8589934592, 100),
            (-8589934592, 1000),  # -2^33
            (-17179869184, 10),
            (-17179869184, 100),
            (-17179869184, 1000),  # -2^34
            (-34359738368, 10),
            (-34359738368, 100),
            (-34359738368, 1000),  # -2^35
            (-68719476736, 10),
            (-68719476736, 100),
            (-68719476736, 1000),  # -2^36
            (-137438953472, 10),
            (-137438953472, 100),
            (-137438953472, 1000),  # -2^37
            (-274877906944, 10),
            (-274877906944, 100),
            (-274877906944, 1000),  # -2^38
            (-549755813888, 10),
            (-549755813888, 100),
            (-549755813888, 1000),  # -2^39
            (-1099511627776, 10),
            (-1099511627776, 100),
            (-1099511627776, 1000),  # -2^40
            (-2199023255552, 10),
            (-2199023255552, 100),
            (-2199023255552, 1000),  # -2^41
            (-4398046511104, 10),
            (-4398046511104, 100),
            (-4398046511104, 1000),  # -2^42
            (-8796093022208, 10),
            (-8796093022208, 100),
            (-8796093022208, 1000),  # -2^43
            (-17592186044416, 10),
            (-17592186044416, 100),
            (-17592186044416, 1000),  # -2^44
            (-35184372088832, 10),
            (-35184372088832, 100),
            (-35184372088832, 1000),  # -2^45
            (-70368744177664, 10),
            (-70368744177664, 100),
            (-70368744177664, 1000),  # -2^46
            (-140737488355328, 10),
            (-140737488355328, 100),
            (-140737488355328, 1000),  # -2^47
            (-281474976710656, 10),
            (-281474976710656, 100),
            (-281474976710656, 1000),  # -2^48
            (-562949953421312, 10),
            (-562949953421312, 100),
            (-562949953421312, 1000),  # -2^49
            (-1125899906842624, 10),
            (-1125899906842624, 100),
            (-1125899906842624, 1000),  # -2^50
            (-2251799813685248, 10),
            (-2251799813685248, 100),
            (-2251799813685248, 1000),  # -2^51
            (-4503599627370496, 10),
            (-4503599627370496, 100),
            (-4503599627370496, 1000),  # -2^52
            (-9007199254740992, 10),
            (-9007199254740992, 100),
            (-9007199254740992, 1000),  # -2^53
            (-18014398509481984, 10),
            (-18014398509481984, 100),
            (-18014398509481984, 1000),  # -2^54
            (-36028797018963968, 10),
            (-36028797018963968, 100),
            (-36028797018963968, 1000),  # -2^55
            (-72057594037927936, 10),
            (-72057594037927936, 100),
            (-72057594037927936, 1000),  # -2^56
            (-144115188075855872, 10),
            (-144115188075855872, 100),
            (-144115188075855872, 1000),  # -2^57
            (-288230376151711744, 10),
            (-288230376151711744, 100),
            (-288230376151711744, 1000),  # -2^58
            (-576460752303423488, 10),
            (-576460752303423488, 100),
            (-576460752303423488, 1000),  # -2^59
            (-1152921504606846976, 10),
            (-1152921504606846976, 100),
            (-1152921504606846976, 1000),  # -2^60
            (-2305843009213693952, 10),
            (-2305843009213693952, 100),
            (-2305843009213693952, 1000),  # -2^61
            (-4611686018427387904, 10),
            (-4611686018427387904, 100),
            (-4611686018427387904, 1000),  # -2^62
            # Boundary values (±1 from base values) - only including those within i64 range
            (-4294967295, 10),
            (-4294967295, 100),
            (-4294967295, 1000),  # -2^32 + 1
            (-4294967297, 10),
            (-4294967297, 100),
            (-4294967297, 1000),  # -2^32 - 1
            (-8589934591, 10),
            (-8589934591, 100),
            (-8589934591, 1000),  # -2^33 + 1
            (-8589934593, 10),
            (-8589934593, 100),
            (-8589934593, 1000),  # -2^33 - 1
        ],
    )
    def test_systematic_negative_boundary_exploration(self, state, buckets):
        """Systematically test negative values around critical boundaries."""
        result = guavahash.guava(state, buckets)
        assert isinstance(result, int), f"Result should be int, got {type(result)}"
        assert 0 <= result < buckets, (
            f"Result {result} not in range [0, {buckets}) for systematic test state {state}"
        )
