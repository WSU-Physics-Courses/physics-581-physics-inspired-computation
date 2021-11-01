"""Basic tests for assignment 4.

"""
import gc  # Garbage collection
import os
import psutil

import numpy as np

import pytest

from phys_581_2021 import assignment_4


class TestLyapunov:
    """Tests for `compute_lyapunov`.

    We use the Lorenz system to test.
    """

    min_norm = 1e-7

    args = dict(
        y0=(1.0, 1.0, 1.0),
        t0=0.0,
        dt=10.0,
        min_norm=min_norm,
        norm=np.linalg.norm,
        Nsamples=10,
        debug=True,
        solve_ivp_args=dict(atol=1e-3, rtol=1e-3),
    )

    @classmethod
    def setup_class(cls):
        # To get a good initial state and dy, we evolve a few times
        args = dict(cls.args, dt=10.0, Nsamples=3)
        lams, ts, ys, dys = assignment_4.compute_lyapunov(cls.compute_dy_dt, **args)
        cls.args["y0"] = ys[-1][:, -1]
        cls.args["dy0"] = dys[-1][:, -1]
        cls.args["compute_dy_dt"] = cls.compute_dy_dt

    @staticmethod  # This just means that the method does not depend on self.
    def compute_dy_dt(t, q):
        sigma = 10.0
        beta = 8.0 / 3
        rho = 28.0

        x, y, z = q
        return (sigma * (y - x), x * (rho - z) - y, x * y - beta * z)

    def test_min_norm(cls):
        """Check that dy's are normalized properly."""
        lams, ts, ys, dys = assignment_4.compute_lyapunov(**cls.args)

        # Get the norms of the first dy0s
        norms = [np.linalg.norm(_dy[:, 0]) for _dy in dys]
        assert np.allclose(norms, cls.min_norm)

    def test_lorenz(cls):
        """Check that the code correctly calculates the exponent."""
        args = dict(cls.args)
        args.pop("solve_ivp_args")  # To cover case of empty args.
        args.pop("debug")
        args["Nsamples"] = 10
        args["dt"] = 10.0
        lams = np.array(assignment_4.compute_lyapunov(**args))
        assert np.allclose(lams.mean(), 0.86, atol=lams.std())
        assert lams.std() < 0.2

    def test_coverage(cls):
        """"Coverage test for NotImplementedError exceptions.

        Please disable once you implement these.
        """
        with pytest.raises(NotImplementedError):
            assignment_4.compute_lyapunov(cls.compute_dy_dt, y0=(1.0, 1.0, 1.0))
