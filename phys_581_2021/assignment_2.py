"""Assignment 2
"""
import math

import numpy as np

from scipy.optimize import OptimizeResult


class OdeResult(OptimizeResult):
    """Bunch object for storing results of solve_ivp* methods."""

    def ___init__(self, t, y, **kw):
        self.t = t
        self.y = y
        self.__dict__.update(kw)


def solve_ivp_abm(
    fun, t_span, y0, Nt, ys=None, dys=None, dcp=None, save_memory=False, start_factor=2
):
    """Solve the specified IVP using a 5th order predictor-corrector method.

    This is the algorithm presented at the end of Section 23.10 of Hamming's book.  It
    is an average of the Milne and Adams-Bashforth cases.

    Arguments
    ---------
    Nt : int
        Number of steps.  The time-step will be `np.diff(t_span)/Nt`.
    ys : [y3, y2, y1, y0] or None
        Previous four steps to get the process started.  If not provided, then these
        will be computed using `solve_ivp_rk4`.
    dys : [dy3, dy2, dy1, dy0] or None
        Derivatives at the corresponding previous steps.  Will be computed if not
        provided.
    dcp : array, None
        Previous corrector-predictor difference (with factor pf 161/170).
    save_memory : bool
        If `True`, then only keep the last four steps.

    Returns
    -------
    res : OdeResult
       Bunch object.

    The remaining arguments should match those of `scipy.integrate.solve_ivp`.  Don't
    worry about optimizations like allowing `fun` to be `vectorized` etc.

    Notes
    -----
    This method requires four initial values to get started.
    """
    t0, t1 = t_span
    dt = (t1 - t0) / Nt

    if ys is None:
        # No initial steps provided.  Use solve_ivp_rk4
        res0 = solve_ivp_rk4(fun=fun, t_span=(0, 4 * dt), y0=y0, Nt=4 * start_factor)

        # Keep only Nt previous values... allows code to work if Nt < 4.
        ys = res0.y.T[::start_factor][:Nt]

    # Compute corresponding ts.
    ts = t0 + np.arange(len(ys)) * dt

    if dys is None:
        dys = [fun(_t, _y) for (_t, _y) in zip(ts, ys)]

    # Convert ts, ys, and dys to lists so we can append etc.
    ts, ys, dys = (list(np.asarray(_x)) for _x in (ts, ys, dys))

    if dcp is None:
        # If not provided, assume it is zero.
        dcp = 0

    while len(ys) < Nt:
        # While look allows this code to work if Nt < 4
        t = ts[-1]

        # We do a little indexing trick here with n, so that y[n-i] is the same as
        # y_{n-i} in the formula.  y[n] = y[-1] is the current step.
        n = -1
        y = ys
        dy = dys

        # New predictor
        p_new = (y[n] + y[n - 1]) / 2 + dt / 48 * (
            119 * dy[n] - 99 * dy[n - 1] + 69 * dy[n - 2] - 17 * dy[n - 3]
        )

        # Compute "midpoint" and its derivative
        t_new = t + dt
        m_new = p_new + dcp
        dm_new = np.asarray(fun(t_new, m_new))

        # Compute new predictor-corrector difference
        dcp = (dt / 48 * 161 / 170) * (
            17 * dm_new - 68 * dy[n] + 102 * dy[n - 1] - 68 * dy[n - 2] + 17 * dy[n - 3]
        )

        # Finally, compute the new step and it's derivative
        y_new = p_new + dcp
        dy_new = np.asarray(fun(t_new, y_new))

        ts.append(t_new)
        ys.append(y_new)
        dys.append(dy_new)

        if save_memory:
            ts.pop(0)
            ys.pop(0)
            dys.pop(0)

    # Note: we transpose the ys array to match solve_ivp
    res = OdeResult(t=np.asarray(ts), y=np.asarray(ys).T)

    # Save args for starting again.
    res.abm_args = dict(ys=res.y[-4:], dys=np.asarray(dys[-4:]), dcp=dcp)
    return res


def solve_ivp_euler(fun, t_span, y0, Nt):
    """Solve the specified IVP using Euler's method.

    Arguments
    ---------
    Nt : int
       Number of steps.  The time-step will be `(t_span[1] - t_span[0])/Nt`.

    Returns
    -------
    res : OdeResult
       Bunch object.

    The remaining arguments should match those of `scipy.integrate.solve_ivp`.  Don't
    worry about optimizations like allowing `fun` to be `vectorized` etc.
    """
    t0, t1 = t_span
    dt = (t1 - t0) / Nt

    ts = [t0]
    ys = [np.asarray(y0)]  # Convert y0 to an array allowing user to pass in list

    for step in range(Nt):
        t = ts[-1]
        y = ys[-1]
        dy = np.asarray(fun(t, y))
        # We explicitly call np.asarray here so that dy_new is an array.  This allows
        # the user to return a list or a tuple, but allows us to work with dy as an
        # array.

        t_new = t + dt
        y_new = y + dt * dy

        ts.append(t_new)
        ys.append(y_new)

    # Note: we transpose the ys array to match solve_ivp
    res = OdeResult(t=np.asarray(ts), y=np.asarray(ys).T)
    return res


def solve_ivp_rk4(fun, t_span, y0, Nt):
    """Solve the specified IVP using 4th order Runge-Kutta.

    Arguments
    ---------
    Nt : int
       Number of steps.  The time-step will be `(t_span[1] - t_span[0])/Nt`.

    Returns
    -------
    res : OdeResult
       Bunch object.

    The remaining arguments should match those of `scipy.integrate.solve_ivp`.  Don't
    worry about optimizations like allowing `fun` to be `vectorized` etc.
    """
    t0, t1 = t_span
    dt = (t1 - t0) / Nt

    ts = [t0]
    ys = [np.asarray(y0)]  # Convert y0 to an array allowing user to pass in list

    for step in range(Nt):
        t = ts[-1]
        y = ys[-1]
        dy = np.asarray(fun(t, y))
        # We explicitly call np.asarray here so that dy_new is an array.  This allows
        # the user to return a list or a tuple, but allows us to work with dy as an
        # array.

        ##### This is incorrect!  Do your work here...
        t_new = t + dt
        y_new = y + dt * dy

        ts.append(t_new)
        ys.append(y_new)

    # Note: we transpose the ys array to match solve_ivp
    res = OdeResult(t=np.asarray(ts), y=np.asarray(ys).T)
    return res
