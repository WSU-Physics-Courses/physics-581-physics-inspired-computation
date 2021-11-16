---
execution:
  timeout: 300
jupytext:
  notebook_metadata_filter: all
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.0
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
toc:
  base_numbering: 1
  nav_menu: {}
  number_sections: true
  sideBar: true
  skip_h1_title: false
  title_cell: Table of Contents
  title_sidebar: Contents
  toc_cell: false
  toc_position: {}
  toc_section_display: true
  toc_window_display: false
varInspector:
  cols:
    lenName: 16
    lenType: 16
    lenVar: 40
  kernels_config:
    python:
      delete_cmd_postfix: ''
      delete_cmd_prefix: 'del '
      library: var_list.py
      varRefreshCmd: print(var_dic_list())
    r:
      delete_cmd_postfix: ') '
      delete_cmd_prefix: rm(
      library: var_list.r
      varRefreshCmd: 'cat(var_dic_list()) '
  types_to_exclude: [module, function, builtin_function_or_method, instance, _Feature]
  window_display: false
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

# Assignment 5: Modeling Data

+++

In this assignment you will test your model against sample "experimental" in order
to try to make a "discovery" with properly quantified errors and confidence values.  In
these notes, we will perform a sample analysis with a periodic signal, but you should
use your chosen model for your analysis.

## Scenario

Imagine that your colleagues have performed an expensive experiment and obtained a small
number $N_d$ of sets of data consisting of tabulated data $D_{d} = \{(x_n, y_n)\}$ which you
believe are generated from your model

\begin{gather*}
   y_n = f(x_n, \vect{a}) + e_n(x_n)
\end{gather*}

where $\vect{a}$ are unknown parameters, and $e_{n}$ are the experimental errors.

Your task is to learn as much as possible about the parameters $\vect{a}$ from the data,
and to express this succinctly and accurately.  In particular, you should provide:

1. An estimate of the "best fit" values of the parameters $\vect{a}$.
2. An estimate of the errors/uncertainties in these parameters.
3. A statistical measure of the goodness-of-fit.

(See the discussion at the end of [section
15.0.0](https://nr304ob.s3.amazonaws.com/FW4FNZ819A0CL5ON.pdf#page=2) of {cite:p}`PTVF:2007`.)

Here we will use the least squares approach, attempting to find parameters $\vect{a}$
that minimize

\begin{gather*}
  \chi^2(\vect{a}) = \sum_{n} \left(\frac{f(x_n,\vect{a})-y_n}{\sigma_n}\right)^2,
  \qquad
  \min_{\vect{a}} \chi^2(\vect{a}) = \chi^2(\bar{\vect{a}}).
\end{gather*}

The minimum $\bar{\vect{a}}$ here will provides the first objective, the **parameter
estimates**.  Near this, $\chi^2(\vect{a})$ will be quadratic:

\begin{gather*}
  \chi^2(\vect{a})
  = \chi^2(\bar{\vect{a}}) + 
  (\vect{a} - \bar{\vect{a}})^T\cdot \mat{C}^{-1}\cdot (\vect{a} - \bar{\vect{a}})
  + \order(\delta\vect{a}^3).
\end{gather*}

The matrix $\mat{C}$ is called the **[covariance matrix]**.  This will
form the basis for our characterization of the errors or uncertainties in the
parameters.  The uncertainties in the parameters will be characterized by ellipsoids of
constant $\chi^2(\vect{a})$.

Finally, we shall see that under appropriate conditions -- namely, that the $e_n$ be
normally distributed and that the model $f(x, \vect{a})$ is approximately linear over
the region of parameter uncertainties -- then we can characterize the distribution of
$\chi^2(\vect{a})$ to determine the **confidence region**.  Specifically, in this case,
the [reduced chi-square statistic] $\chi^2_r \approx 1$ should be close to 1 if the
model is good and the errors have been appropriately characterized:

\begin{gather*}
  \chi^2_r(\vect{a}) = \frac{\chi^2(\vect{a})}{\nu}, \qquad
  \nu = N_{\mathrm{data}} - N_{\mathrm{parameters}}.
\end{gather*}

:::{important}

**If** the errors $e_n$ are normally distributed, **and** the model is linear, then you
can use the results in section 15.6.5 of {cite:p}`PTVF:2007` to determine which contours
of constant $\chi^2(\vect{a})$ correspond to which confidence regions.

If the errors are not normally distributed, then you should not rely on
$\chi^2_r(\vect{a})$ to characterize your goodness-of-fit, or your confidence regions.
Instead you must perform a Monte Carlo simulation to see how $\chi^2(\vect{a})$ is
distributed, then from this determine the contours of $\chi^2(\vect{a})$ which
correspond to which contour region.

If you model is not sufficiently linear, then you likely need to consider more advanced
techniques such as MCMC to characterize your uncertainties, which will likely be more
complicated regions than ellipsoids in parameter space.
:::

## Model: Periodic Signals

:::{margin}
As an example, we will consider later are temperature fluctuations in Moab UT.  See
{cite:p}`Forbes:2021` for details.
:::
Here we will work with the following model, looking for periodic signals in data:

\begin{gather*}
  y = c + A\cos(\omega t + \phi) = f(t,\vect{a}), \qquad
  \vect{a} = (\omega, c, A, \phi).
\end{gather*}

Our primary focus here will be to find the frequency $\omega$ or period $T=2\pi /
\omega$ (and possibly the phase $\phi$).  The other parameters $c$, $A$, (and $\phi$)
are called [nuisance parameter]s: we need to include them in our analysis, but we don't
really care about their values.

## Obtaining Fits

Before looking at real data, it is a good idea to generate some sample data with known
errors, and see what this means.  Here we start without thinking too much, applying the
standard approach of [least squares] fitting.

:::{margin}
We use two features to make interacting with the data nicer.  One is
[`collections.namedtuple`], which behaves like a tuple `p = (1.1, 1.2, 3.3, 4.2)`, but also
allows you to name each entry, so you can now do `p.w`. *(For more details and other
options, see
[Understand how to use NamedTuple and Dataclass in Python](https://towardsdatascience.com/understand-how-to-use-namedtuple-and-dataclass-in-python-e82e535c3691).)*

The second is the [uncertainties] package which can keep track of parameter values and
their errors as specified by the covariance matrix. This provides a nice way of
displaying parameters with errors, and of propagating errors.  If you do arithmetic (or
use the functions in `unp = uncertainties.unumpy` or `uncertainties.umath`), then the
errors will be propagated using linear error analysis, taking the full covariance into
account.

:::

```{code-cell} ipython3
from collections import namedtuple
from uncertainties import correlated_values, unumpy as unp

Nt = 100
t_max = 10.0

# Exact parameter values
Params = namedtuple("Params", ["w", "c", "A", "phi"])
w, c, A, phi = a_exact = Params(w=2 * np.pi / 5, c=1.2, A=3.4, phi=5.6)


def f(t, w, c, A, phi):
    """Model function."""
    return c + A * np.cos(w * t + phi)


def f_wrong(t, w, c, A, phi):
    """Wrong model function."""
    return c + A * np.cos(w * t + phi) ** 3


# Exact data and experimental errors
t = np.linspace(0, t_max, Nt)
y = f(t, *a_exact)
sigmas = 0.5 * np.ones(Nt)
wrong_sigmas = sigmas / 2.0

rng = np.random.default_rng(seed=2)
ydata = rng.normal(loc=y, scale=sigmas)
```

:::{margin}

For the incorrect model, we used

\begin{gather*}
  c + A\cos^3(\omega t +\phi)
\end{gather*}

which is more "peaky" than a pure cosine.

:::

```{code-cell} ipython3
:tags: [hide-input]

# Best fit of wrong model for plotting
from scipy.optimize import curve_fit

a_wrong = curve_fit(f=f_wrong, xdata=t, ydata=ydata, p0=a_exact)[0]

fig, axs = plt.subplots(2, 1, figsize=(10, 10))
ax = axs[0]
ax.errorbar(t, ydata, yerr=wrong_sigmas, fmt="C0.", ecolor="C1", label="data")
ax.plot(t, y, "-C2", label="exact")
ax.plot(t, f_wrong(t, *a_wrong), "--C3", label="wrong model")
ax.set(xlabel="$t$", ylabel="$f(t)$", title="Wrong (underestimated) errors")
ax.legend()

ax = axs[1]
ax.errorbar(t, ydata, yerr=sigmas, fmt="C0.", ecolor="C1", label="data")
ax.plot(t, y, "-C2", label="exact")
ax.plot(t, f_wrong(t, *a_wrong), "--C3", label="wrong model")
ax.set(xlabel="$t$", ylabel="$f(t)$", title="Correctly estimated errors")
ax.legend()
```

:::{important}
Look closely at the errors in the bottom figure and how they do not all overlap the exact
model.  These are $1\sigma$ error bars, meaning that about
[68% of the time](https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule), the
data should lie within this distance from the model, but that 32% of the data should
lie further away.  As we have carefully generated the deviations here, this gives a
visual idea of what a model and consistent data (with errors) should look like.  Can you
"see" that the wrong model is inconsistent with the data and errors?
:::

We perform three fits to demonstrate the different functions available in SciPy.  Note:
we use the `wrong_sigmas` here which underestimate the errors by a factor of 2.  This
will result in an excessively large $\chi^2_r \gg 1$, and demonstrate the meaning of the
`absolute_sigma=False` flag provided by `curve_fit` that effectively scales the errors
so that $\chi^2_r = 1$ before providing the covariance matrix $\mat{C}$.

```{code-cell} ipython3
:tags: [hide-input]

def show(p):
    """Nicer displaying of parameters with covariance.
    
    Assumes `p` is a `namedtuple` of values with correlated uncertanties::
    
        p = Params(*correlated_values(a, covariance_mat=C))
    """
    # Format .2uS means show 2 digits of precision in the uncertainties with the
    # short-form: e.g. 0.12(34)
    values = ",".join(map("{0[0]}={0[1]:.2uS}".format, zip(p._fields, p)))
    print(f"{p.__class__.__name__}({values})")


print("Defined function show() for displaying parameter estimates")
```

### `curve_fit`
  [`scipy.optimize.curve_fit`] is a good choice for fitting data to a curve.  It provides
  the covariance matrix with the option of automatically scaling of the errors to get a
  reduced $\chi^2_r = 1$ if you don't know the absolute magnitude of the errors.

  This routine takes your model function `f(x, p1, p2, ...)` and your data as an input.
  If you do not provide a guess, it will try a guess of ones.

```{code-cell} ipython3
from scipy.optimize import curve_fit

nu = len(t) - len(a_exact)
a, C = curve_fit(
    f=f, xdata=t, ydata=ydata, p0=a_exact, sigma=wrong_sigmas, absolute_sigma=True
)
a_ = Params(*correlated_values(a, covariance_mat=C))
chi2_r = (((f(t, *a) - ydata) / wrong_sigmas) ** 2).sum() / nu

print("Fit with wrong errors (too small)")
show(a_)
print(f"chi^2_r = {chi2_r:.2g}")

print("\nAfter scaling C*chi^2_r - same as absolute_sigma=False")
a_ = Params(*correlated_values(a, covariance_mat=C * chi2_r))
show(a_)

a, C = curve_fit(
    f=f, xdata=t, ydata=ydata, p0=a_exact, sigma=wrong_sigmas, absolute_sigma=False
)
a_ = Params(*correlated_values(a, covariance_mat=C))
show(a_)

print("\nFit with wrong model.")
a_wrong, C_wrong = curve_fit(
    f=f, xdata=t, ydata=ydata, p0=a_exact, sigma=sigmas, absolute_sigma=True
)
chi2_r_wrong = (((f_wrong(t, *a_wrong) - ydata) / sigmas) ** 2).sum() / nu
a_wrong_ = Params(*correlated_values(a_wrong, covariance_mat=C_wrong))
show(a_wrong_)
print(f"chi^2_r = {chi2_r_wrong:.2g}")

print("\nFit with correct errors and model")
a, C = curve_fit(
    f=f, xdata=t, ydata=ydata, p0=a_exact, sigma=sigmas, absolute_sigma=True
)
a_ = Params(*correlated_values(a, covariance_mat=C))
chi2_r_correct = (((f(t, *a) - ydata) / sigmas) ** 2).sum() / nu
show(a_)
print(f"chi^2_r = {chi2_r_correct:.2g}")
```

```{code-cell} ipython3
:tags: [hide-input]

fig, axs = plt.subplots(1, 3, figsize=(10, 3), sharey=True)

ax = axs[0]
ax.errorbar(t, f(t, *a) - ydata, yerr=wrong_sigmas, fmt="C0.", ecolor="C1")
ax.set(
    xlabel="$t$",
    ylabel="$f(t_n) - y_n$",
    title=fr"$\chi^2_r={chi2_r:.2g}$" + "\nCorrect model, wrong errors",
)

ax = axs[1]
ax.errorbar(t, f_wrong(t, *a_wrong) - ydata, yerr=sigmas, fmt="C0.", ecolor="C1")
ax.set(
    xlabel="$t$",
    title=rf"$\chi^2_r={chi2_r_wrong:.2g}$" + "\nWrong model, correct errors",
)

ax = axs[2]
ax.errorbar(
    t, f(t, *a) - ydata, yerr=sigmas, fmt="C0.", ecolor="C1", label="correct model"
)
ax.set(
    xlabel="$t$",
    title=rf"$\chi^2_r={chi2_r_correct:.2g}$" + "\nCorrect model and errors",
)
for ax in axs:
    ax.grid(True)
```

```{code-cell} ipython3
:tags: [hide-cell]

# Glue value so we can use it in the documents
from myst_nb import glue

glue("wrong_chi2_r", chi2_r)
glue("correct_chi2_r", chi2_r_correct)
```

The last result is what you should be aiming for.  Here we have used a correct estimate
of the errors, and found that $\chi^2_r = $ {glue:text}`correct_chi2_r:.2f`.  This gives
us the third component of model fitting -- a statistical measure of the goodness-of-fit
that is valid if the errors are small enough that a linear approximation to the model is
valid.  We should check this (we will below), but if it is valid, then we can trust the
other parts -- the parameter estimates and their correlated uncertainties.

::::{important}
In the other cases, the large value $\chi^2_r = $ {glue:text}`wrong_chi2_r:.2f`
indicates that something is wrong, and we must be very careful interpreting the
results.  If (and only if) we are confident in the errors (as we should be) then we can
use this to reject the model as an exceedingly unlikely explanation of the data, even
though the model "looks" good ("chi-by-eye").

However, if, after plotting the residuals, it looks like there are no systematic
deviations and the residuals look flat as they do on the left, then one might reasonably
suspect that the errors have been underestimated.  Go back to the experimentalists and
see if something is wrong.  In the meantime, you might consider using the
`absolute_sigma=False` option to get estimates of the parameter uncertainties **while
you wait**, but don't publish until you understand why your $\chi^2_r$ is so large.

If the model is incorrect, then one typically sees some sort of
systematic deviations like the periodic peak structure in the middle plot.  In this
case, the parameter estimates and values do not really have any meaning, and should be
discarded until a better model is found.

::::

### `least_squares`

[`scipy.optimize.least_squares`] is a bit more general.  This function needs to be
provided with the list of weighted residuals:

\begin{gather*}
  r_n = \frac{y_n - f(x_n, \vect{a})}{\sigma_n}
\end{gather*}
 
and will the minimize the **cost function**

\begin{gather*}
  \frac{\chi^2}{2} = \frac{1}{2}\sum_{n} r_n^2.
\end{gather*}

You could customize this, for example, to allow fitting of complex-valued data.  You
must provide an initial guess for the parameter values here. 

:::{margin}
Note that the factor of $1/2$ in the cost function ensures that the Hessian $\mat{H} =
\mat{J}^T\cdot\mat{J}$ gives the inverse covariance matrix.
:::
To construct the covariance matrix, you can use the returned Jacobian:

\begin{gather*}
   \mat{C}^{-1} = \mat{J}^T\cdot \mat{J}.
\end{gather*}

To reproduce the results of `curve_fit` with `absolute_sigma=False`, you can normalize
this by $\chi^2_r$:

\begin{gather*}
   \mat{C} \rightarrow \chi^2_r \mat{C}.
\end{gather*}

```{code-cell} ipython3
from scipy.optimize import least_squares


def get_errors(a):
    return (f(t, *a) - ydata) / wrong_sigmas


res = least_squares(fun=get_errors, x0=a_exact)

a = res.x
J = res.jac
C = np.linalg.inv(J.T @ J)
a_ = Params(*correlated_values(a, covariance_mat=C))
nu = len(t) - len(a)
chi2_r = (get_errors(a) ** 2).sum() / nu

print("Fit with wrong errors (too small)")
show(a_)
print(f"chi^2_r = {chi2_r:.2g}")

a_ = Params(*correlated_values(a, covariance_mat=C * chi2_r))
print()
print("After scaling errors to get chi^2_r=1")
show(a_)
```

### `minimize`

[`scipy.optimize.minimize`] is a generic minimizer.  This provides you with the most
flexibility, but you must provide the objective function and carefully scale the results
to get the covariance matrix.  As can be deduced from `least_square`, you will get the
correct covariance matrix $\mat{C} = \mat{H}^{-1}$ where $\mat{H}$ is the hessian
(second-derivative matrix) of the objective.  However, if you do this, you will likely
have issues with tolerances because `minimize` expects the objective function to have an
optimal value close to 1.

Instead, we should use the reduced $\chi^2_r$ as an objective, which will require
scaling the hessian to get the parameter covariance matrix:

\begin{gather*}
  \min_{\vect{a}} \chi^2_r(\vect{a})
  = \frac{1}{\nu}\sum_{n}\left(\frac{f(x_n;\vect{a}) - y_b}{\sigma_n}\right)^2, \\
  \nu = N_{\text{data}} - N_{\text{parameters}},\qquad
  \mat{C} = \frac{\mat{H}^{-1}}{\nu/2}.
\end{gather*}

```{code-cell} ipython3
from scipy.optimize import minimize


def get_chi2_r(a):
    errors = (f(t, *a) - ydata) / wrong_sigmas
    nu = len(t) - len(a)
    return (abs(errors) ** 2).sum() / nu


res = minimize(fun=get_chi2_r, x0=a_exact, method="BFGS", tol=1e-6)

print(res.message)
assert res.success
a = res.x
nu = len(t) - len(a)
C = res.hess_inv / (nu / 2)
a_ = Params(*correlated_values(a, covariance_mat=C))
chi2_r = get_chi2_r(a)

print("Fit with wrong errors (too small)")
show(a_)
print(f"chi^2_r = {chi2_r:.2g}")

print()
a_ = Params(*correlated_values(a, covariance_mat=C * chi2_r))
print("After scaling errors to get chi^2_r=1")
show(a_)
```

[`scipy.optimize.curve_fit`]: <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html>
[`scipy.optimize.least_squares`]: <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html>
[`scipy.optimize.minimize`]: <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html>

## Changing Variables

Once we have established the best fit parameters $\vect{a}$ and covariance matrix
$\mat{C} = \mat{C}^T$ we have the following model about the minimum $\bar{\vect{a}}$:

\begin{gather*}
  \overbrace{\delta\chi^2(\vect{a})}^{\chi^2(\vect{a}) - \chi^2(\bar{\vect{a}})}
  = \delta\vect{a}^T\cdot \mat{C}^{-1}\cdot \overbrace{\delta\vect{a}}^{\vect{a} -
  \bar{\vect{a}}}
  + \order(\delta\vect{a}^3)
\end{gather*}

Once we have these results, we might want to consider other parameter combinations
$\vect{b} = \vect{g}(\vect{a})$.  We can immediately transform these results **if the
$\vect{g}(\vect{a})$ is sufficiently linear** about $\bar{\vect{a}}$:

\begin{gather*}
  \vect{b} = \vect{g}(\vect{a}) \approx
  \overbrace{\vect{g}(\bar{\vect{a}})}^{\bar{\vect{b}}}
  + \mat{J}\cdot\overbrace{\delta \vect{a}}^{\vect{a} - \bar{\vect{a}}},\\
  \qquad
  \delta\vect{a} = \mat{J}^{-1}\cdot \delta\vect{b},
  \qquad
  [\mat{J}]_{ij} = \pdiff{g_i(\bar{\vect{a}})}{\bar{a}_i},\\
  \delta\chi^2 = \delta\vect{b}^T\cdot\mat{C}_{b}^{-1}\cdot\delta\vect{b}
  + \order(\delta\vect{b}^3),
  \qquad
  \mat{C}_{b} = \mat{J}\cdot\mat{C}\cdot\mat{J}^T.
\end{gather*}

This type of transformation can be done *automatically* by the [uncertainties] package,
which propagates the correlated errors through any arithmetic operations and non-linear
functions in the `uncertainties.umath` or `uncertainties.unumpy` modules.  For example,
in our model, we might want to consider the time at which the periodic signal is a
maximum, rather than the phase:

\begin{gather*}
  c + A\cos(\omega t + \phi) = c + A\cos\big(\omega (t - t_0)\big), \qquad
  t_0 = -\phi / \omega.
\end{gather*}

If $\phi$ and $\omega$ had **independent gaussian errors**, then we could use standard error
analysis techniques to deduce that the relative error in $t_0$ would be the sum of the
squares of the relative errors in $\phi$ and $\omega$:

\begin{gather*}
   \delta t_0 = \abs{t_0}\sqrt{\left(\frac{\delta \phi}{\phi}\right)^2
     + \left(\frac{\delta \omega}{\omega}\right)^2}.
\end{gather*}

```{code-cell} ipython3
from uncertainties import ufloat, covariance_matrix, correlated_values

a_ = Params(*correlated_values(a, covariance_mat=C))

w = a_.w
# Make phi lie between -2*np.pi and 0 so t0 is positive
phi = a_.phi % (2 * np.pi) - 2 * np.pi
t0 = -phi / w
print(f"Correlated   w={w:.3uS}, phi={phi:.3uS}, t0={t0:.3uS}")

# Now compute result as if errors were uncorrelated
w_ = ufloat(w.n, w.s)
phi_ = ufloat(phi.n, phi.s)
t0_ = -phi_ / w_
print(f"Uncorrelated w={w_:.3uS}, phi={phi_:.3uS}, t0={t0_:.3uS}")
dt0 = t0.n * np.sqrt((w.s / w.n) ** 2 + (phi.s / phi.n) ** 2)
print(f"Error from uncorrelated error formula dt0 = {dt0:.3g}")
```

We see here that the computed error in $t_0$ from the actual parameters is comparable
but slightly less than the estimate given by the uncorrelated error formula above.  This
is because the errors in $\omega$ and $\phi$ have some correlations as can be seen in
the off-diagonal entries of the 2-parameter covariance matrix:

```{code-cell} ipython3
covariance_matrix([phi, w])
```

## Principal Component Analysis (PCA)

By diagonalizing the symmetric covariance matrix $\mat{C} = \mat{C}^T$, we can perform a [principal
component analysis] (PCA).  We note that about the minimum $\bar{\vect{a}}$, we have the model:

:::{margin}
Close to any minimum, a function is approximately quadratic without any linear term.
Thus, we can express it locally in this form.  Since $\delta\vect{a}$ is the same on
both sides, we can take $\mat{C} = \mat{C}^T$ to be symmetric.  Finally, if we are truly
at a minimum, then $\mat{C}$ will be positive semi-definite with non-negative
eigenvalues.
:::

\begin{gather*}
  \overbrace{\delta\chi^2(\vect{a})}^{\chi^2(\vect{a}) - \chi^2(\bar{\vect{a}})}
  = \delta\vect{a}^T\cdot \mat{C}^{-1}\cdot \overbrace{\delta\vect{a}}^{\vect{a} -
  \bar{\vect{a}}}
  + \order(\delta\vect{a}^3).
\end{gather*}

By diagonalizing the covariance matrix, we can find the "principal components" -- those
linear combinations of the original parameters that are most tightly constrained by the data:

\begin{gather*}
  \mat{C} = \mat{V}\cdot\mat{D}\cdot\mat{V}^T, \qquad
  \mat{C}\cdot\vect{v}_i = \vect{v}_i \sigma_i^2, \\
  \mat{D} = \diag(\vect{\sigma}^2), \qquad
  \mat{V} = \begin{pmatrix}
    \vect{v}_0 & \vect{v}_1 & \cdots
  \end{pmatrix}.
\end{gather*}

In this new basis, we have the model

\begin{gather*}
  \delta\chi^2(\vect{a}) = (\mat{V}^T\cdot\delta\vect{a})^T
  \cdot\mat{D}^{-1}\cdot(\mat{V}^T\cdot \delta\vect{a})
  =
  \sum_{i}\frac{\lambda_i^2}{\sigma_i^2},
  \qquad
  \lambda_i = \vect{v}_{i}^T\cdot\delta\vect{a}.
\end{gather*}

The columns of $\vect{V}$ thus define an orthonormal basis (hence $\mat{V}^T =
\mat{V}^{-1}$) for parameter space such that the linear combinations of parameters along
these directions $\lambda_i$ are independent, and normally distributed with variance
$\sigma_i^2$.

Note that the $\lambda_i$ parameters represent linear combinations of the physical
parameters $\vect{a}$.  While these are well defined, the eigenvectors themselves
$\vect{v}_i$ may not make much sense unless the original variables $\vect{a}$ are
appropriately scaled to make the components of the eigenvectors compatible.  One such
option is to scale each parameter by its best fit value $\bar{\vect{a}}$, then we can
write:

\begin{gather*}
  \lambda_i = \overbrace{\vect{v}_i \bar{\vect{a}}}^{\tilde{\vect{v}}_i} \cdot
  \frac{\delta \vect{a}}{\bar{\vect{a}}}
\end{gather*}

where the $\vect{v}_i \bar{\vect{a}}$ and $\delta \vect{a}/\bar{\vect{a}}$ denote
element-wise multiplication and division respectively.  The vectors $\tilde{v}_i$ now
provide a PCA of the relative errors, and it is often instructive to plot the components
of these vectors:

:::{margin}
This code needs some checking to make sure that the scaling is done properly and the
values of $\sigma_i$ are correct.  There are many options: think about what you want to
show and define a scaling that makes sense to you.
:::

```{code-cell} ipython3
from uncertainties.unumpy import nominal_values


def num2tex(x, digits=2, min_power=-2, max_power=3):
    """Return a nice LaTeX string for the number."""
    power = int(np.floor(np.log10(abs(x))))
    mantissa = x / 10 ** power
    if min_power <= power and power <= max_power:
        mantissa = mantissa * 10 ** power
        format = f"{{:.{digits}g}}"
    elif power == 1:
        format = rf"{{:.{digits-1}f}}\times 10"
    else:
        format = rf"{{:.{digits-1}f}}\times 10^{{{{{{}}}}}}"
    return format.format(mantissa, power)


def plot_pca(a, C, labels=None, relative=True):
    """Draw a PCA eigenvector plot.
    
    Arguments
    ---------
    a : Params
        Parameter values
    C : array
        Covariance matrix
    labels : [str]
        Labels for the parameters (will use `a._fields` if `None`)
    """
    if labels is None:
        labels = p._fields
    d, V = np.linalg.eigh(C)
    assert np.allclose((V * d[np.newaxis, :]) @ V.T, C)
    if relative:
        V *= a[:, np.newaxis]
        labels = [fr"${_l}/\bar{{{_l}}}$" for _l in labels]
    else:
        labels = list(map("${}$".format, labels))

    fig, axs = plt.subplots(len(a), 1, gridspec_kw=dict(hspace=0), sharex=True)
    is_ = np.arange(len(a_))
    for i, ax, sigma2, v, label in zip(is_, axs, d, V.T, labels):
        # Normalize so maximum component is 1
        ind = np.argmax(abs(v))
        _fact = v[ind]
        sigma = np.sqrt(sigma2 / _fact ** 2)
        ax.bar(is_, v / _fact)
        ax.set(ylim=(-1.2, 1.2))
        ax.yaxis.set_label_position("right")
        ax.set_ylabel(fr"$\sigma_{i} = {num2tex(sigma)}$", ha="left", rotation=0)
        ax.grid(True)
    ax.set_xticks(is_)
    ax.set_xticklabels(labels)


plot_pca(a, C, labels=[r"\omega", r"c", r"A", r"\phi"])
display(plt.gcf())

# New parameters with t0 instead of w.  Note that the uncertainties package
# can construct a covariance matrix from any set of parameters.
p_new = np.concatenate([a_[:3], [t0]])
C_new = covariance_matrix(p_new)
plot_pca(nominal_values(p_new), C_new, labels=[r"\omega", r"c", r"A", r"t_0"])
display(plt.gcf())
plt.close("all")

show(a_)
show(Params(*(a_ / a)))
```

```{code-cell} ipython3
show(Params(*correlated_values(a, C)))
np.sqrt(np.diag(C / a[:, None] / a[None, :]))
np.sqrt(np.diag(C))
```

## Correlated Errors and the Covariance Matrix

The covariance matrix $\mat{C}$ describes the local dependence of $\chi^2$ on the
deviations $\delta\vect{a} = \vect{a} - \bar{\vect{a}}$ from the best fit values:

```{math}
  :label: eq:chi2_C
  \delta\chi^2 \approx \delta\vect{a}^T\cdot\mat{C}^{-1}\cdot\delta\vect{a}
```

We should check this to be sure.  Note that if we vary a single parameter $a_i$ while
holding the others fixed, then we should find:

\begin{gather*}
  \delta\chi^2 \approx \delta a_i^2 [\mat{C}^{-1}]_{ii}.
\end{gather*}

This is easy to check numerically

:::{margin}
Note that from this plot it is easy to see that the parameter $\omega$ is the most
tightly constrained, followed by $\phi$, $c$, and then $A$, which is most poorly
constrained.  This is consistent with the PCA.
:::

```{code-cell} ipython3
a, C = curve_fit(
    f=f, xdata=t, ydata=ydata, p0=a_exact, sigma=sigmas, absolute_sigma=True
)
a_ = Params(*correlated_values(a, covariance_mat=C))

def get_chi2(a, i=0, dai=0):
    a_ = np.copy(a)
    a_[i] += dai
    return (((f(t, *a_) - ydata) / sigmas)**2).sum()

Cinv = np.linalg.inv(C)

fig, ax = plt.subplots()
chi2 = get_chi2(a=a)
for i in range(len(a)):
    sigma_i = 1/np.sqrt(Cinv[i,i])
    dais = np.linspace(-sigma_i, sigma_i, 30)
    chi2s = [get_chi2(a=a, i=i, dai=dai) - chi2 for dai in dais]
    l, = ax.plot(dais, chi2s, "--", label=f"$a_i$ = {Params._fields[i]}")
    ax.plot(dais, dais**2 / sigma_i**2, ".", c=l.get_c())
ax.set(xlabel="$a_i$", ylabel=r"$\delta\chi^2$")
ax.legend();
```

Here we see that our interpretation of the diagonals of $\mat{C}^{-1}$ correspond with
the behavior of $\chi^2$.  This supports the following interpretation of the diagonal
elements of $\mat{C}^{-1}$ and $\mat{C}$:

:::{margin}
Prove the second meaning by using the quadratic model {eq}`eq:chi2_C`.  Vary $a_i$ but
then find the new minimum for the other parameters with this fixed value of $a_i$.  This
should allow $\delta\chi^2$ to relax compared to the results shown in the figure,
resulting in a larger range $\sigma_i > \sigma_i'$.  $\sigma_i$ corresponds to the
bounds $A-A'$ in figure 15.6.4 of {cite:p}`PTVF:2007, while $\sigma'_i$ corresponds to
the bounds $Z-Z'$.  As discussed in the text, only the wider bound of $\sigma_i$
corresponding to the diagonals of the covariance matrix are useful for describing errors.
:::

1. The diagonal elements $\sigma'_i = 1/\sqrt{[\mat{C}^{-1}]_{ii}}$ tell us how much we can
   vary the parameter $a_i$ away from the best fit value before $\chi^2$ changes by 1
   **while holding the other parameters fixed**.  I.e. $a_i \in (\bar{a}_i \pm \sigma'_{i})$.

2. The diagonal elements $\sigma_i = \sqrt{\mat{C}_{ii}}$ tell us how much we can
   vary the parameter $a_i$ away from the best fit value before $\chi^2$ changes by 1
   **while re-minimizing over the other parameters fixed**.
   
Thus, we can describe the distribution of parameters as ellipsoids of constant $\delta\chi^2$:

\begin{gather*}
  \delta\chi^2 \approx \delta\vect{a}^T\cdot\mat{C}^{-1}\cdot\delta\vect{a}.
\end{gather*}

To plot these in 2D, we can factor $\mat{C} = \mat{L}\cdot\mat{L}^T$ using either a
[Cholesky decomposition] or the same diagonalization as performed above in the PCA:
$\mat{C} = \mat{V}\cdot\mat{D}\cdot\mat{V}^T$, $\mat{L} =
\mat{V}\cdot\sqrt{\mat{D}}$.  We then have:

\begin{gather*}
  \delta\chi^2 \approx \vect{x}^T\cdot\vect{x}, \qquad
  \delta\vect{a} = \mat{L}\cdot \vect{x}.
\end{gather*}

Thus, the ellipsoids of constant $\chi^2$ are spheres in the space $\vect{x}$.  We can
now plot these pairwise in a "corner plot":

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

## Confidence Region

To describe the 





If our errors are indeed gaussian and the model is a good
fit, then we can consider the parameters $\vect{a}$ to be distributed with a
[multivariate normal distribution] about their mean $\bar{\vect{a}}$:

\begin{gather*}
  P(\delta\vect{a}) = \frac{1}{\sqrt{(2\pi)^{N} \det \mat{\Sigma}}}\exp\left(
    -\frac{1}{2}\delta\vect{a}^T\cdot\mat{\Sigma}^{-1}\delta\vect{a}\right),
  \\
  \mat{\Sigma} = \mat{C}, \qquad
  \delta\vect{a} = \vect{a} - \bar{\vect{a}}.
\end{gather*}







Consider $\chi^2(\vect{a})$ as a function of the parameters $\vect{a} = \bar{\vect{a}} +
\delta\vect{a}$ where $\bar{\vect{a}}$ are the exact parameter values for the model with
experimental errors $e_n$ of a known distribution:

\begin{gather*}
  y_n = f(x_n, \bar{\vect{a}}) + e_n.
\end{gather*}

If the errors are sufficiently small we can expand the model about the exact parameters
in powers of $\delta\vect{a} = \vect{a} - \bar{\vect{a}}$:

\begin{gather*}
  f(x_n, \vect{a}) = f(x_n, \bar{\vect{a}}) + \vect{J}_n^T\cdot\delta\vect{a}
  + \frac{1}{2}\delta\vect{a}^T\cdot \mat{H}_n\cdot\delta\vect{a}
  + \order(\delta\vect{a}^2), \\
  [\vect{J}_n]_{i} = \pdiff{f(x_n, \bar{\vect{a}})}{\bar{a}_i}, \qquad
  [\mat{H}_n]_{ij} = \frac{\partial^2 f(x_n, \bar{\vect{a}})}{\partial\bar{a}_i\partial\bar{a}_j}.
\end{gather*}



Confidence Levels

If the experimental errors $e_n$ are independent and normally distributed, **and** your
model is sufficiently linear, then you can use the formulae discussed in section 15.6.5
of {cite:p}`PTVF:2007` to determine the confidence limits of your parameter estimates
and the corresponding covariance matrix $\mat{C}$.  The procedure in this case is:

1. Let $\nu$ be the number of fitted parameters whose





:::{sidebar} Algebra of Random Variables

See {ref}`random_variables` for details.

:::
If we treat the errors $e_n$ as independent [random
variables](https://en.wikipedia.org/wiki/Random_variable) with distribution $P_n(e)$,
then we can consider the $\chi^2$ as a random variable:

\begin{align*}
  \chi^2(\vect{a})
  &= \sum_n\left(\frac{f(x_n, \vect{a}) - y_n}{\sigma_n}\right)^2\\
  &= \delta\vect{a}^T\left(\sum_n\frac{\vect{J}^T_n\vect{J}_n
                           - \mat{H}_n e_n}{\sigma_n^2}\right)\delta\vect{a} + \\
  &\qquad - 2\sum_n\frac{e_n\vect{J}_n^T}{\sigma_n^2}\cdot\delta\vect{a}
  + \sum_n\frac{e_n^2}{\sigma_n^2}
  + \order(\delta\vect{a}^3).
\end{align*}

Consider taking many measurements and averaging.  Each measurement will give data
$\{(x_n, y_n)\}$ with a different realization of the errors $e_n$ sampled from whatever
distribution is relevant for the experiment.  The resulting $\chi^2$ will thus have the
following distribution
The


\begin{gather*}
  \begin{aligned}
    \braket{\chi^2(\vect{a})}
    &= \left\langle\sum_n\left(\frac{f(x_n, \vect{a}) - y_n}{\sigma_n}\right)^2\right\rangle\\
    &= \delta\vect{a}^T\left(\sum_n\frac{\vect{J}^T_n\vect{J}_n}{\sigma_n^2}\right)\delta\vect{a}
  + \left(2\sum_n\frac{\braket{e_n}\vect{J}_n}{\sigma_n^2}\right)\cdot\delta\vect{a}
  + \sum_n\frac{\braket{e_n^2}}{\sigma_n^2},
  \end{aligned}\\
  y_n = f(x_n, \bar{\vect{a}}) + e_n, \\
  f(x_n, \vect{a}) = f(x_n, \bar{\vect{a}}) + \mat{J}_n\cdot\delta\vect{a} + \order(\delta\vect{a}^2),\\
\end{gather*}






for some

In the previous section, we computed the best fit parameters $\bar{\vect{a}}$, and estimated the
covariance matrix $\mat{C}$.


From the `least_squares` and `minimize` models, we see that $\chi^2_r$
depends on the parameters as:

\begin{gather*}
  \chi^2_r(\vect{a}) = \chi^2_r(\bar{\vect{a}})
  + \frac{1}{2} \delta\vect{a}^T
    \cdot \overbrace{\frac{\mat{C^{-1}}}{\nu/2}}^{\mat{H}}
    \cdot \delta\vect{a}
  + \order(\delta\vect{a}^2), \qquad
  \delta\vect{a} = \vect{a} - \bar{\vect{a}}.
\end{gather*}

\begin{gather*}
  \ln P(\vect{a}) \approx
\end{gather*}

+++

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

## Extensions

One can extend this discussion in several ways.  For example:

1. What happens if the errors depend on the parameters?

   \begin{gather*}
     y_n = f(x_n; \vect{a}) + e_n(x_n; \vect{a})
   \end{gather*}

2. What about if the model gives a relationship between $x_n$ and $y_n$, but that each
   has its own errors?

   \begin{gather*}
     y_n - e^{(y)}_n = f(x_n - e^{(x)}_n; \vect{a}).
   \end{gather*}

   This is discussed in [section 15.3](https://nr304ob.s3.amazonaws.com/GOH252ZDG0UO8GXM.pdf#page=1) of {cite:p}`PTVF:2007`.

+++

## References

* [Samples, samples,
  everywhere...](http://mattpitkin.github.io/samplers-demo/pages/samplers-samplers-everywhere/):
  A nice overview of different MCMC software accessible with python.
