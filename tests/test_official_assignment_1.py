"""Official Tests for Assignment 1

These tests are the official tests for assignment 1.  Run with:

```bash
pytest -k test_official_assignment_1 --no-cov
```
"""

import numpy as np

import pytest

from phys_581_2021 import assignment_1


class TestMontyHall:
    def test_monty_hall(self, seed=2021 + 1):
        play_monty_hall = assignment_1.play_monty_hall
        N = 10000
        np.random.seed(seed)
        switches = np.array([play_monty_hall(switch=True) for n in range(N)])
        np.random.seed(seed)
        sticks = np.array([play_monty_hall(switch=False) for n in range(N)])
        assert np.allclose(sticks.mean(), 1 / 3, atol=0.01)
        assert np.allclose(switches.mean(), 2 / 3, atol=0.01)

        # Since we reseed the random numbers, the results should be complementary
        assert np.allclose(1, sticks + switches)


def test_lambertw():
    z_min = -np.exp(-1)

    for k, z_max in ((-1, 0), (0, 10)):
        zs = np.linspace(z_min, z_max, 100)[1:-1]
        ws = assignment_1.lambertw(zs, k=k)
        assert np.allclose(ws * np.exp(ws), zs)


def test_zeta():
    """Basic test of zeta function to make sure it works with arrays."""
    vals = [(100.0, 1.0),
            (10.0, 1.0009945751278180854),
            (3.0, 1.2020569031595942854),
            (2.0, 1.6449340668482264365)]

    for s, exact in vals:
        assert np.allclose(assignment_1.zeta(s), exact)


def test_zeta_hard():
    """Hard test of zeta function to make sure it works with arrays."""
    vals = [(1.5, 2.6123753486854883433),
            (1.1, 10.584448464950809826),
            (1.01, 100.57794333849687249)]
    
    for s, exact in vals:
        assert np.allclose(assignment_1.zeta(s), exact)
        

def test_derivative():
    """Test the derivative code."""

    xs = [0, 1.0, 10.0]
    rtol = 1e-12
    f = np.sin
    for x in xs:
        dfx = np.cos(x)
        ddfx = -np.sin(x)
        dddfx = -np.cos(x)
        assert np.allclose(assignment_1.derivative(f, x=x, d=0), f(x), rtol=rtol)
        assert np.allclose(assignment_1.derivative(f, x=x, d=1), dfx, rtol=rtol)
        assert np.allclose(assignment_1.derivative(f, x=x, d=2), ddfx, rtol=rtol)
        assert np.allclose(assignment_1.derivative(f, x=x, d=3), dddfx, rtol=rtol)
