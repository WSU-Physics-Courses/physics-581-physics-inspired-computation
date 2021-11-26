"""Assignment 1
"""
import math

import numpy as np


def play_monty_hall(switch=False):
    """Return ``True`` if the contestant wins one round of Monty Hall.

    Arguments
    ---------
    switch : bool
       If `True`, then switch doors, otherwise stick with the original door.
    """

    ### To Do: Use np.random to simulate a game
    win = True  # Stub
    return win


def lambertw(z, k=-1):
    r"""Return :math:`w` from the `k`'th branch of the LambertW function.

    .. math::
      z = we^w, \qquad
      w = W_k(z).

    Arguments
    ---------
    z : float, array_like
        Argument.  You can assume that ``z >= -exp(-1)`` and that ``z <= 0`` if
        ``k == -1``.  Raise ``ValueError`` otherwise (unless your code correctly extends
        :math:`W(z)` to the complex plane).
    k : [0, -1]
        Branch.  If ``k == 0``, then return the solution :math:`w>-1`, otherwise if
        ``k == -1``, return the solution :math:`w < -1`

    Notes
    -----
    Do not use a canned implementation, even if you find one in SciPy.  Write your own
    version.
    """
    if k not in set([-1, 0]):
        raise ValueError(f"k must be either 0 or -1 (got {k})")

    z_min = -math.exp(-1)

    if np.any(np.asarray(z) < z_min):
        raise ValueError(f"Invalid z = {z} < {z_min}")

    if k == -1 and np.any(np.asarray(z) > 0):
        raise ValueError(f"Invalid z = {z} > 0 for k == -1.")

    ### To Do: Compute W(z)
    w = 0 * z  # Stub
    return w


def zeta(s):
    r"""Return the Riemann zeta function at `s`.

    .. math::
      \zeta(s) = \sum_{1}^{\infty} \frac{1}{n^{s}}.

    Arguments
    ---------
    s : float
       Argument of the zeta function.
    """
    ### To Do: Compute zeta(s)
    return 1.0 * s  # Stub


def derivative(f, x, d=0):
    """Return the `d`'th derivative of `f(x)` at `x`.

    Arguments
    ---------
    f : function
        The function to take the derivative of.
    x : float
        Where to take the derivative.
    d : int
        Which derivative to take.  `d=0` just evaluates the function.
    """
    if d == 0:
        return f(x)

    fx = f(x)
    eps = np.finfo(np.asarray(fx).dtype).eps

    if d == 1:
        # Estimate the third derivative so we can estimate the optimal step size
        xs = np.linspace(x - 0.01, x + 0.01, 5)
        fs = list(map(f, xs))  #  Don't assume f is vectorized.
        d3fxs = 6 * np.polyfit(xs, fs, deg=3)[0]
        h = (3 * eps * abs(fx) / (abs(d3fxs) + 0.01)) ** (1 / 3)
        x1 = x - h
        x2 = x + h
        return (f(x2) - f(x1)) / (x2 - x1)

    # Recursively compute... this is not a good idea!
    def df(x):
        return derivative(f, x=x, d=1)

    return derivative(df, x=x, d=d - 1)
