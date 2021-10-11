"""Assignment 2
"""
import math

import numpy as np

from scipy.optimize import OptimizeResult


class OdeResult(OptimizeResult):
    """Bunch object for storing results of solve_ivp* methods."""


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
    ys : [y0, y1, y2, y3] or None
        First four steps to get the process started.  If not provided, then these
        will be computed using `solve_ivp_rk4`.
    dys : [dy0, dy1, dy2, dy3] or None
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

        ys = res0.y.T[::start_factor]

    # Keep only Nt previous values... allows code to work if Nt < 4.
    ys = ys[: Nt + 1]

    # Compute corresponding ts.
    ts = t0 + np.arange(len(ys)) * dt

    if dys is None:
        dys = [fun(_t, _y) for (_t, _y) in zip(ts, ys)]

    dys = dys[: Nt + 1]

    # Convert ts, ys, and dys to lists so we can append etc.  This is a little
    # convoluted but does not allocate more memory if the previous values were arrays.
    ts, ys, dys = ([np.asarray(_y) for _y in _ys] for _ys in (ts, ys, dys))

    if dcp is None:
        # If not provided, assume it is zero.
        dcp = 0

    for nt in range(Nt - len(ys) + 1):
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

        if save_memory:
            ts.pop(0)
            ys.pop(0)
            dys.pop(0)

        ts.append(t_new)
        ys.append(y_new)
        dys.append(dy_new)

    assert np.allclose(ts[-1], t1)
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


def step_rk45(fun, t, y, f, h):  # pragma: no cover
    """Take one step using the RK45 algorithm.

    Parameters
    ----------
    fun : callable
        Right-hand side of the system.
    t : float
        Current time.
    y : ndarray, shape (n,)
        Current state.
    f : ndarray, shape (n,)
        Current value of the derivative, i.e., ``fun(x, y)``.
    h : float
        Step to use.

    Returns
    -------
    y_new : ndarray, shape (n,)
        Solution at t + h computed with a higher accuracy.
    f_new : ndarray, shape (n,)
        Derivative ``fun(t + h, y_new)``.

    References
    ----------
    .. [1] E. Hairer, S. P. Norsett G. Wanner, "Solving Ordinary Differential
           Equations I: Nonstiff Problems", Sec. II.4.
    """
    A = np.array(
        [
            [0, 0, 0, 0, 0],
            [1 / 5, 0, 0, 0, 0],
            [3 / 40, 9 / 40, 0, 0, 0],
            [44 / 45, -56 / 15, 32 / 9, 0, 0],
            [19372 / 6561, -25360 / 2187, 64448 / 6561, -212 / 729, 0],
            [9017 / 3168, -355 / 33, 46732 / 5247, 49 / 176, -5103 / 18656],
        ]
    )
    B = np.array([35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84])
    C = np.array([0, 1 / 5, 3 / 10, 4 / 5, 8 / 9, 1])
    E = np.array(
        [-71 / 57600, 0, 71 / 16695, -71 / 1920, 17253 / 339200, -22 / 525, 1 / 40]
    )
    K = [f]
    K[0] = f
    for s, (a, c) in enumerate(zip(A[1:], C[1:]), start=1):
        dy = np.dot(K[:s].T, a[:s]) * h
        K[s] = fun(t + c * h, y + dy)

    y_new = y + h * np.dot(K[:-1].T, B)
    f_new = fun(t + h, y_new)

    K[-1] = f_new

    return y_new, f_new
