"""Official Tests for Assignment 4

These tests are the official tests for assignment 4.  Run with:

```bash
pytest -k test_official_assignment_4 --no-cov
```
"""

import numpy as np

import pytest

from phys_581_2021 import assignment_4


class Lorenz:
    """Lorenz Equations"""

    def __init__(self, sigma=10.0, beta=8.0 / 3, rho=28.0):
        self.sigma = sigma
        self.beta = beta
        self.rho = rho

    def compute_dy_dt(self, t, q):
        """Lorenz equations."""
        x, y, z = q
        return (self.sigma * (y - x), x * (self.rho - z) - y, x * y - self.beta * z)

    # Known solutions from
    # https://ecommons.cornell.edu/bitstream/handle/1813/7351/98-1697.pdf;jsessionid=ADFF736928C5DBB80656C44D97A01754?sequence=1
    known_exponents = [
        (dict(sigma=16, rho=45.92, beta=4), 1.50255),
        (dict(sigma=16, rho=40.0, beta=4), 1.37446),
        (dict(sigma=10, rho=28.0, beta=8.0 / 3.0), 0.90566),
    ]


@pytest.fixture(params=Lorenz.known_exponents)
def sol(request):
    yield request.param


class TestLyapunov:
    def test_lorenz1(self, sol):
        params, max_exp = sol

        ode = Lorenz(**params)
        y0 = (1.0, 1.0, 1.0)
        Nsamples = 100

        res = np.asarray(
            assignment_4.compute_lyapunov(ode.compute_dy_dt, y0=y0, Nsamples=Nsamples)
        )

        assert np.allclose(res.mean(), max_exp, rtol=0.05)
        assert np.allclose(res.mean(), max_exp, rtol=res.std())

    def test_lorenz2(self, sol):
        """Start far from attractor."""
        params, max_exp = sol
        ode = Lorenz(**params)
        y0 = (100.0, 100.0, 100.0)
        Nsamples = 100
        res = np.asarray(
            assignment_4.compute_lyapunov(ode.compute_dy_dt, y0=y0, Nsamples=Nsamples)
        )

        assert np.allclose(res.mean(), max_exp, rtol=0.05)
        assert np.allclose(res.mean(), max_exp, rtol=res.std())
