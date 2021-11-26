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
 
## Linear Gaussian Approximation

We start with an "exact" solution, then generate some data to analyze at $N_t$ equally spaced
points for $t \in [0, t_\max]$.

```{code-cell} ipython3
from IPython.display import Latex
from collections import namedtuple
from uncertainties import correlated_values, unumpy as unp
from scipy.optimize import least_squares
from scipy.stats import chi2

Nt = 7
t_max = 10.0

# Exact parameter values
Params = namedtuple("Params", ["w", "c", "A", "phi"])
a_exact = Params(w=2 * np.pi / 5, c=2.1, A=3.4, phi=5.6)
w, c, A, phi = a_exact


def f(t, w, c, A, phi, np=np):
    """Model function."""
    return c + A * np.cos(w * t + phi)


# Exact data and experimental errors
t = np.linspace(0, t_max, Nt)
y = f(t, *a_exact)
sigmas = 0.5 * np.ones(Nt)


# Randomly generated data... An "Experiment"
rng = np.random.default_rng(seed=2)
ydata = rng.normal(loc=y, scale=sigmas)

ts = np.linspace(0, t_max)  # Many points for a smooth curve.
fig, ax = plt.subplots(figsize=(10, 5))
ax.errorbar(t, ydata, yerr=sigmas, fmt="C0.", ecolor="C1", label="data")
ax.plot(ts, f(ts, *a_exact), "-C2", label="exact")
ax.set(xlabel="$t$", ylabel="$f(t)$")
ax.legend();
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
def get_residuals(p, xdata=t, ydata=ydata, sigmas=sigmas):
    """Return residuals for least_squares."""
    return (ydata - f(xdata, *p))/sigmas
    

# By using simple numpy functions, we can compute the jacobian
# with the complex-step method.
kw = dict(jac='cs')

res = least_squares(fun=get_residuals, x0=a_exact, **kw)
p = Params(*res.x)
C = np.linalg.inv(res.jac.T @ res.jac)
r = get_residuals(p)
nu = len(r) - len(p)
chi2_r = np.sum(abs(r)**2) / nu
Q = 1 - chi2.cdf(chi2_r*nu, df=nu)

Latex(rf"\chi^2_r = {chi2_r:.2g}, \qquad Q = {Q:.2g}")
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

from myst_nb import glue

# Generate actual distribution of chi2_r using MC
from functools import partial

def sample_chi2_r():
    """Return chi2_r from a sample experiment and fit."""
    global y, sigmas, a_exact
    fun = partial(get_residuals, ydata=rng.normal(loc=y, scale=sigmas))
    res = least_squares(fun=fun, x0=a_exact, **kw)
    p = Params(*res.x)
    chi2_r = sum(abs(fun(p))**2) / nu
    return chi2_r


Ns = 2000  # number of samples
chi2_rs = [sample_chi2_r() for n in range(Ns)]

_chi2_r = np.linspace(0, 4, 500)
_i = np.where(_chi2_r >= chi2_r)[0][0]
fig, ax = plt.subplots()
ax.plot(_chi2_r, nu*chi2.pdf(nu*_chi2_r, df=nu), "-C0", label=fr"PDF ($\nu={nu-1}$)")
ax.plot(_chi2_r, nu*chi2.pdf(nu*_chi2_r, df=nu-1), ":C0", label=rf"$\nu={nu-1}$")
ax.plot(_chi2_r, nu*chi2.pdf(nu*_chi2_r, df=nu+1), ":C0", label=rf"$\nu={nu+1}$")
ax.plot(_chi2_r, chi2.cdf(nu*_chi2_r, df=nu), "--C1", label="CDF")
kw = dict(bins=50, histtype='step', alpha=0.8, density=True)
ax.hist(chi2_rs, ec="C2", label=f"{Ns} samples", **kw)
ax.fill_between(_chi2_r[_i:], nu*chi2.pdf(nu*_chi2_r[_i:], df=nu), fc="C0")
ax.axvline([chi2_r], ls=":", c="y")
ax.axhline([1-Q], ls=":", c="y")
ax.set(xlim=(0, 4),
       ylim=(0, 1.1),
       xlabel=r"$\chi^2_r=\chi^2/\nu$", 
       title=fr"Distribution of $\chi^2_r$ with $\nu={nu} = {Nt}-{len(p)}$ degrees of freedom")
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
# Here we use the uncertainties package to do linear
# error propagation of are parameter covariances
p_ = Params(*correlated_values(p, C))
pr_ = Params(*correlated_values(p, C*chi2_r))


def plot_band(t, y_, sigma=1, ax=None, **kw):
    """Plot a band using correlated errors in y_."""
    
    ### To Do: These bands are valid in the Gaussian case, but should
    ### be properly scaled using the proper confidence analysis.
    if ax is None:
        ax = plt.gca()
    y = unp.nominal_values(y_)
    dy = unp.std_devs(y_)
    ax.fill_between(t, y-dy*sigma, y+dy*sigma, **kw)
    return ax
    

ts = np.linspace(0, t_max)  # Many points for a smooth curve.
fig, axs = plt.subplots(2, 1, figsize=(10, 10))
for _p_, ax in zip((p_, pr_), axs):
    ax.errorbar(t, ydata, yerr=sigmas, fmt="C0.", ecolor="C1", label="data")
    ax.plot(ts, f(ts, *a_exact), "-C2", label="exact")
    ax.plot(ts, f(ts, *p), "--C3", label="best fit")
    plot_band(t=ts, y_=f(ts, *_p_, np=unp), ax=ax, fc="C3", alpha=0.5, 
              sigma=1, label=r"$1\sigma$ band")
    plot_band(t=ts, y_=f(ts, *_p_, np=unp), ax=ax, fc="C3", alpha=0.2, 
              sigma=2, label=r"$2\sigma$ band")
    ax.set(xlabel="$t$", ylabel="$f(t)$")
    ax.legend();
axs[0].set(title=fr"$\chi^2_r={chi2_r:.2f}$, $Q={Q:.2g}$");
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
from scipy.stats import norm

fig, ax = plt.subplots()
_x = np.linspace(0, 7, 200)
for _name, _p, _Cii in zip(Params._fields, p_, np.diag(C)):
    print(f"{_name}: {_p:.2uS}, (sqrt(C_ii) = {np.sqrt(_Cii):.2g})")
    ax.plot(_x, norm.pdf(_x, loc=_p.n, scale=_p.s), label=_name)
ax.legend();
```

### Pairwise Distributions

Supposed we are most interested in the frequency $\omega$ and phase $\phi$.  We can
consider the marginal distribution of these two parameters by extracting the appropriate
columns and rows.  Note that we must now choose our contours using $\tilde{\nu} = 2$.
We display these as contours of $\chi^2$:

```{code-cell} ipython3
from scipy.stats import norm, chi2

i, j = map(Params._fields.index, ['w', 'phi'])
w_, phi_ = p_.w, p_.phi

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
sigmas = np.array([1, 2, 3, 4])
ps = norm.cdf(sigmas) - norm.cdf(-sigmas)

# Now use chi2 distribution to get the corresponding contours
levels = chi2.ppf(ps, df=2)
fig, ax = plt.subplots(figsize=(10, 6))
_cs = ax.contour(ws, phis, dchi2, levels=levels, cmap="winter")
fmt = dict([(_l, fr"${_n}\sigma$")
            for _l, _n, _p in zip(levels, sigmas, ps)])

# Draw single-parameter confidence limits to show that
# they are smaller.
for _n, _sigma in enumerate(sigmas):
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

We now show use 

```{code-cell} ipython3

a, C = curve_fit(
    f=f, xdata=t, ydata=ydata, p0=a_exact, sigma=sigmas, absolute_sigma=True
)
a_ = Params(*correlated_values(a, covariance_mat=C))

def corner_plot(a, C, labels=[r"\omega", r"c", r"A", r"\phi"], axs=None, fig=None):
    if axs is None:
        fig, axs = plt.subplots(len(a), len(a), sharex=True, sharey=True,
            gridspec_kw=dict(hspace=0, wspace=0),
            figsize=(10, 10))
    for i, ai in enumerate(a):
        for j, aj in enumerate(a):
            if i <= j:
                if fig is not None:
                    axs[i, j].set(visible=False)
                continue
            ax = axs[i, j]
            inds = np.array([[i, j]])
            C2 = C[inds.T, inds]
            sigma_i, sigma_j = np.sqrt([C[i,i], C[j,j]])
            dai = np.linspace(-3*sigma_i, 3*sigma_i, 100)
            daj = np.linspace(-3*sigma_j, 3*sigma_j, 102)
            das = np.meshgrid(dai, daj, indexing='ij', sparse=False)
            dchi2 = np.einsum('xij,yij,xy->ij', das, das, np.linalg.inv(C2))
            ax.contour(daj, dai, dchi2,
                       colors='C0', 
                       linestyles=['-', '--', '-', '-'],
                       levels=[1.0, 2.30, 2.71, 6.63]) 
            
            if j == 0:
                ax.set(ylabel=rf"${labels[i]}$")
            if i == len(a) - 1:
                ax.set(xlabel=rf"${labels[j]}$")
    return locals()
    
locals().update(corner_plot(a, C))
dchi2.max()
```

Here we play with a multi-normal distribution.

```{code-cell} ipython3
import corner
from scipy.stats import chi2

rng = np.random.default_rng(seed=2)
L = rng.random((2, 2))
C = L @ L.T

X = rng.multivariate_normal(mean=[0, 0], cov=C, size=10000)
a0, a1 = X.T

dchi2 = np.einsum('ai,aj,ij->a', X, X, np.linalg.inv(C))

fig = plt.figure(figsize=(10,10))
fig = corner.corner(X, fig=fig);
axs = np.array([[fig.axes[0], fig.axes[1]],
                [fig.axes[2], fig.axes[3]]])
ax = axs[1,1]
corner_plot([0, 0], C, axs=axs, labels=['a0', 'a1']);

#ax.plot(chi2.ppf(0.683, df=1), 0, 1, color='y')
```

```{code-cell} ipython3
chi2s = np.linspace(0, 10, 100)
plt.hist(dchi2, bins=100, density=True);
plt.plot(chi2s, chi2.pdf(chi2s, df=2))
plt.vlines(chi2.ppf([0.683, 0.90, 0.9545, 0.99, 0.9973, 0.9999], df=2), 0, 1, color='y')
```

```{code-cell} ipython3
chi2.ppf(0.683, df=2)   # Value of chi^2 with ellipse containing 68.3% of the data
```

```{code-cell} ipython3
a
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
            for _l, _n, _p in zip(levels, sigmas, ps)])

# Draw single-parameter confidence limits to show that
# they are smaller.
for _n, _sigma in enumerate(sigmas):
    kw = dict(c=_cs.collections[_n].get_edgecolor(), 
              alpha=0.5, zorder=-100)
    for _s in [1, -1]:
        ax.axhline(t0_.n + _s*_sigma*t0_.s, ls=":", **kw)
        ax.axvline(w_.n + _s*_sigma*w_.s, ls="--", **kw)
ax.clabel(_cs, _cs.levels, inline=True, fmt=fmt, fontsize=10)
ax.set(xlabel="$\omega$", ylabel="$t_0$");
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

## References

* [Samples, samples,
  everywhere...](http://mattpitkin.github.io/samplers-demo/pages/samplers-samplers-everywhere/):
  A nice overview of different MCMC software accessible with python.
