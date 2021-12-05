---
execution:
  timeout: 300
jupytext:
  notebook_metadata_filter: all
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.1
kernelspec:
  display_name: Python 3 (phys-581-2021)
  language: python
  name: phys-581-2021
language_info:
  codemirror_mode:
    name: ipython
    version: 3
  file_extension: .py
  mimetype: text/x-python
  name: python
  nbconvert_exporter: python
  pygments_lexer: ipython3
  version: 3.9.7
---

```{code-cell} ipython3
:tags: [hide-cell]

import mmf_setup

mmf_setup.nbinit()
import logging

logging.getLogger("matplotlib").setLevel(logging.CRITICAL)
%matplotlib inline
import numpy as np, matplotlib.pyplot as plt
```

# Model Fitting E.g. 1: Cosine

Here we go through the step-by-step procedure for fitting data to the following model:

\begin{gather*}
   y_n = f(t_n, \vect{a}) + e_n, \qquad
   f(t, \vect{a}) = A\cos(\omega t + \phi) + c, \qquad
   \vect{a} = \begin{pmatrix}
     \omega\\
     c\\
     A\\
     \phi
   \end{pmatrix}.
\end{gather*}

We shall assume that the errors are independently distributed, considering both the case
of gaussian errors, and non-gaussian: 

\begin{gather*}
  p_n(e_n) = \frac{p_e(e_n/\sigma_n)}{\sigma_n}, \qquad
  p_e(x) = \overbrace{\frac{e^{-x^2/2}}{\sqrt{2\pi}}}^{\text{gaussian}}.
\end{gather*}

We start with the gaussian case, and assume that the errors are sufficiently small that
the standard analysis techniques based on $\chi^2(\vect{a})$ apply as discussed in
chapter 15 of {cite:p}`PTVF:2007`.  We then test these using Monte Carlo (MC) and then
use an MCMC approach to solve the general case.

To make our examples mode modular, I am going to use a class to represent the mock
experiment.  We can specify the nature of the errors, and generate sample experiments
for our analysis.

```{code-cell} ipython3
from IPython.display import Latex
from collections import namedtuple
from functools import partial
import uncertainties
from uncertainties import unumpy as unp
from scipy.optimize import least_squares
import scipy.stats
sp = scipy


class Experiment:
    """Class representing a mock experiment.
    
    Attributes
    ----------
    a : Params
        Exact parameter values.
    ts : array-like
        Times at which to sample the function.
    ys : array-like
        Exact values sampled at the specified times.
    ydata : array-like
        Simulated measurement.
    """ 
    Params = namedtuple("Params", ["w", "c", "A", "phi"])
    labels = [r"$\omega$", r"$c$", r"$A$", r"$\phi$"]

    def __init__(self, 
                 random=np.random.default_rng(seed=2).normal, 
                 ts=np.linspace(0, 10.0, 7),
                 sigmas=0.5,
                 a=Params(w=2 * np.pi / 5, c=2.1, A=3.4, phi=5.6)):
        """Constructor.
        
        Arguments
        ---------
        random : function
            Random generator for the errors.  Should return 
            sample errors from a normalized distribution.  Will
            be scaled by sigmas to get the actual errors.
        ts : array-like
            Range of times at which to sample the function.
        sigmas : float or array-like
            Errors.
        """
        self.random = random
        self.ts = np.asarray(ts)
        self.a = self.Params(*a)
        self.ys = self.f(self.ts, *self.a)
        
        # Allow sigmas to be a float
        self.sigmas = np.zeros_like(ts) + sigmas
        self.ydata = self.measure()
    
    def f(self, ts=None, *a, np=np):
        """Model function."""
        if not a:
            a = self.a
        if ts is None:
            ts = self.ts

        a = self.Params(*a)
            
        return a.c + a.A * np.cos(a.w * ts + a.phi)
        
    def measure(self, ys=None, a=None, sigmas=None):
        """Return `ydata` corresponding to a simulated measuement."""
        if ys is None:
            if a is None:
                ys = self.ys
            else:
                ys = self.f(self.ts, *a)
        if sigmas is None:
            sigmas = self.sigmas
        return self.random(loc=ys, scale=sigmas)
        
    def residuals(self, a, ydata=None, sigmas=None):
        """Return the residuals for least_square.
        
        May be overloaded to implement robust fitting models.
        
        Arguments
        ---------
        a : Params
            Parameter estimate.
        """
        if ydata is None:
            ydata = self.ydata
        if sigmas is None:
            sigmas = self.sigmas
        return (ydata - self.f(self.ts, *a))/sigmas
    
    FitResults = namedtuple("FitResults", 
                            ['a', 'C', 'chi2_r', 'nu', 'a_'])
    
    def fit(self, ydata=None, sigmas=None):
        """Return `FitResults` from least_squares fit.
        
        Arguments
        ---------
        ydata : array-like, optional
            Experimental data.  Uses `self.ydata` if not provided.

        Returns
        -------
        a : Params
            Parameter estimates.
        C : array
            Covariance matrix.
        chi2_r : float
            Sum of the residuals normalized by `nu`.
        nu : int
            Effectve number of degrees of freedom.
        a_ : Params
            Correlated parameter estimates using
            `uncertainties.correlated_values`.
        """
        if ydata is None:
            ydata = self.ydata
        if sigmas is None:
            sigmas = self.sigmas
            
        # Using simple numpy functions, we can compute the jacobian
        # with the complex-step method.
        fun = partial(self.residuals, ydata=ydata, sigmas=sigmas)
        res = least_squares(fun=fun, x0=self.a, jac='cs')
        a = self.Params(*res.x)
        C = np.linalg.inv(res.jac.T @ res.jac)
        a_ = self.correlated_values(a, C)
        r = self.residuals(a, ydata=ydata, sigmas=sigmas)
        nu = len(r) - len(a)
        chi2_r = np.sum(abs(r)**2) / nu
        
        return self.FitResults(a=a, C=C, chi2_r=chi2_r, nu=nu, a_=a_)

    def correlated_values(self, a, C):
        """Return `Params()` as correlated values using 
        `uncertainties.correlated_values`
        """
        return self.Params(*uncertainties.correlated_values(a, C))
        
    def sample_chi2_r(self, Nsamples=2000, a=None):
        """Return samples of the chi2_r obtained by repeated fitting.
        
        Arguments
        ---------
        a : Params, optional:
            Parameter values.  If not provided, `self.a` will be
            used, otherwise we will assume that the supplied
            parameters are to be used as a proxy model.
        Nsamples : int
            Number of samples.
        """
        if a is None:
            a = self.a
        chi2_rs = [self.fit(ydata=self.measure(a=a)).chi2_r
                   for n in range(Nsamples)]
        return chi2_rs
        
    def plot(self, a_=None, a_sigmas=[1, 2, 3, 4], ax=None):
        """Display the current experiment.
        
        Arguments
        ---------
        a_ : Params
            Correlated best fit parameters.  If provided, this fit 
            will be shown with the corresponding confidence regions.
        a_sigmas : array-like
            Bands to show.
        """
        if ax is None:
            fig, ax = plt.subplots()

        ts = np.linspace(self.ts.min(), self.ts.max())
        ax.errorbar(self.ts, self.ydata, yerr=self.sigmas, 
                    fmt="C0.", ecolor="C1", label="data")
        ax.plot(ts, self.f(ts), "-C2", label="exact")
        
        if a_ is not None:
            ys_ = self.f(ts, *a_, np=unp)
            fc = "C3"
            alphas = np.linspace(0.5, 0.1, len(a_sigmas))
            for sigma, alpha in zip(a_sigmas, alphas):
                self.plot_band(ts, ys_, sigma=sigma, ax=ax, 
                               fc=fc, alpha=alpha,
                               label=fr"${sigma}\sigma$ band")

        ax.set(xlabel="$t$", ylabel="$f(t)$")
        
        ax.legend()
        return ax
    
    def plot_band(self, t, y_, sigma=1, ax=None, **kw):
        """Plot a band using correlated errors in y_."""
        if ax is None:
            ax = plt.gca()
        y = unp.nominal_values(y_)
        dy = unp.std_devs(y_)
        ax.fill_between(t, y-dy*sigma, y+dy*sigma, **kw)
        return ax
```

## Linear Gaussian Approximation

We start with an "exact" solution, then generate some data to analyze at $N_t$ equally spaced
points for $t \in [0, t_\max]$.

```{code-cell} ipython3
expt = Experiment(ts=np.linspace(0, 10.0, 7), 
                  random=np.random.default_rng(seed=2).normal)

fig, ax = plt.subplots(figsize=(10, 5))
expt.plot(ax=ax)
```

### Chi Square Fit

Now we do the fit.  We use {py:func}`scipy.optimize.least_squares` which requires a
function that returns the list of weighted residuals:

\begin{gather*}
  r_n = \frac{y_n - f(x_n, \vect{a})}{\sigma_n}.
\end{gather*}
 
This minimizes the following **cost function**, for which the Hessian is the inverse
covariance matrix:

\begin{gather*}
  \frac{\chi^2}{2} = \frac{1}{2}\sum_{n} r_n^2, \qquad
  \mat{C}^{-1} = \mat{J}^T\cdot \mat{J}.
\end{gather*}

```{code-cell} ipython3
res = expt.fit()

# Since our errors are gaussian and small, we expect that the 
# standard chi2 distribution will hold, so we can compute the
# Q values using the corresponding CDF:
Q = 1 - sp.stats.chi2.cdf(res.chi2_r*res.nu, df=res.nu)

Latex(rf"$\chi^2_r = {res.chi2_r:.2g}, \qquad Q = {Q:.2g}$")
```

Here we have used the {ref}`chi-squared-distribution` $P_{\nu,\chi^2}(\chi^2)$ to calculate the
chi-square probability $Q$, sometimes called the [tail distribution]:

\begin{gather*}
  Q &= \int_{\chi^2}^{\infty} P_{\nu, \chi^2}(\chi^2)\d{\chi^2} = 
  1 - \underbrace{\int_{0}^{\chi^2} P_{\nu, \chi^2}(\chi^2)\d{\chi^2}}_{\text{CDF}}
  &= \int_{\chi^2_r}^{\infty} P_{\nu, \chi^2_r}(\chi^2_r)\d{\chi^2_r}.
\end{gather*}

This is the probability that $\chi^2$ exceeds the value found, and is the complement of
the [cumulative distribution function] (CDF).  This is sometimes called a [one-sided
$p$-value] and is used as a [test statistic] to assess whether or not the model is
reasonable.  As discussed in section 15.1 of {cite:p}`PTVF:2007`, values of $Q> 0.001$
are not too bad:

> Truly *wrong* models have values will often be rejected with vastly smaller values of
> $Q$, $10^{-18}$, say.

:::{sidebar} Distribution of $\chi^2_r$.

The solid line shows the PDF with shaded contribution to $Q$.  The dashed line shows the
CDF and the dotted horizontal yellow line show the $P=1-Q$ value at the minimum
$\chi^2_r$ for the given dataset.  To compare, we sampled and fit 2000 independent
"experiments" plotting the histogram of the $\chi^2_r$ values.  This verifies that we
have used the correct value of $\nu$ as this clearly differs from the dotted $\nu \pm 1$
curves.  We see that, although the $Q$ for our original experiment is not great, it is
actually perfectly consistent with the data -- we just got unlucky, which happens.

:::

Here we plot the distribution of the reduced chi squared for our dataset with $\nu = N -
M$ degrees of freedom:

\begin{gather*}
  \chi^2_r = \frac{\chi^2}{\nu},\qquad
  P_{\nu,\chi^2_r}(\chi^2_r) = \nu P_{\nu, \chi^2}(\nu\chi^2_r).
\end{gather*}

```{code-cell} ipython3
:tags: [hide-input]

# Generate actual distribution of chi2_r using MC

Ns = 2000  # number of samples
chi2_rs = expt.sample_chi2_r()

res = expt.fit()
nu, chi2_r = res.nu, res.chi2_r

_chi2_r = np.linspace(0, 3, 500)
_i = np.where(_chi2_r >= chi2_r)[0][0]
fig, ax = plt.subplots()
ax.plot(_chi2_r, nu*sp.stats.chi2.pdf(nu*_chi2_r, df=nu), 
        "-C0", label=rf"PDF ($\nu={nu}$)")
ax.plot(_chi2_r, nu*sp.stats.chi2.pdf(nu*_chi2_r, df=nu-1), 
        ":C0", label=rf"$\nu={nu}\pm 1$")
ax.plot(_chi2_r, nu*sp.stats.chi2.pdf(nu*_chi2_r, df=nu+1), 
        ":C0")
ax.plot(_chi2_r, sp.stats.chi2.cdf(nu*_chi2_r, df=nu), 
        "--C1", label="CDF")
kw = dict(bins=50, histtype='step', alpha=0.8, density=True)
ax.hist(chi2_rs, ec="C2", label=f"{Ns} samples", **kw)
ax.fill_between(_chi2_r[_i:], nu*sp.stats.chi2.pdf(nu*_chi2_r[_i:], df=nu), 
                fc="C0")
ax.axvline([chi2_r], ls=":", c="y")
ax.axhline([1-Q], ls=":", c="y")
ax.set(xlim=(0, 4),
       xlabel=r"$\chi^2_r=\chi^2/\nu$", 
       title=fr"Distribution of $\chi^2_r$ with " + 
             fr"$\nu={nu} = {len(expt.ts)}-{len(res.a)}$ degrees of freedom")
ax.legend();
```

### Parameter Estimates and Uncertainties

The results of the fit are characterized by the best-fit parameter values $\bar{\vect{a}}$ and
the covariance matrix $\mat{C}$ such that, to lowest order, $\chi^2(\vect{a})$ is quadratic:

\begin{gather*}
  \overbrace{\Delta \chi^2(\vect{a})}^{\chi^2(\vect{a})- \chi^2(\bar{\vect{a}})} 
  \approx 
  \delta\vect{a}^T
  \mat{C}^{-1}
  \overbrace{\delta\vect{a}}^{\vect{a}-\bar{\vect{a}}}.
\end{gather*}

The confidence region corresponding to confidence level $p$ is given by the region
within the contour

\begin{gather*}
  \Delta \chi^2(\vect{a})
  \approx 
  \delta\vect{a}^T
  \mat{C}^{-1}
  \delta\vect{a} < \chi^2_{p}
\end{gather*}

:::{margin}
See {ref}`confidence-regions` and especially the caveats in {ref}`confidence-levels`
corresponding to the points below.
:::
where the contour $\chi^2_{p}$ is carefully chosen so that this region contains fraction
$p$ of the samples. This can bed computed from the inverse of the [cumulative
distribution function] (CDF) for the chi squared distribution with $\nu$ degrees of freedom:

\begin{gather*}
  \int_{\rlap{P(\vect{a}) < P_p}}\d^{\nu}\vect{a}\; P(\vect{a}) = 
  \int_0^{\chi^2_p}\d{\chi^2}P_{\nu, \chi^2}(\chi^2)
  = p(\chi^2_p)
\end{gather*}

if:

1. the fit is good, 
2. the posterior distribution is well approximated by a [multivariate normal
   distribution] (i.e. if the experimental errors are gaussian and the model is linear
   in the region of these errors), and
3. you use the correct value of $\nu$ corresponding to the number of free parameters you
   wish to consider.  If you want to consider a marginal distribution of $\tilde{\nu} <
   \nu$ parameters, then just extract the corresponding $\tilde{nu}$ rows and columns
   from $\mat{C}$ (not $\mat{C}^{-1}$).

In our case, the errors are gaussian as we saw above, so we can proceed with the
simplified approach.  What we do here is use the [uncertainties] package to perform a
forward error propagation of the parameter covariance matrix $\mat{C}$ through to the
actual function values for the model $y = f(x, \vect{a})$.  We then treat each $y$ as a
single parameter ($\tilde{\nu}=1$) and use the $n\sigma$ values where $\sigma$ is the
standard deviation computed by the [uncertainties] package to produce a $1\sigma$ and
$2\sigma$ uncertainty band corresponding to our parameter values:

```{code-cell} ipython3
a_ = expt.correlated_values(res.a, res.C)
ar_ = expt.correlated_values(res.a, res.C*res.chi2_r)

fig, axs = plt.subplots(2, 1, figsize=(10, 10))
for _a_, ax in zip((a_, ar_), axs):
    expt.plot(a_=_a_, ax=ax)
axs[0].set(title=fr"$\chi^2_r={res.chi2_r:.2f}$, $Q={Q:.2g}$");
axs[1].set(title=r"Rescaled covariance so $\chi^2_r=1$");
```

:::{margin}

In this case, are errors were correct: we simply got unlucky.  This might mean that our
best fit parameters $\bar{\vect{a}}$ have a large systematic deviation from the true
values, so perhaps the extra uncertainty implied in this approach is warranted.  I need
to explore this further.  It does not seem to be generally advocated for, i.e. I do not
see it discussed in {cite:p}`PTVF:2007`.

:::

In the lower plot, we have rescaled the covariance matrix $\mat{C} \rightarrow \chi^2_r
\mat{C}$ as if we did not trust our error estimates, and interpreted the large
$\chi^2_r$ value as a sign that we underestimated the errors.

We can now look at some of the marginal distributions.  One can use a set of corner
plots to summarize this information, but we first do this explicitly.

### Single Parameter Distributions

We start with the individual parameter marginal distributions.  In this case
$\tilde{\nu} = 1$.  Since our posterior is well approximated by a gaussian, we can
simply look at the standard deviations given as the square root of the corresponding
diagonal entry of the covariance matrix: $\sigma_i = \sqrt{C_{ii}}$.  This is nicely
summarized by printing the parameters using the [uncertainties] package as we show below:

```{code-cell} ipython3
res = expt.fit()
a_, C = res.a_, res.C

fig, ax = plt.subplots()
_x = np.linspace(0, 7, 200)
for _name, _a, _Cii in zip(a_._fields, a_, np.diag(C)):
    print(f"{_name}: {_a:.2uS}, (sqrt(C_ii) = {np.sqrt(_Cii):.2g})")
    ax.plot(_x, sp.stats.norm.pdf(_x, loc=_a.n, scale=_a.s), label=_name)
ax.legend();
```

### Pairwise Distributions

Supposed we are most interested in the frequency $\omega$ and phase $\phi$.  We can
consider the marginal distribution of these two parameters by extracting the appropriate
columns and rows.  Note that we must now choose our contours using $\tilde{\nu} = 2$.
We display these as contours of $\chi^2$:

```{code-cell} ipython3
res = expt.fit()

a_ = res.a_

i, j = map(a_._fields.index, ['w', 'phi'])
w_, phi_ = a_.w, a_.phi

# Extract rows and colums.  Note: C[[i, j], [i, j]] does not work.
Cij = C[[i, j], :][:, [i, j]]

# We can also do this with the uncertainties package
from uncertainties import covariance_matrix
assert np.allclose(Cij, covariance_matrix([w_, phi_]))

_sigma = 5
ws, phis = np.meshgrid(
  np.linspace(w_.n-_sigma*w_.s, w_.n+_sigma*w_.s, 200),
  np.linspace(phi_.n-_sigma*phi_.s, phi_.n+_sigma*phi_.s, 200))

# Deviation matrix to calculate chi2
dws_phis = np.array([ws-w_.n, phis-phi_.n])

# This is just the matrix product, but we want to do this
# over a bunch of parameter values, so we use einsum.
dchi2 = np.einsum('ij,ixy,jxy->xy', 
                   np.linalg.inv(Cij), dws_phis, dws_phis)

# Use a normal distribution to compute the confidence levels
sigmas_ = np.array([1, 2, 3, 4])
ps = sp.stats.norm.cdf(sigmas_) - sp.stats.norm.cdf(-sigmas_)

# Now use chi2 distribution to get the corresponding contours
levels = sp.stats.chi2.ppf(ps, df=2)
fig, ax = plt.subplots(figsize=(10, 6))
_cs = ax.contour(ws, phis, dchi2, levels=levels, cmap="winter")
fmt = dict([(_l, fr"${_n}\sigma$")
            for _l, _n, _p in zip(levels, sigmas_, ps)])

# Draw single-parameter confidence limits to show that
# they are smaller.
for _n, _sigma in enumerate(sigmas_):
    kw = dict(c=_cs.collections[_n].get_edgecolor(), 
              alpha=0.5, zorder=-100)
    for _s in [1, -1]:
        ax.axhline(phi_.n + _s*_sigma*phi_.s, ls=":", **kw)
        ax.axvline(w_.n + _s*_sigma*w_.s, ls="--", **kw)
ax.clabel(_cs, _cs.levels, inline=True, fmt=fmt, fontsize=10)
ax.set(xlabel="$\omega$", ylabel="$\phi$");
```

We show the $1\sigma$, $2\sigma$, $3\sigma$, and $4\sigma$ $\tilde{\nu} = 2$-parameter
confidence regions demonstrating the correlations between $\omega$ and $\phi$.  For
comparison, we show the corresponding 1-parameter regions as dotted lines.  E.g. for the
$1\sigma$ confidence regions, the same amount of posterior probability (68.27%) lies
within the center blue ellipse as lies between the central vertical blue dashed lines, or
between the central horizontal blue dotted lines.

In other words, the single-parameter confidence regions include points outside of the
2-parameter ellipse, hence must be smaller as shown to keep the same probability.

Here is the full corner plot using {py:func}`phys_581_2021.plotting.corner_plot`:

```{code-cell} ipython3
from phys_581_2021.plotting import corner_plot
res = expt.fit()

fig, axs = corner_plot(res.a_, labels=expt.labels)
```

### Change of Variables

To compute a change of variables, we need to keep track of the Jacobian of the
transformation so we can properly transform the covariance matrix.  The [uncertainties]
package does this automatically, computing the derivatives with [automatic
differentiation].  This is only valid if the errors are small enough that the model is
approximately linear, but is very convenient.  Here we replace $\phi$ with the location
of the peak $t_0$:

\begin{gather*}
  \omega t + \phi \equiv \omega(t - t_0) \mod 2\pi, \qquad
  t_0 = -\phi/\omega.
\end{gather*}

```{code-cell} ipython3
# make sure t0_ is positive and small by making phi0_ between -2pi and 0
phi0_ = phi_ % (2*np.pi) - 2*np.pi
t0_ = - phi0_ / w_

Cij = covariance_matrix([w_, t0_])

_sigma = 5
ws, t0s = np.meshgrid(
  np.linspace(w_.n-_sigma*w_.s, w_.n+_sigma*w_.s, 200),
  np.linspace(t0_.n-_sigma*t0_.s, t0_.n+_sigma*t0_.s, 200))

# Deviation matrix to calculate chi2
dws_t0s = np.array([ws-w_.n, t0s-t0_.n])
dchi2 = np.einsum('ij,ixy,jxy->xy', 
                   np.linalg.inv(Cij), dws_t0s, dws_t0s)

# Now use chi2 distribution to get the corresponding contours
fig, ax = plt.subplots(figsize=(10, 6))
_cs = ax.contour(ws, t0s, dchi2, levels=levels, cmap="winter")
fmt = dict([(_l, fr"${_n}\sigma$")
            for _l, _n, _p in zip(levels, sigmas_, ps)])

# Draw single-parameter confidence limits to show that
# they are smaller.
for _n, _sigma in enumerate(sigmas_):
    kw = dict(c=_cs.collections[_n].get_edgecolor(), 
              alpha=0.5, zorder=-100)
    for _s in [1, -1]:
        ax.axhline(t0_.n + _s*_sigma*t0_.s, ls=":", **kw)
        ax.axvline(w_.n + _s*_sigma*w_.s, ls="--", **kw)
ax.clabel(_cs, _cs.levels, inline=True, fmt=fmt, fontsize=10)
ax.set(xlabel="$\omega$", ylabel="$t_0$");
```

## Non-Gaussian Errors

We now repeat the analysis, but with non-gaussian errors.  Instead, we use the [Gumbel
distribution]:

\begin{gather*}
  P_n(y_n) = \frac{1}{\sigma_n} e^{-z-e^{-z}}, \qquad
  z = \frac{y_n - f(x_n, \vect{a})}{\sigma_n}.
\end{gather*}

If we consider the normalized errors $\tilde{e}_n$, they are distributed as:

\begin{gather*}
  \tilde{e}_n = \frac{y_n - f(x_n, \bar{\vect{a}})}{\sigma_n}, \qquad
  P_n(\tilde{e}_n) = e^{-\tilde{e}_n-e^{-\tilde{e}_n}}.
\end{gather*}

The log-likelihood will be a sum of

We can use this to generate the various simulated $P_{\nu}(\chi^2)$ distributions for
Gumbel distributed errors.

```{code-cell} ipython3
en = np.linspace(-3, 10, 100)
plt.plot(en, en + np.exp(-en))
```

```{code-cell} ipython3
from scipy.interpolate import InterpolatedUnivariateSpline, UnivariateSpline

def get_cdf_ppf(samples=None):
    """Return interpolated cdf and ppf functions.

    Results
    -------
    cdf : function
        Cumulative distribution function `q=cdf(chi2_r)`.
    ppf : function
        Percent point function (inverse of `cdf`).
    """
    Ns = len(samples)
    ps = np.linspace(0, 1, Ns)
    x = sorted(samples)
    cdf = InterpolatedUnivariateSpline(x, ps, k=1, ext='const')
    ppf = InterpolatedUnivariateSpline(ps, x, k=1, ext='const')
    return cdf, ppf

def get_chi2_cdf_ppf(nu=1, random=rng.normal, Ns=10000):
    """Return `(cdf, pdf, samples)` for the chi2 distribution.
    
    Arguments
    ---------
    nu : int
        Degrees of freedom.
    random : function
        Random number generator for errors.
    Ns : int
        Number of samples.
    """
    en = random(size=(Ns, nu))
    chi2 = (en**2).sum(axis=-1)
    cdf, ppf = get_cdf_ppf(chi2)
    return cdf, ppf, chi2
```

```{code-cell} ipython3
:tags: [hide-input]

import scipy.stats
sp = scipy

chi2r_ = np.linspace(0, 4, 100)

hist_kw = dict(bins=np.linspace(0, 4, 100), histtype='step',
               alpha=0.8, density=True)
fig, axs = plt.subplots(1, 2, figsize=(10, 4))
for ax, label, random in zip(axs, 
                             ["normal", "gumbel"],
                             [rng.normal, rng.gumbel]):
    for _n, nu in enumerate([1, 2, 3, 10, 50]):
        cdf, ppf, chi2r_samples = get_chi2_cdf_ppf(nu=nu, random=random)
        chi2r_samples /= nu
        c = f"C{_n}"
        l, = ax.plot(chi2r_, cdf(nu*chi2r_), 
                     "--", lw=1, c=c, label=fr"CDF $\nu={nu}$")
        if label == "normal":
            ax.plot(chi2r_, nu*sp.stats.chi2.pdf(nu*chi2r_, df=nu), 
                    ls=":", c=c)
            ax.plot(chi2r_, sp.stats.chi2.cdf(nu*chi2r_, df=nu), 
                    ls=":", c=c)
            ax.set(xlim=(0, 2))
        else:
            ax.set(xlim=(0, 4))
        ax.hist(chi2r_samples, ec=c, **hist_kw)
    ax.set(title=rf"$\chi^2_r$ distribution for {label} errors")
    ax.set(ylim=(0, 2), xlabel=r"$\chi^2_r$")
    ax.legend(loc='upper right')
    
plt.tight_layout()
```

On the left we show the CDF and PDF histogram for $\chi^2_r$ generated from a sample of
random numbers for a standard normal distribution, comparing with the analytic forms
(dotted lines).  On the right we use the same method to compute the CDF for the standard
[Gumbel distribution].

We now generate experimental data and proceed with an analysis:

```{code-cell} ipython3
# Randomly generated data...
# An "Experiment" with non-gaussian errors.
rng = np.random.default_rng(seed=2)
ydata = rng.gumbel(loc=y, scale=sigmas)

fig, ax = plt.subplots(figsize=(10, 5))
ax.errorbar(t, ydata, yerr=sigmas, fmt="C0.", ecolor="C1", label="data")
ax.plot(ts, f(ts, *a_exact), "-C2", label="exact")
ax.set(xlabel="$t$", ylabel="$f(t)$")
ax.legend();
```

### Chi Square Fit

```{code-cell} ipython3
res = least_squares(fun=partial(get_residuals, ydata=ydata),
                    x0=a_exact, jac='cs')
p = Params(*res.x)
C = np.linalg.inv(res.jac.T @ res.jac)
r = get_residuals(p)
nu = len(r) - len(p)
chi2_r = np.sum(abs(r)**2) / nu
Q_wrong = 1 - sp.stats.chi2.cdf(chi2_r*nu, df=nu)

cdf_gumbel, pdf_gumbel, chi2s_gumbel = get_chi2_cdf_ppf(nu=nu, random=rng.gumbel)
Q = 1 - cdf_gumbel(chi2_r*nu)

Latex(r", \qquad ".join([
    rf"$\chi^2_r = {chi2_r:.2g}",
    rf"Q = {Q:.2g}",
    rf"Q_{{\mathrm{{wrong}}}} = {Q_wrong:.2g}$"]))
```

With the non-gaussian errors, estimating the $Q$ value with the chi squared distribution
gives a very wrong interpretation about the quality of the fit.  Instead, we must use
the corresponding CDF for our Gumbel-distributed errors.  To obtain the confidence
region with confidence level $p$, we must find the value of $\chi^2_p$ where:

\begin{gather*}
  \int_0^{\chi^2_p}P(\chi^2)\d{\chi^2} = p.
\end{gather*}

This is just the inverse CDF.  We can check our method (slowly) by actually fitting the
data repeatedly to generate the distribution of $\chi^2$:

```{code-cell} ipython3
:tags: [hide-input]

# Generate actual distribution of chi2_r using MC
from functools import partial

Ns = 2000  # number of samples
chi2s_data = np.array([nu*get_chi2_r(random=rng.gumbel) for n in range(Ns)])
chi2s_normal = np.array([nu*get_chi2_r(random=rng.normal) for n in range(Ns)])

cdf_data, ppf_data = get_cdf_ppf(chi2s_data)

_chi2_r = np.linspace(0, np.max(chi2s_gumbel)/nu, 500)
fig, ax = plt.subplots()
ax.plot(_chi2_r, cdf_data(nu*_chi2_r), '-C0', label="data")
ax.plot(_chi2_r, cdf_gumbel(nu*_chi2_r), ':C1', label="gumbel")
ax.plot(_chi2_r, sp.stats.chi2.cdf(nu*_chi2_r, df=nu), '--C2', label="normal")
ax.set(xlabel="$\chi^2_r$", ylabel="CDF", 
       title=fr"CDF for $P(\chi^2_r)$ for $\nu={nu}$ Gumbel-distributed errors.")

kw = dict(bins=100, histtype='step', alpha=0.8, density=True)
ax.hist(chi2s_data/nu, ec="C0", **kw)
ax.hist(chi2s_gumbel/nu, ec="C1", **kw)
ax.legend();
```

```{code-cell} ipython3
fig, ax = plt.subplots()
random = rng.gumbel
for Ns in [500, 1000]:
    chi2s_data = np.array([nu*get_chi2_r(random=random) for n in range(Ns)])
    cdf_data, ppf_data = get_cdf_ppf(chi2s_data)
    cdf_gumbel, pdf_gumbel, chi2s_gumbel = get_chi2_cdf_ppf(nu=nu, random=random)
    ax.plot(_chi2_r, cdf_data(nu*_chi2_r), '-', label=f"data {Ns}")
ax.plot(_chi2_r, cdf_gumbel(nu*_chi2_r), ':', label="gumbel")
ax.legend()
```

```{code-cell} ipython3
:tags: [hide-input]

res = expt.fit()
nu, chi2_r = res.nu, res.chi2_r

_chi2_r = np.linspace(0, 5, 500)
_i = np.where(_chi2_r >= chi2_r)[0][0]
fig, ax = plt.subplots()
ax.plot(_chi2_r, nu*sp.stats.chi2.pdf(nu*_chi2_r, df=nu), "-C1", label=rf"$\nu={nu}$")
ax.plot(_chi2_r, nu*sp.stats.chi2.pdf(nu*_chi2_r, df=nu-1), ":C1", label=rf"$\nu={nu}\pm 1$")
ax.plot(_chi2_r, nu*sp.stats.chi2.pdf(nu*_chi2_r, df=nu+1), ":C1")

ax.plot(_chi2_r, cdf_gumbel(nu*_chi2_r), "--C0", label=rf"CDF (Gumbel)")
ax.plot(_chi2_r, sp.stats.chi2.cdf(nu*_chi2_r, df=nu), "--C1", label=rf"CDF $\nu={nu}$")

# Make sure bins end on chi2_r
bins = np.linspace(0, chi2_r, 20)
_d = np.diff(bins).mean()
bins = np.concatenate([bins, np.arange(chi2_r+_d, 4+_d, _d)])
kw = dict(bins=bins, histtype='step', alpha=0.8, density=True)
res = ax.hist(chi2s_gumbel/nu, ec="C0", label=f"{Ns} samples (Gumbel)", **kw)

# Add filled region
xy = res[2][0].xy[res[2][0].xy[:, 0] >= chi2_r, :]
xy[0, 1] = 0
ax.add_patch(plt.Polygon(xy, fc="C0"))
ax.hist(chi2s_normal/nu, ls=":", ec="C1", label=fr"{Ns} samples ($\chi^2_{{\nu=3}}$)", **kw)

ax.axvline([chi2_r], ls=":", c="y")
ax.axhline([1-Q], ls=":", c="y")
ax.set(xlim=(0, 5),
       xlabel=r"$\chi^2_r=\chi^2/\nu$", 
       title=fr"Distribution of $\chi^2_r$ for $\nu={nu}$ gumbel errors; Q={Q:.2g}")
ax.legend();
```

[covariance matrix]: <https://en.wikipedia.org/wiki/Covariance_matrix>
[uncertainties]: <https://pythonhosted.org/uncertainties/>
[`collections.namedtuple`]: <https://docs.python.org/3/library/collections.html#collections.namedtuple>
[confidence region]: <https://en.wikipedia.org/wiki/Confidence_region>
[nuisance parameter]: <https://en.wikipedia.org/wiki/Nuisance_parameter>
[least squares]: <https://en.wikipedia.org/wiki/Least_squares>
[algebra of random varables]: <https://en.wikipedia.org/wiki/Algebra_of_random_variables>
[principal componant analysis]: <https://en.wikipedia.org/wiki/Principal_component_analysis>
[reduced chi-square statistic]: <https://en.wikipedia.org/wiki/Reduced_chi-squared_statistic>
[multivariate normal distribution]: <https://en.wikipedia.org/wiki/Multivariate_normal_distribution>
[Cholesky decomposition]: <https://en.wikipedia.org/wiki/Cholesky_decomposition>
[cumulative distribution function]: <https://en.wikipedia.org/wiki/Cumulative_distribution_function>
[tail distribution]: <https://en.wikipedia.org/wiki/Cumulative_distribution_function#Complementary_cumulative_distribution_function_(tail_distribution)>
[one-sided $p$-value]: <https://en.wikipedia.org/wiki/P-value>
[test statistic]: <https://en.wikipedia.org/wiki/Test_statistic>
[automatic differentiation]: <https://en.wikipedia.org/wiki/Automatic_differentiation>
[Gumbel distribution]: <https://en.wikipedia.org/wiki/Gumbel_distribution>

## References

* [Samples, samples,
  everywhere...](http://mattpitkin.github.io/samplers-demo/pages/samplers-samplers-everywhere/):
  A nice overview of different MCMC software accessible with python.
