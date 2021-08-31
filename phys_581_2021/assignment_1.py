"""Assignment 1
"""
import math

import numpy as np


def play_monty_hall(switch=False):
    """Return `True` if the contestant wins one round of Monty Hall.

    Arguments
    ---------
    switch : bool
       If `True`, then switch doors, otherwise stick with the original door.
    """

    # Use np.random to simulate a game
    win = True  # Stub
    return win


def lambertw(z, k=-1):
    r"""Return `x` from the k'th branch of the LambertW function.

    $$
      z = we^w, \qquad
      w = W_k(z).
    $$

    Arguments
    ---------
    z : float, array_like
        Argument.  You can assume that `z >= -exp(-1)` and that `z <= 0` if `k == -1`.
        Raise `ValueError` otherwise (unless your code correctly extends W(z)
        to the complex plane).
    k : [0, -1]
        Branch.  If `k == 0`, then return the solution $w>-1$, otherwise if `k == -1`,
        return the solution $w < -1$

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

    # Compute W(z)
    w = 0 * z  # Stub
    return w
