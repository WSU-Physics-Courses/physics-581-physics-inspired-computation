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
