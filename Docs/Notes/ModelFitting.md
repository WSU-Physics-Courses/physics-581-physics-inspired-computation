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
The goals of model fitting as discussed at the end of [section
15.0.0](https://nr304ob.s3.amazonaws.com/FW4FNZ819A0CL5ON.pdf#page=2) of
{cite:p}`PTVF:2007` can be expressed as

1. Determine the "best fit" parameters. I.e. maximize the $p(a|\vect{y})$.  If the prior
   does not depend on $a$ (e.g. if it is flat), then this is equivalent to [maximum
   likelihood estimation] which implicitly chooses such a prior.
2. Characterize the uncertainties.  This is done by looking at the shape of the
   distribution.
3. Provide a measure of the goodness-of-fit.  The [model evidence] $p(\vect{y})$
   provides a way of doing this which balances likelihood with model complexity but the
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



Generally, we assume that the errors $e_n$ are independent, with PDF $p_n(e_n)$, in
which case $p_e(\vect{e}) = p_1(e_1)p_2(e_2)\dots p_N(e_N))$:

\begin{gather*}
  \mathcal{L}(a|\vect{y}) = p(\vect{y}|a) = p_e(\overbrace{\vect{y}-a}^{\vect{e}}).
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
