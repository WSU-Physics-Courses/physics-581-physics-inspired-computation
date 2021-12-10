"""Official Tests for Assignment 2

These tests are the official tests for assignment 2.  Run with:

```bash
pytest -k test_official_assignment_2 --no-cov
```
"""

import numpy as np

import pytest

from phys_581_2021 import assignment_2


class ODE1:
    """Gaussian."""

    def dy_dt(self, t, y):
        return -t * y

    def y(self, t, y0):
        """Exact solution."""
        y0, t = map(np.asarray, (y0, t))
        return y0 * np.exp(-(t ** 2) / 2)


class TestSolveIVP:
    def test1(self):
        """Simple test of a gaussian."""

        ode = ODE1()

        y0 = [1.0]
        t0 = 0.0
        T = 1.0
        Nt = 500

        res = assignment_2.solve_ivp_rk4(ode.dy_dt, t_span=(t0, T), y0=y0, Nt=Nt)
        assert np.allclose(res.y, ode.y(res.t, y0=y0))

    def test_scaling(self):
        """Scaling of error."""
        ode = ODE1()

        y0 = [1.0]
        t0 = 0.0
        T = 1.0

        Nts = 2 ** (np.arange(3, 11))
        errs = []
        for Nt in Nts:
            res = assignment_2.solve_ivp_rk4(ode.dy_dt, t_span=(t0, T), y0=y0, Nt=Nt)
            err = abs(res.y[0, -1] - ode.y(T, y0=y0)[0])
            errs.append(err)

        hs = T / Nts
        p, loga = np.polyfit(np.log(hs), np.log(errs), deg=1)
        a = np.exp(loga)
        assert np.allclose(p, 4, rtol=0.01)
        assert a < 1e-3
