"""Basic tests for assignment 2.

"""
import gc  # Garbage collection
import os
import psutil

import numpy as np

import pytest

from phys_581_2021 import assignment_2


def fun(t, y):
    """Return dy_dt for a gaussian."""
    return -t * y


def get_y_exact(t, y0):
    """Exact solution."""
    y0, t = map(np.asarray, (y0, t))
    return y0 * np.exp(-(t ** 2) / 2)


class TestABM:
    """Tests for the abm solver.

    Uses a gaussian as a test function.
    """

    def test1(self):
        """Simple test of a gaussian."""

        y0 = [1.0]
        t0 = 0.0
        T = 1.0
        Nt = 500

        res = assignment_2.solve_ivp_abm(fun, t_span=(t0, T), y0=y0, Nt=Nt)
        assert np.allclose(res.y, get_y_exact(res.t, y0=y0))

    def test_mem(self):
        """Test memory usage.

        The strategy here is to use a large system with 2MB/state.  This should be
        large enough that we can trace individual allocations of arrays without noticing
        incidental allocations.

        This is somewhat tricky to do since garbage collection is not guaranteed.  Our
        main point is to ensure that the memory usage is bounded if `save_memory=True`.
        """
        _proc = psutil.Process(os.getpid())
        _mem0 = _proc.memory_info().rss
        MB_per_state = 2

        def num_arrays():
            return np.round(
                (_proc.memory_info().rss - _mem0) / 1024 ** 2 / MB_per_state, 0
            )

        dtype = np.dtype(float)
        bytes_per_float = dtype.itemsize
        N = MB_per_state * 1024 ** 2 / bytes_per_float

        # Check that memory testing is working
        assert num_arrays() == 0
        y0 = np.arange(N, dtype=dtype)
        assert num_arrays() == 1

        Nt = 40
        t0 = 0.0
        T = 1.0

        # Pre-populate arrays with exact solution
        dt = (T - t0) / Nt
        ts = t0 + np.arange(4) * dt
        ys = [get_y_exact(t=_t, y0=y0) for _t in ts]
        dys = [fun(t=_t, y=_y) for _t, _y in zip(ts, ys)]
        dcp = 0 * ys[-1]

        assert num_arrays() == 10

        res = assignment_2.solve_ivp_abm(
            fun, t_span=(t0, T), y0=y0, Nt=Nt, save_memory=True, ys=ys, dys=dys, dcp=dcp
        )

        # Intermediate arrays get stored... often garbage collection does not happen
        # until later.  This number may be smaller if the arrays are bigger.
        assert num_arrays() <= 33

        assert np.allclose(res.y, get_y_exact(res.t, y0[:, np.newaxis]))


class TestEuler:
    def test1(self):
        """Simple test of a gaussian."""

        y0 = [1.0]
        t0 = 0.0
        T = 1.0
        Nt = 500

        res = assignment_2.solve_ivp_euler(fun, t_span=(t0, T), y0=y0, Nt=Nt)
        assert np.allclose(res.y, get_y_exact(res.t, y0=y0), rtol=1e-3)
