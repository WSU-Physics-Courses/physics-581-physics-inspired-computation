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

# Model Fitting

## Single Value

Consider an experiment designed to measures a value $a$.  Suppose that the experiment is
performed $N$ times, finding results

\begin{gather*}
  y_n = a + e_n
\end{gather*}

where $e_n$ is a random variable (see {ref}`random_variables`).  What do we learn about
the parameter $a$ from these experiments $\vect{y} = (y_1, y_2, \dots, y_{N})$?  Key
to this is the [likelihood function] $\mathcal{L}(a|\vect{y}) = p(\vect{y}|a)$ which is
the probability or likelihood of obtaining the data $\vect{y}$ if the actual parameter
value were $a$.

:::{margin}
We simply solve for $\vect{e}$ here and insert it into $p_e(\vect{e})$.
:::
In its full glory, if the errors are distributed according to the probability
distribution function (PDF) $p_e(\vect{e})$, then

\begin{gather*}
  \mathcal{L}(a|\vect{y}) = p(\vect{y}|a) = p_e(\overbrace{\vect{y}-a}^{\vect{e}}).
\end{gather*}

Note that this **is not** a probability distribution for the parameter $a$.  To obtain such
a distribution, called the **posterior distribution**, we must use [Bayes' theorem], and
assume some **prior distribution** $p(a)$ for $a$ representing our prior knowledge about
$a$:

\begin{gather*}
  p(a|\vect{y}) = \frac{\mathcal{L}(a|\vect{y})p(a)}{p(\vect{y})}
\end{gather*}

:::{margin}
The **model evidence** is also called the **marginal likelihood**.
:::
The denominator $p(\vect{y})$ is here is the **[model evidence]** and is generally
regarded simply as a normalization factor to ensure that $\int p(a|\vect{y}) \d{a} =
1$.

This is what we can learn about the true value of $a$ from the measurements.  The
resulting posterior distribution combines our prior knowledge -- what we know about $a$ before the
experiment -- with the experimental results, and normalizes these.  All of what follows
in model fitting comes from this result, using various approximations, or simplifications.

## Curve Fitting

Expanding on this, consider a model $y = f(x, \vect{a})$ depending on $M$ parameters
$\vect{a}$, and a collection of measurements $\vect{y} = f(\vect{x}, \vect{a}) +
\vect{e}$ where again $e_{n}$ are random variables with overall PDF $p_e(\vect{e})$.
[Bayes' theorem] says the same thing:

\begin{gather*}
  p(\vect{a}|\vect{y}) = \frac{\mathcal{L}(\vect{a}|\vect{y})p(\vect{a})}{p(\vect{y})}
\end{gather*}

but the likelihood function is *slightly* more complicated

\begin{gather*}
  \mathcal{L}(\vect{a}|\vect{y}) = p(\vect{y}|\vect{a}) 
  = p_e\bigr(\vect{y} - f(\vect{x}, \vect{a})\bigr).
\end{gather*}

## The Main Point

The entire point of model fitting is to determine and characterize the posterior
distribution $p(\vect{a}|\vect{y})$.  In principle, using [Bayes' theorem] is
straightforward -- simply multiply the distributions.  The computational challenges
arise as follows:

1. To explore the posterior, finding, for example, the maximum, and characterizing the
   shape.
2. To **marginalize** over *nuisance parameters* by integrating
   the posterior over these parameters.

In general, these tasks are not feasible analytically, but can be easily performed using
simple (but often slow) Monte Carlo techniques.  One case where analytic solutions are
available is where the posterior is gaussian (a [multivariate normal distribution]):

:::{margin}
To work with such [multivariate normal distribution]s numerically, you can use
{py:data}`scipy.stats.multivariate_normal`.  This has methods like `pdf()` and `cdf()`
which compute the probability distribution function and cumulative distribution function
respectively.
:::

\begin{gather*}
  p(\vect{a}|\vect{y}) = \frac{
    \exp\Bigl(-\frac{1}{2}(\vect{a} - \bar{\vect{a}})^T\cdot
    \mat{C}^{-1}\cdot
    (\vect{a} - \bar{\vect{a}})\Bigr)
  }{\sqrt{\det{(2\pi)\mat{C}}}}.
\end{gather*}

Here $\bar{\vect{a}}$ are the "best-fit" parameters, and $\mat{C}$ is the [covariance
matrix].  This will be the case if the errors $p_e(\vect{e})$ and priors $p(\vect{a})$
are gaussian, and the model $f(\vect{x}, \vect{a}) \approx f(\vect{x}, \bar{\vect{a}}) +
\mat{J}\cdot(\vect{a}-\bar{\vect{a}})$ is sufficiently linear close to the best-fit
value.

:::{margin}
A function like $x^4$ cannot be characterized by a quadratic form, but these cases are
rare.

Since the logarithm is monotonic, it preserves extrema.
:::
In most cases, the posterior is not gaussian.  However, the maximum of *any
generic function* can still be expressed as a quadratic form.  Inspired by the
[multivariate normal distribution], we consider instead the negative logarithm of the
posterior, whose minimum is an exact quadratic form:

\begin{gather*}
  -\ln p(\vect{a}|\vect{y}) + \text{const} 
  \approx 
   \frac{1}{2}
   \overbrace{(\vect{a} - \bar{\vect{a}})^T\cdot
     \mat{C}^{-1}\cdot
     (\vect{a} - \bar{\vect{a}})}^{\Delta\chi^2}.
\end{gather*}

This form is valid for virtually *any* form of posterior, as long as the final result is
sufficiently well constrained.

:::{note}
The quadratic portion denoted $\Delta\chi^2$ by the brace here corresponds to the
change in $\chi^2$ when performing the usual least-squares fitting.  We will discuss
this more below.
:::

:::{margin}
Confidence regions are properly expressed in terms of a percentage $p$, but often
expressed in terms of $n\sigma$ for a gaussian distribution where fraction $p_{n}$
of the probability lies between $\mu \pm n\sigma$ with [mean] $\mu$ and [standard
deviation] $\sigma$.  The relationship can be computed using the CDF of the
normal gaussian distribution:

\begin{align*}
  c(x) &= \int_0^{x}\!\!\!\d{x}\; \frac{e^{-x^2/2}}{\sqrt{2\pi}},\\
  p_{n} &= \int_{-n}^{n}\!\!\!\d{x}\;\frac{e^{-x^2/2}}{\sqrt{2\pi}},\\
        &= c(n) - c(-n).
\end{align*}

| $n\sigma$ | $p_n$    |
|-----------|----------|
| $1\sigma$ | $68.27%$ |
| $2\sigma$ | $95.45%$ |
| $3\sigma$ | $99.73%$ |
| $4\sigma$ | $99.99%$ |

:::
### [Confidence Region]s

If your results are such that this form is valid, then to you can report
$\bar{\vect{a}}$ and $\mat{C}$, but you need one more thing: **confidence regions** --
regions in parameter space that contain a fraction $p$ of the parameters.  These can be
expressed in terms of contours (ellipsoids) of this function:

\begin{gather*}
  \DeclareMathOperator{\CR}{CR}
  \vect{a} \in \CR(p) = \Bigl\{
    \vect{a} \Big| 
    (\vect{a} - \bar{\vect{a}})^T\cdot
     \mat{C}^{-1}\cdot
     (\vect{a} - \bar{\vect{a}}) \leq \Delta \chi^2(p)
     \Bigr\},
\end{gather*}

but we must also express how the contour levels of $\Delta \chi^2(p)$ depend on the
confidence level $p$:

\begin{gather*}
  \int_{\vect{a} \in \CR(p)} p(\vect{a}|\vect{y}) = p.
\end{gather*}

:::{margin}
Numerically $\Delta\chi^2_{\nu}(p)$ can be computed with the `ppf(p)` function of
{py:data}`scipy.stats.chi2`, which gives the inverse of the `cdf()`.
:::
In the Gaussian case, this is the [chi-squared distribution] $P_{\chi^2, \nu}(\chi^2)$
with $\nu$ degrees of freedom corresponding to $\nu$ parameters $\vect{a}$ (see
{ref}`chi-squared-distribution` for details): 

\begin{gather*}
  p = \int_{0}^{\Delta\chi^2(p)}\d{\chi^2}\;P_{\chi^2, \nu}(\chi^2).
\end{gather*}

In general, however, the tails of your posterior distribution will not be gaussian, and
so you will also need to report appropriate contours $\Delta\chi^2(p)$ for your desired
set of confidence levels $p$.

If your posterior is not well approximated by a quadratic over the regions of interest,
then the confidence regions will not be ellipsoids, and you must work harder to
characterize the final distribution.  Markov-chain Monte Carlo [MCMC] is the tool for
this job.

### Marginalization

To marginalize over *nuisance parameters*, one integrates the posterior
$p(\vect{a}|\vect{y})$ over these, leaving the final posterior for the relevant
parameters.  This integration extends over the full parameter range, and so is sensitive
to the tails of the distribution, which may have a different form for different
parameter sets.  For this reason, your may need to quote values for the contours
$\Delta\chi^2(p)$ for *each set of relevant parameters*.

I.e.: even if you provide the confidence level for a set of $N>2$ relevant parameters, to
obtain the pairwise confidence regions, you must still integrate the posterior over the
full range of parameters, so the $\nu=2$ contour $\Delta\chi^2(p)$ may have no simple
relationship to the full $\nu = N$ contour.

:::{margin}
**Exercise:** Prove that this procedure works by computing some gaussian integrals,
either numerically or symbolically.
:::

Again, in the gaussian case, analytic results exist.  Once you determine the posterior
distribution for your complete set of parameters, marginalization is straightforward:

1. If needed, first transform your variables
   
   \begin{gather*}
     \vect{a} \rightarrow \mat{S}\vect{a}, \qquad
     \mat{C} \rightarrow \mat{S}\mat{C}\mat{S}^{T},
   \end{gather*}
   
   so that the nuisance parameters you wish to marginalize over are orthogonal to the
   others.  We will assume this has been done.

2. Simply project $\vect{a}$ and $\mat{C}$ (not $\mat{C}^{-1}$) onto the subspace of
   remaining parameters.  I.e. just keep the appropriate rows and columns of $\mat{C}$
   and the remaining variables.

The contours are again given by the appropriate [chi-squared distribution] $P_{\chi^2,
\nu}(\chi^2)$ where $\nu$ is the number of remaining variables.

```{code-cell} ipython3
:tags: [hide-cell]

import scipy.stats, scipy.integrate
sp = scipy

# Here we numerically check this by comparing the pdf 

N = 3
rng = np.random.default_rng(seed=1)
a = rng.random(size=N) - 0.5
C = rng.random(size=(N, N)) - 0.5
C = C @ C.T

rv1 = sp.stats.multivariate_normal(mean=a, cov=C)
rv2 = sp.stats.multivariate_normal(mean=a[1:], cov=C[1:, :][:, 1:])

# Tests that the PDFs are equivalent at some random points
a2 = rng.random(size=N-1) - 0.5

res, err = sp.integrate.quad(lambda x: rv1.pdf([x] + a2.tolist()),
                             -np.inf, np.inf)
assert err < 1e-8
assert np.allclose(res, rv2.pdf(a2), atol=2*err)

# Print table for margin.
c = sp.stats.norm().cdf
print(r"| $n\sigma$ | $p_n$     |")
print(r"|-----------|-----------|")
for n in range(1, 4):
    print(fr"| ${n}\sigma$ | ${100*(c(n) - c(-n)):.2f}%$ |")
```

## Summary


To fit a model $y=f(x, \vect{a})$ depending on $M$ parameters $\vect{a}$ to a collection
of measurements $\vect{y} = f(\vect{x}, \vect{a}) + \vect{e}$ with errors $\vect{e}$
distributed as $p_e(\vect{e})$ we must characterize the posterior distribution:

\begin{gather*}
  p(\vect{a}|\vect{y}) = \frac{\mathcal{L}(\vect{a}|\vect{y})p(\vect{a})}{p(\vect{y})},
  \qquad
  \mathcal{L}(\vect{a}|\vect{y}) = p(\vect{y}|\vect{a}) 
  = p_e\bigr(\vect{y} - f(\vect{x}, \vect{a})\bigr).
\end{gather*}

If the variance in the parameters is small enough, the posterior will be
well-approximated by a quadratic near its [mode] (maximum).  We use the model

\begin{gather*}
  -2\ln p(\vect{a}|\vect{y}) + \text{const} 
  \approx 
   (\vect{a} - \bar{\vect{a}})^T\cdot
   \mat{C}^{-1}\cdot
   (\vect{a} - \bar{\vect{a}})
   \leq \Delta\chi^2(p)
\end{gather*}

to characterize the confidence regions corresponding to fraction $p$ of the total
distribution.  The best fit parameters $\vect{a}$ which maximize the posterior, the
covariance matrix $\mat{C}$ *and* the appropriate contour levels $\Delta\chi^2(p)$ for
your desired confidence levels $p$ should be reported *for all* sets of relevant
parameters.

If (an only if) your posterior is gaussian, then you may use the standard
[chi-squared distribution] to obtain these contours
$\DeclareMathOperator{\CDF}{CDF}\Delta\chi^2(p) = \CDF^{-1}_{\chi^2,\nu}(p)$ from the
inverse cumulative distribution function for the {ref}`chi-squared-distribution` of
$\nu$ parameters.

For more details see {ref}`model-fitting-details` including a discussion of how this
works when your errors are gaussian, how the Bayesian approach reproduces the standard
least-squares approach with an appropriate choice of likelihood function and prior.

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
