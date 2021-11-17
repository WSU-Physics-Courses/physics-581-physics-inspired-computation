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

:::{sidebar} Model Fitting
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

## Curve Fitting

Expanding on this, consider a model $y = f(x, \vect{a})$ depending on several parameters
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

## Identically Independently Distributed (idd) Errors

The most common formulation follows from considering flat priors ($p(\vect{a})$ is
independent of $\vect{a}$) and errors that are identically and independently
distributed (iid) with a common probability distribution $N(x)$ where $x =
e_n/\sigma_n$:

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
likelihood, which we express as minimizing the following **objective function**:

\begin{gather*}
  N(x) = e^{-\rho(x)}, \qquad
  \min_{\vect{a}} \underbrace{\sum_n \rho\Biggl(
    \frac{\overbrace{y_n - f(x_n, \vect{a})}^{e_n}}{\sigma_n}
  \Biggr)}_{-\ln \mathcal{L}(\vect{a}|\vect{y}) + \sum_n\ln \sigma_n}.
\end{gather*}

If the errors are normal (gaussian), then $\rho(x) = -\ln N(x) = x^2/2$, and we recover
the familiar approach of minimizing $\chi^2$, the sum of the square of the residuals: 

\begin{gather*}
  \frac{\chi^2}{2}
  =
  \sum_n \rho\Biggl(
    \frac{y_n - f(x_n, \vect{a})}{\sigma_n}
  \Biggr)
  =
  \frac{1}{2}\sum_n \Biggl(
    \frac{y_n - f(x_n, \vect{a}}{\sigma_n}
  \Biggr)^2. 
\end{gather*}

### Poisson Distribution (Incomplete)

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
