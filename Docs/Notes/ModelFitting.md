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

A complete characterization of the posterior $p(\vect{a}:\vect{y})$ is usually provided
through a large set of sample data $\{\vect{a}_n\}$ sampled with the appropriate
probability from this distribution.  The goal of methods like Markov chain Monte
Carlo ([MCMC]) is to generate such a distribution.

Alternatively, the posterior might be known analytically.  This is the case if both the
prior and likelihood are [multivariate normal distribution]s (i.e. if the model is linear
and the errors are normally distributed):

\begin{gather*}
  p(\vect{a}|\vect{y}) = \frac{1}{\sqrt{\det{(2\pi\mat{\Sigma})}}}\exp\Bigl(
    -\frac{1}{2}
    (\vect{a} - \bar{\vect{a}})^T
    \cdot\mat{\Sigma^{-1}}
    \cdot(\vect{a} - \bar{\vect{a}})
  \Bigr)
\end{gather*}




:::{sidebar} Warning: [Marginal Distributions}

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



https://en.wikipedia.org/wiki/Statistical_significance



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
