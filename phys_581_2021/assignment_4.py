"""Assignment 4: Chaos
"""
import numpy as np

from scipy.integrate import solve_ivp

_DEFAULT_RNG = np.random.default_rng(0)


def compute_lyapunov(
    compute_dy_dt,
    y0,
    dy0=None,
    t0=0,
    dt=None,
    min_norm=None,
    Nsamples=None,
    norm=np.linalg.norm,
    rng=_DEFAULT_RNG,
    debug=False,
    solve_ivp_args=None,
):
    """Return a list of uncorrelated values `lams` estimating the maximal Lyapunov
    exponent for the ODE.

    The arguments here follow the conventions required by `solve_ivp`, but the actual
    solver used is up to implementer.

    Arguments
    ---------
    compute_dy_dt : function
        Return `dy_dt = compute_dy_dt(t, y)`.
    y0 : array-like
        Initial state.
    dy0 : array-like, None
        Initial direction to store.  If `None`, then this is chosen randomly.

    t0 : float
        Initial time.
    dt : float, None
        Evolve for this length of time when computing the exponent.  If `None`, then
        a reasonable value should be estimated by the code.  (The code may adaptively
        update `dt`.)
    min_norm : float, None
        Minimum norm. Start with states separated by `min_norm`, then evolve by `dt`,
        extract the exponent, add this to the samples, then pull the state back along
        the same direction to have length `min_norm` and repeat.  If `None`, then
        reasonable values should be estimated by the code.
    Nsamples : int
        Number of samples to use when estimating the Lyapunov exponent.  The estimate
        should be the mean of this many samples with an error as the standard deviation.
    norm : function
        Use this function to compute the norm of the difference between states.
        (Default is `np.linalg.norm`.)
    rng : random number generator
        Random number generator such as returned by `np.random.default_rng()`, which is
        used by default if one is not provided.
    debug : bool
        If `True`, then return `(lams, ts, ys, dys)` with the sample evolution.
    solve_ivp_args : dict, None
        Additional arguments for `solve_ivp`.

    Returns
    -------
    lams : array of floats
        Array of maximal Lyapunov exponents such that the mean and standard deviations
        give a good estimate.  These should be uncorrelated.
    ts, ys, dys : array
        Only provided if `debug` is `True`.  Times, states, and separations used in
        sampling.
    """
    if min_norm is None or dt is None:
        ### To Do: Implement here code to estimate good values for min_norm and dt.
        raise NotImplementedError(
            "Automatic `min_norm` and `dt` determination not implemented"
        )

    t0 = 0
    y0 = np.asarray(y0)

    if dy0 is None:
        # Get a random displacement with positive and negative values.  We use a trick
        # here of converting y0 to a flat floating point array so that if it happens to
        # be complex, we can generate random real and imaginary parts.
        y0_real_flat = y0.view(dtype=float).ravel()
        dy0 = (
            (rng.random(len(y0_real_flat)) - 0.5).view(dtype=y0.dtype).reshape(y0.shape)
        )

    dy0 = np.asarray(dy0)

    # Here is rough code... you should improve this, especially if you want to
    # dynamically determine dt.
    t = t0
    y = y0
    dy = dy0

    lams = []

    # Only keep if debugging (to keep the memory footprint down)
    if debug:
        ts = []
        ys = []
        dys = []

    if solve_ivp_args is None:
        solve_ivp_args = {}

    for n in range(Nsamples):
        # Normalize dy to have length min_norm.
        dy = dy * min_norm / norm(dy)

        # Here is where we do the evolution.  This should definitely be improved to make
        # sure that the evolution is stable and numerically accurate.
        kwargs = dict(solve_ivp_args, fun=compute_dy_dt, t_span=(t, t + dt))
        res0 = solve_ivp(y0=y, **kwargs)
        t_eval = res0.t
        # Use same ts with t_eval to makes sure times match.
        res1 = solve_ivp(y0=y + dy, t_eval=t_eval, **kwargs)

        t += dt
        y0s = res0.y
        y1s = res1.y
        dys_ = y1s - y0s
        dy_norms = norm(dys_, axis=0)

        # Here we use np.polyfit to fit a straight light to the log of the norms.  This
        # could definitely be improved with some kind of check to see if the data is
        # really well modeled by a straight line.
        lam = np.polyfit(t_eval, np.log(dy_norms), deg=1)[0]

        y = y0s[:, -1]
        dy = dys_[:, -1]

        if debug:
            ts.append(t_eval)
            ys.append(y0s)
            dys.append(dys_)

        lams.append(lam)

    if debug:
        return (lams, ts, ys, dys)
    return lams
