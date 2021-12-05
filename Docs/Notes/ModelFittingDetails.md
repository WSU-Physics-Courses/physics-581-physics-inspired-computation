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

(model-fitting-details)=
# Model Fitting Details

Recall that, to fit a model $y = f(x, \vect{a})$ that depends on $M$ parameters
$\vect{a}$ to a collection of measurements $\vect{y} = f(\vect{x}, \vect{a}) +
\vect{e}$ where the errors $e_{n}$ are random variables with overall PDF
$p_e(\vect{e})$, [Bayes' theorem] says:

\begin{gather*}
  p(\vect{a}|\vect{y}) = \frac{\mathcal{L}(\vect{a}|\vect{y})p(\vect{a})}{p(\vect{y})}
\end{gather*}

where the likelihood function is:

\begin{gather*}
  \mathcal{L}(\vect{a}|\vect{y}) = p(\vect{y}|\vect{a}) 
  = p_e\bigr(\vect{y} - f(\vect{x}, \vect{a})\bigr).
\end{gather*}

:::{admonition} Least Squares

The familiar procedures of least-squares accomplishes these goals as follows.  First 

minimizing $\chi^2$ express this in terms of a best-fit set of
   parameters $\bar{\vect{a}}$ and a local characterization of the maximum as a
   quadratic form expressed in terms of a covariance matrix $\mat{C}$.

However, to do this properly requires
   knowing the posterior over the full integration range (not just near the maximum),
   and generally results in nasty functions that cannot be done analytically.
   The one case in which everything has simple analytic results is if the final
   distribution is gaussian, but this only generically happens if both the errors and
   priors are gaussian **and** the model is linear.  If the errors are small, then a
   linear approximation to the model may be sufficient, and 

:::

:::{admonition} Goals of Model Fitting
The model-fitting goals discussed at the end of [section
15.0.0](https://nr304ob.s3.amazonaws.com/FW4FNZ819A0CL5ON.pdf#page=2) of
{cite:p}`PTVF:2007` can be expressed as

1. "Best fit" parameters maximize the posterior $p(a|\vect{y})$.  If the
   prior doesn't depend on $a$ (e.g. flat), then this is a [maximum likelihood
   estimation].
2. Uncertainties are characterized by the shape of the posterior $p(a|\vect{y})$.
3. Goodness-of-fit can be expressed through the [model evidence] $p(\vect{y})$,
   which balances likelihood with model complexity but the
   issue is more complicated: see, for example, [this discussion on stack
   overflow](https://stats.stackexchange.com/a/70208).
:::


## Independently Distributed Errors

The most common formulation follows from considering flat priors ($p(\vect{a})$ is
independent of $\vect{a}$) and errors that are independently
distributed with a common probability distribution $N(x)$ where $x = e_n/\sigma_n$:

\begin{gather*}
  p_n(e_n) = \frac{N(e_n/\sigma_n)}{\sigma_n}, \qquad
  p_e(\vect{e}) = \prod_{n=1}^{N} \frac{1}{\sigma_n}N\left(\frac{e_n}{\sigma_n}\right).
\end{gather*}

I.e., the probability of simultaneously realizing all of the errors $\vect{e}$ is the
probability of realizing $e_0$, and $e_1$, and $e_2$, etc.

:::{margin}

The distributions in {py:mod}`scipy.stats` are generally characterized by a
*location* (`loc`) and a *scale* (`scale`).  These are the mean and standard deviation
for a normal distribution ({py:data}`scipy.stats.norm`) and have default values `loc=0`
and `scale=1`.  Thus, the distribution $N(x)$ here could be thought to represent the
default of many of the distributions presented there.

:::

The most common case is that of errors distributed normally with zero mean and standard
deviation $\sigma_n$:

\begin{gather*}
  N(x) = \frac{e^{-x^2/2}}{\sqrt{2\pi}}, \qquad
  p_n(e_n) = \frac{e^{-e_n^2/2/\sigma_n^2}}{\sqrt{2\pi \sigma_n^2}} 
           = \frac{N(e_n/\sigma_n)}{\sigma_n},
\end{gather*}

but we can consider any distribution $N(x)$.

:::{margin}
Since $\ln$ is monotonically increasing, maximizing
$\mathcal{L}$  is equivalent to minimizing the negative
log $-\ln \mathcal{L}$, which we express in terms of the negative log of
$\rho(x) = -\ln N(x)$.

:::

Maximizing the posterior $p(\vect{a}|\vect{y})$ is then equivalent to maximizing the
likelihood, which we express as minimizing the following **objective function** $F(\vect{a})$:

\begin{gather*}
  N(x) = e^{-\rho(x)}, \qquad
  \min_{\vect{a}} \underbrace{\sum_n \rho\Biggl(
    \frac{\overbrace{y_n - f(x_n, \vect{a})}^{e_n}}{\sigma_n}
  \Biggr)}_{F(\vect{a}) = -\ln \mathcal{L}(\vect{a}|\vect{y}) + \sum_n\ln \sigma_n}.
\end{gather*}

At the minimum $\bar{\vect{a}}$, the objective function has zero gradient, and hence is
approximately quadratic, described by the [Hessian matrix] $\mat{H}$:

\begin{gather*}
  F(\vect{a}) \approx \overbrace{F(\bar{\vect{a}})}^{F_0}
  + \frac{(\vect{a} - \bar{\vect{a}})^T
    \cdot \mat{H}
    \cdot(\vect{a} - \bar{\vect{a}})}{2}, 
  \qquad
  [\mat{H}]_{ij} = \left.
  \frac{\partial^2 F(\vect{a})}{\partial a_i \partial
  a_j}\right|_{\vect{a} = \bar{\vect{a}}}.
\end{gather*}

If the errors are normal (gaussian), then $\rho(x) = -\ln N(x) = x^2/2$, and we recover
the familiar approach of minimizing $\chi^2$, the sum of the square of the residuals: 

\begin{gather*}
  F(\vect{a}) = \frac{\chi^2(\vect{a})}{2}
  =
  \sum_n \rho\Biggl(
    \frac{y_n - f(x_n, \vect{a})}{\sigma_n}
  \Biggr)
  =
  \frac{1}{2}\sum_n \Biggl(
    \frac{y_n - f(x_n, \vect{a})}{\sigma_n}
  \Biggr)^2. 
\end{gather*}

:::{margin}
Note that the
normalization factors contains the $\chi^2_0$ as a goodness-of-fit measure, but it is not
completely trivial to extract:

\begin{align*}
  &\int e^{-F(\vect{a})}\d^{k}{\vect{a}}\\
  &\approx \frac{e^{-F_0}}{\sqrt{\det(2\pi \mat{C})}}\\
  &= \frac{e^{-\chi^2_0/2}}{\sqrt{\det(2\pi \mat{C})}},\\
  &\int \mathcal{L}(\vect{a}|\vect{y}) \d^{k}\vect{a}\\
  &\approx
  (\textstyle\prod_n \sigma_n)
  \int e^{-F(\vect{a})}\d^{k}{\vect{a}}\\
  &= \frac{(\textstyle\prod_n \sigma_n) e^{-\chi^2_0/2}}{\sqrt{\det(2\pi \mat{C})}}.
\end{align*}
:::

In this case, the [Hessian matrix] $\mat{H} = \mat{C}^{-1} = \mat{\Sigma}^{-1}$ is
exactly the inverse of the [covariance matrix] $\mat{C}$, and the posterior distribution
is approximately a [multivariate normal distribution] with mean $\bar{\vect{a}}$ and
covariance matrix $\mat{C} = \mat{\Sigma} = \mat{H}^{-1}$ after normalizing

\begin{align*}
  p(\vect{a}|\vect{y}) &\propto 
  \mathcal{L}(\vect{a}|\vect{y})
  \propto e^{-F(\vect{a})}
  \propto e^{-(\vect{a} - \bar{\vect{a}})^T \cdot \mat{C}^{-1}
    \cdot (\vect{a} - \bar{\vect{a}})/2},\\
  p(\vect{a}|\vect{y}) &=
  \frac{\mathcal{L}(\vect{a}|\vect{y})}
       {\int\mathcal{L}(\vect{a}|\vect{y})\d^{k}{\vect{a}}}
  =
  \frac{e^{-F(\vect{a})}}{\int e^{-F(\vect{a})}\d^{k}{\vect{a}}}\\
  &\approx
  \frac{
    \exp\Bigl(
      -\frac{1}{2}
      (\vect{a} - \bar{\vect{a}})^T
      \cdot\mat{C}^{-1}
      \cdot(\vect{a} - \bar{\vect{a}})
    \Bigr)
  }{
    \sqrt{\det{(2\pi\mat{C})}}
  }
\end{align*}

where there are $M$ parameters $\vect{a} = (a_0, a_1, \dots, a_{M-1})$.

::::{admonition} Poisson Distribution (Incomplete)
:class: dropdown

**Poisson Distribution (Incomplete)**

As another example, supposed your data $y_n$ comes from counting (e.g. photons on a
detector).  In this case, the errors are probably more appropriately described by a
[Poisson distribution].  For example, supposed we have a photo-detector that measures
photons at a location $x$ with spatial probability distribution $n(x) =
\abs{\psi(x)}^2$ which is some wavefunction that we want to model.  
The detectors will count photons at some rate average rate $r = \alpha n(x)\d{x}$ where
$\d{x}$ is the pixel size and $\alpha$ is some capture rate (photons per unit time)
which is a property of the detector.  If the detector is on for time $t$, then the
average number of photons measured at $x$ will be $\lambda = rt$ and our data point will
be $y = n(x) = rt/\alpha t \d{x}$.  

The probability of measuring $k$ photons in the time $t$ is:

\begin{gather*}
  p(k) = \frac{\lambda^{k}e^{-\lambda}}{k!}.
\end{gather*}

::::

## Parameter Uncertainties (Covariance)

A complete characterization of the posterior $p(\vect{a}|\vect{y})$ is usually provided
through a large set of sample data $\{\vect{a}_n\}$ sampled with the appropriate
probability from this distribution.  The goal of methods like Markov chain Monte
Carlo ([MCMC]) is to generate such a distribution.

Alternatively, the posterior might be known analytically.  This is the case if both the
prior and likelihood are [multivariate normal distribution]s (i.e. if the model is linear
and the errors are normally distributed):

\begin{gather*}
  p(\vect{a}|\vect{y}) = \frac{1}{\sqrt{\det{(2\pi\mat{C})}}}\exp\Bigl(
    -\frac{1}{2}
    (\vect{a} - \bar{\vect{a}})^T
    \cdot\mat{C}^{-1}
    \cdot(\vect{a} - \bar{\vect{a}})
  \Bigr).
\end{gather*}


:::{sidebar} Warning: [Marginal Distributions]

Even a complete collection of [marginal distributions] do not completely characterize a
given multivariate distribution.  This idea is demonstrated through the
[Datasaurus Dozen] or [Anscombosaurus] which demonstrate how different distributions can
have the same statistics:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Always visualize your data! (Thanks to <a href="https://twitter.com/AlbertoCairo?ref_src=twsrc%5Etfw">@albertocairo</a> for the artwork 😀) <a href="https://t.co/8D8sgLLqB5">pic.twitter.com/8D8sgLLqB5</a></p>&mdash; Justin Matejka (@JustinMatejka) <a href="https://twitter.com/JustinMatejka/status/770682771656368128?ref_src=twsrc%5Etfw">August 30, 2016</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Topological data analysis provides an interesting set of tools for discovering patterns
in data.  If you are interested in this, see [Math 529: Intro. to Computational
Topology](http://www.math.wsu.edu/faculty/bkrishna/Math529.html) (offered Spring 2022,
Tue+Thu 10:35-11:50 AM) taught by Bala Krishnamoorthy:

<iframe width="100%" src="https://www.youtube.com/embed/1FLZTIQoVU8"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen></iframe>

[datasaurus dozen]: <https://www.autodesk.com/research/publications/same-stats-different-graphs>
[Anscombosaurus]: <https://twitter.com/maartenzam/status/770723795518812160>
:::

### Marginal Distributions

Once one obtains the posterior distribution $p(\vect{a}|\vect{y})$, one needs to
communicate this.  The first thing one might do is to look at the uniform [probability distribution]
for each parameter:

\begin{gather*}
    p_{i}(a_i|\vect{y}) = \int p(\vect{a}|\vect{y}) \prod_{k\neq i} \d{a_k}.
\end{gather*}

This gives us an idea about how the parameter $a_{i}$ is distributed.  In particular,
one can plot these distributions using a histogram, or one can present numerical values
of various statistical features like:
* the [mean], [median], or [mode], which act as a description of the "best fit"
  parameter values;
* the [standard deviation], which acts as a description of the uncertanties; and
* the [skewness], [kurtosis], etc. which characterize how different the distribution is
  from a [normal distrbution] (along with the differences between the [mean], [median], and [mode]).

Pairwise distributions

\begin{gather*}
  p_{ij}(a_i, a_j|\vect{y}) = \int p(\vect{a}|\vect{y}) \prod_{k\neq i,j} \d{a_k}.
\end{gather*}

can also be easily visualized through a **corner plot** plot.

#### The Gaussian Case

If your posterior is well approximated by a [multivariate normal distribution], then one
can analytically compute the marginal distributions.  The result is simply obtained by
taking the appropriate columns and rows of the covariance matrix $\mat{C}$:

\begin{align*}
  p_{i}(a_i|\vect{y}) &= 
  \frac{1}{\sqrt{2\pi C_{ii}}}\exp\Bigl(
    -\frac{(a_i - \bar{a}_i)^2}{2C_{ii}}
  \Bigr), \\
  p_{ij}(a_i, a_j|\vect{y})&=
  \frac{1}{\sqrt{\det{(2\pi\mat{C}_{ij})}}}\exp\Bigl(
    -\frac{1}{2}
    \begin{pmatrix}
      a_{i}-\bar{a}_{i} & a_{j} - \bar{a}_{j}
    \end{pmatrix}
    \cdot\mat{C}_{ij}^{-1}
    \cdot
    \begin{pmatrix}
      a_{i}-\bar{a}_{i}\\
      a_{j} - \bar{a}_{j}
    \end{pmatrix}
  \Bigr), \\
  &\mat{C}_{ij} = \begin{pmatrix}
    C_{ii} & C_{ij}\\
    C_{ji} & C_{jj}
  \end{pmatrix}.
\end{align*}

This generalizes to any set of parameters, but see the note below about how to interpret
these regions.

(confidence-levels)=
## Confidence Levels

When considering a marginal distribution of $\nu$ variables constructed this way, you
should determine your confidence region by using the corresponding $\chi^2$ distribution
with $\nu$ degrees of freedom $P_{\chi^2, \nu}(\chi^2)$.  Specifically, to find the
confidence regions containing fraction $p$ of the total samples over $\nu$ variables,
you should consider the region

\begin{gather*}
  \delta \vect{a}^T\mat{C}^{-1}\delta \vect{a} \leq \chi^2_p, \qquad
  \int_0^{\chi^2_p}\d{\chi^2}\; P_{\nu,\chi^2}(\chi^2) = p
\end{gather*}

:::{margin}
The relationship between $p_{n\sigma}$ and $n\sigma$ comes from the standard gaussian
distribution of a single variable with zero mean and unit norm:

\begin{gather*}
  p_{n\sigma} = \int_{-n}^{n}\!\!\d{x}\; \frac{e^{-x^2/2}}{\sqrt{2\pi}} \\
  = \int_{-n\sigma}^{n\sigma}\!\!\d{x}\; \frac{e^{-x^2/2\sigma^2}}{\sqrt{2\pi\sigma^2}}.
\end{gather*}
:::

with $p_{1\sigma}=68.27\%$ for the $1\sigma$ confidence level, $p_{2\sigma}=84.27\%$,
$p_{3\sigma} = 91.67\%$, $p_{4\sigma} = 95.45\%$, etc.

The value $\chi^2_p$ can be computed with the {py:meth}`scipy.stats.rv_continuous.ppf`
method of the {py:data}`scipy.stats.chi2` distribution.  For $\nu=1$ we have simply
$\chi^2_p = n$ for the $n\sigma$ confidence level, but this differs for $\nu > 1$.  See
{ref}`confidence-regions` for details.

:::{important}

There are several important caveats here:

1. This only makes sense if your model is a good fit (i.e. $Q > 0.001$).  If your model
   is not good, you can pretend like you do not know the distribution of your errors,
   and scale the uncertainties by an overall factor to make $\chi^2_r = 1$.  This
   corresponds to scaling:
   
   \begin{gather}
     \sigma_n \rightarrow \sigma_n \sqrt{\chi^2_r}, \qquad
     \mat{C} \rightarrow \chi^2_r\mat{C}.
   \end{gather}

   Another option: if your experimental errors are *independent and identically
   distributed* (*iid*), you can use the *bootstrap method* discussed in section 15.6.2
   of {cite:p}`PTVF:2007` to use the data itself to estimate the errors.

2. If your distribution is not gaussian, then the relationship between the contours
   $\chi^2_p$ and the confidence level $p$ will likely not be given by the chi square
   distribution $P_{\chi^2, \nu}(\chi^2)$.  If the errors are small, one can still use this
   approach as the posterior distribution will still be approximately quadratic close to
   the maximum at $\vect{a} = \bar{\vect{a}}$:

   \begin{gather*}
     -2\ln \frac{p(\vect{a}|\vect{y})}{p(\bar{\vect{a}}|\vect{y})} 
     \approx 
     \delta\vect{a}^T
     \mat{C}^{-1}
     \delta\vect{a}, \qquad
     \delta \vect{a}^T\mat{C}^{-1}\delta \vect{a} \leq \chi^2_p.
   \end{gather*}

   Hence, one can still approximate the confidence region from the levels of constant
   $\chi^2_p$, but the relationship between this and $p$ must now be determined by a simple
   Monte Carlo calculation as discussed in section 15.6.1 of {cite:p}`PTVF:2007`.

3. If you want to explore a smaller set of $\tilde{\nu} < \nu$ parameters, you can
   integrate the posterior distribution over the $\nu - \tilde{\nu}$ "nuisance"
   parameters by just keeping the corresponding rows and columns of $\mat{C}$ in a new
   smaller matrix $\tilde{\mat{C}}$ as discussed above for the cases $\tilde{nu} = 1$
   and $\tilde{nu} = 2$.  This corresponds to minimizing over the nuisance
   parameters. Note: do not extract the rows and columns of $\mat{C}^{-1}$ which would
   correspond to holding the nuisance parameters fixed, which is almost certainly not
   what you want to do.
   
   Once you have done this, you can explore the contour in this marginal
   distribution corresponding to 
   
   \begin{gather*}
     \Delta \tilde{\chi}^2(\tilde{\vect{a}})
     \approx 
     \delta\tilde{\vect{a}}^T
     \tilde{\mat{C}}^{-1}
     \delta\tilde{\vect{a}} < \chi^2_{p}
   \end{gather*}
   
   where you must determine $\chi^2_{p}$ from the inverse (CDF) for the chi squared
   distribution with $\tilde{\nu}$ degrees of freedom if your posterior is gaussian, or
   using Monte Carlo.
:::



(geometry-of-fitting)=
## The Geometry of Data Fitting

Data fitting can be visualized geometrically as follows.  Consider $N$ data points
$\vect{y} = (y_{0}, y_{1}, \dots, y_{N-1})$ as a vector $\vect{y} \in \mathbb{R}^{N}$.
A model with $M$ parameters $\vect{a}$ can now be though of as an $M$-dimensional
surface in $\mathbb{R}^{N}$ as defined by the set of points $\vect{f}(\vect{a})$.

### Example: Three Points

The geometry of fitting a two-parameter curve $y_n = f(x_n, \vect{a})$ to three data points
$\vect{y}$ can be visualized in 3D.  Here we demonstrate two models, one linear, and
another exponential.

\begin{gather*}
  \vect{y}_{\text{linear}} = a_0 \vect{x} + a_1, \qquad
  \vect{y}_{\text{exponential}} = a_0 e^{a_1\vect{x}}
\end{gather*}

The linear model (middle green) gives a plane in the 3D space of points $\vect{y}$,
while the exponential model (right, red) gives a curved surface with a singular point
where $a_0=0$.  The data $\vect{y}$ is the orange point.  The best-fit problem reduces
to finding the point on these surfaces which is closest to the data in terms of of the
$L_2$ norm $\norm{\vect{y}}_2 \sqrt{\chi^2}$.  These solutions ate noted by black
crosses.  In this picture, the vector from the best fit point to the data (orange line)
is normal to the surface.

```{code-cell} ipython3
:tags: [hide-input, full-width]

from myst_nb import glue

from scipy.optimize import curve_fit

from matplotlib.gridspec import GridSpec

plt.close('all')
rng = np.random.default_rng(seed=0)
y = np.asarray([2, 1, 3])
x = np.asarray([-1, 0, 1])

Na = 10
Nb = 12

x_, a_, b_ = np.meshgrid(
    x,
    np.linspace(-0.3, 3, Na),
    np.linspace(-0.3, 0.7, Nb),
    indexing='ij', 
    sparse=True)

def f1(x, a0, a1):
    return a0 + a1*x

def f2(x, a0, a1):
    return a0*np.exp(a1*x)
    
f1_ = f1(x_, a_, b_)
f2_ = f2(x_, a_, b_)
a1, C1 = curve_fit(f1, x, y)
a2, C2 = curve_fit(f2, x, y, p0=[0, 3.5])

cs = ['C1', 'C2', 'C3']

fig = plt.figure(figsize=(12, 5))
gs = GridSpec(1, 3, figure=fig, width_ratios=(1, 2, 2))

axs = [fig.add_subplot(gs[0]), 
       fig.add_subplot(gs[1], projection='3d'),
       fig.add_subplot(gs[2], projection='3d')]

_x = np.linspace(-1, 1)

ax = axs[0]
ax.plot(x, y, 'o', c=cs[0])
ax.plot(x, f1(x, *a1), 'xk')
ax.plot(x, f2(x, *a2), 'xk')
ax.plot(_x, f1(_x, *a1), '-', c=cs[1])
ax.plot(_x, f2(_x, *a2), '--', c=cs[2])

axs[1].plot_surface(*f1_, color=cs[1])
axs[2].plot_surface(*f2_, color=cs[2])

axs[1].set(title=r"$\mathbf{y} = a_0 \mathbf{x} + a_1$")
axs[2].set(title=r"$\mathbf{y} = a_0 e^{a_1\mathbf{x}}$")

ax = axs[0]
ax.grid(True)
ax.set(xlabel='$x$', ylabel='$y$', aspect=1)

for f, a, f_, ax in zip((f1, f2), (a1, a2), (f1_, f2_), axs[1:]):
    y_ = f(x, *a)
    ax.plot(*y_, 'x', c='k', alpha=1.0, zorder=100)
    ax.plot(*y, 'o', c=cs[0], alpha=1.0, zorder=100)
    ax.plot([y_[0], y[0]], [y_[1], y[1]], [y_[2], y[2]], ls='-', c=cs[0], alpha=1.0, zorder=100)
    ax.set(xlabel='$y_0$', ylabel='$y_1$', zlabel='$y_2$')
    ax.view_init(elev=2, azim=-80)
    # Make the aspect ratio 1,1,1: see https://stackoverflow.com/a/64487277/1088938
    ax.set_box_aspect(np.ptp(f_, axis=(1,2)))

plt.tight_layout()
```

The geometry is the same with other norms, but the notion of distance and angles can
change.  This same picture can be used with unequal errors by first scaling the data and
functions $y_n \rightarrow y_n/\sigma_n$, $f(x, \vect{a}) \rightarrow f(x,\vect{a})/\sigma(x_n)$ where $\sigma(x_n) = \sigma_n$ is an appropriate function.  These
factors of $\sigma_n$ can also just be absorbed into a redefined metric.



## Complete Example
Here we work through a complete example of a single parameter model $y_n = a + e_n$ with
independent gaussian error distributions $p_n(e_n)$ with zero mean (unbiased) and
variance $\sigma_n^2$.  This simplifies things, because the product of gaussian
distributions is gaussian:

\begin{gather*}
  \exp\left(-\frac{(x-\mu_1)^2}{2\sigma_1^2}\right)
  \exp\left(-\frac{(x-\mu_2)^2}{2\sigma_2^2}\right)
  \propto
  \exp\left(-\frac{(x - \mu_{12})^2}{2\sigma_{12}^2}\right)\\
  \mu_{12} = \frac{\sigma_2^2\mu_1 + \sigma_1^2\mu_2}{\sigma_1^2 + \sigma_2^2}, \qquad
  \frac{1}{\sigma_{12}^2} = \frac{1}{\sigma_1^2} + \frac{1}{\sigma_2^2}
\end{gather*}

We start with gaussian prior $p(a)$ with mean $a_p$ and variance $\sigma_p^2$.  After a
measurement with value $y_0$, our posterior is:

\begin{gather*}
  p(a|y_0) \propto p_0(y_0 - a)p(a) \propto 
\end{gather*}



, after several measurements
$y_0$, $y_1$, and $y_2$, we have posteriors

\begin{align*}
  p(a|y_0) &\propto p_0(y_0 - a)p(a),\\
  p(a|y_0,y_1) &\propto p_1(y_0 - a)p(a|y_0) 
  \propto p_1(y_1 - a)p_0(y_0 - a)p(a), \\
  p(a|y_0,y_1,y_2) &\propto p_2(y_2-a)p_1(y_1 - a)p_0(y_0 - a)p(a).
\end{align*}

Note that the order in which we include the measurements makes no difference, as
expected from the final form $p(a|\vect{y}) \propto p_e(\vect{y}-\vect{e})p(a)$.

Consider a single measurement, but now with two error estimates $p_0(e_0)$ and an
underestimated error $\tilde{p}_0(e_0) = \lambda p_0(\lambda e_0)$

\begin{gather*}
    p(a|y_0) = \frac{p_0(y_0 - a)p(a)}{\int p_0(y_0 - a)p(a)\d{a}}\\
    \tilde{p}(a|y_0) = \frac{\tilde{p}_0(y_0 - a)p(a)}{\int \tilde{p}_0(y_0 - a)p(a)\d{a}}
    = \frac{p_0(\lambda y_0 - \lambda a)p(a)}{\int p_0(\lambda y_0 -
    \lambda a)p(a)\d{a}}.
\end{gather*}

These are **not** the same.  Consider a flat prior and normally distributed errors with
correct $\sigma$ and incorrect $\tilde{\sigma} = \sigma / \lambda$:

\begin{gather*}
  p(a|y_0) = \frac{}{}e^{-(y_0-a)^2/2\sigma^2}
\end{gather*}




[chi-squared distribution]: <https://en.wikipedia.org/wiki/Chi-squared_distribution>
[sum or normally distributed random variables]: <https://en.wikipedia.org/wiki/Sum_of_normally_distributed_random_variables>
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
[likelihood function]: <https://en.wikipedia.org/wiki/Likelihood_function>
[Bayesian inference]: <https://en.wikipedia.org/wiki/Bayesian_inference>
[Bayes' theorem]: <https://en.wikipedia.org/wiki/Bayes%27_theorem>
[model evidence]: <https://en.wikipedia.org/wiki/Marginal_likelihood>
[maximum likelihood estimation]: <https://en.wikipedia.org/wiki/Maximum_likelihood_estimation>
[Poisson distribution]: <https://en.wikipedia.org/wiki/Poisson_distribution>
[mean]: <https://en.wikipedia.org/wiki/Expected_value>
[median]: <https://en.wikipedia.org/wiki/Median>
[mode]: <https://en.wikipedia.org/wiki/Mode_(statistics)>
[standard deviation]: <https://en.wikipedia.org/wiki/Standard_deviation>
[probability distribution]: <https://en.wikipedia.org/wiki/Probability_distribution>
[skewness]: <https://en.wikipedia.org/wiki/Skewness>
[kurtosis]: <https://en.wikipedia.org/wiki/Kurtosis>
[marginal distributions]: <https://en.wikipedia.org/wiki/Marginal_distribution>

[MCMC]: <https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo>
[Hessian matrix]: <https://en.wikipedia.org/wiki/Hessian_matrix>
