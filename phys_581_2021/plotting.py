"""Tools for plotting."""
import numpy as np

import scipy.stats

from matplotlib import pyplot as plt

import uncertainties
from uncertainties import unumpy as unp

sp = scipy


def corner_plot(
    a,
    C=None,
    labels=None,
    levels=None,
    sigmas=(1, 2, 3, 4),
    axes=None,
    fig=None,
    Nxy=(100, 101),
    contour_kw=None,
):  # pragma: no cover
    """Make a corner-plot of the variables `a`.

    Parameters
    ----------
    a : [float] or [uncertainties.ufloat]
        Parameter values.  These can be `ufloat` values from the :py:mod:`uncertainties`
        package.
    C : array-like, optional
        Covariance matrix.  If `a` is a list of `ufloat`s, then the correlation matrix
        will be computed with `C = uncertainties.covariance_matrix(a)` if not provided.
    labels : [str], optional
        Labels for plot.  If not provided, then if `a._fields` exists, these will be
        used, otherwise, they will be labelled `a_n`.
    levels : array-like, optional
        Contours to draw.  If not, then we will assume the variables are gaussian and
        use the ``nu=2`` degree-of-freedom chi square distribution to convert from
        `sigmas`.
    sigmas : array-like, optional
        If provided and `levels` is `None`, then use to generate levels.
    axes : array of Axes, optional
        If provided, then the we will draw in these.
    Nxy : (int, int)
        Size of grid for contour plot.
    contour_kw : dict, optional
        Additional arguments for :py:meth:`matplotlib.axes.Axes.contour` like
       `linestyles`, and `colors`.
    """
    Na = len(a)
    if C is None:
        C = np.asarray(uncertainties.covariance_matrix(a))
    if labels is None:
        labels = getattr(a, "_fields", [f"$a_{_n}$" for _n in range(Na)])

    a = unp.nominal_values(a)

    sigmas = np.asarray(sigmas)
    sigma_max = 1.5 * max(sigmas)
    if levels is None:
        q = sp.stats.norm.cdf(sigmas) - sp.stats.norm.cdf(-sigmas)
        levels = sp.stats.chi2.ppf(q, df=2)
    axs = axes
    if axs is None:
        if fig is None:
            fig = plt.figure(figsize=(10, 10))
        axs = fig.subplots(
            Na,
            Na,
            sharex="col",
            sharey="row",
            gridspec_kw=dict(hspace=0, wspace=0),
        )

    if contour_kw is None:
        contour_kw = {}

    for i, ai in enumerate(a):
        for j, aj in enumerate(a):
            if i <= j:
                if axes is None:  # Only toggle visibility if we generated axes
                    axs[i, j].set(visible=False)
                continue
            ax = axs[i, j]
            inds = np.array([[i, j]])
            C2 = C[inds.T, inds]
            sigma_i, sigma_j = np.sqrt([C[i, i], C[j, j]])
            dai = np.linspace(-sigma_max * sigma_i, sigma_max * sigma_i, Nxy[0])
            daj = np.linspace(-sigma_max * sigma_j, sigma_max * sigma_j, Nxy[1])
            das = np.meshgrid(dai, daj, indexing="ij", sparse=False)
            dchi2 = np.einsum("xij,yij,xy->ij", das, das, np.linalg.inv(C2))
            ax.contour(
                a[j] + daj,
                a[i] + dai,
                dchi2,
                levels=levels,
                **contour_kw,
            )

            if j == 0:
                ax.set(ylabel=f"{labels[i]}")
            if i == len(a) - 1:
                ax.set(xlabel=f"{labels[j]}")
    return fig, axs
