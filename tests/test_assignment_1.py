"""Basic Tests for Assignment 1.
"""
import numpy as np

import pytest

from phys_581_2021 import assignment_1


def test_monty_hall_basic():
    """Basic tests that the function runs."""
    assert assignment_1.play_monty_hall(switch=False) in set([True, False])
    assert assignment_1.play_monty_hall(switch=True) in set([True, False])


class TestLambertW:
    def test_lambertw_basic(self):
        """Make sure code works with arrays."""
        x = np.linspace(-0.1, 0, 10)
        assert len(assignment_1.lambertw(x, k=-1)) == len(x)
        assert len(assignment_1.lambertw(x, k=0)) == len(x)

    def test_invalid(self):
        """Test invalid values."""

        with pytest.raises(ValueError, match="k must be either 0 or -1 (got 1)"):
            assignment_1.lambertw(0.1, k=1)

        with pytest.raises(ValueError, match="Invalid z = -0.5 < {z_min}"):
            assignment_1.lambertw(-0.5, k=0)

        with pytest.raises(ValueError, match="Invalid z = -10 < {z_min}"):
            assignment_1.lambertw(-10, k=-1)
