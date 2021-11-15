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

(random_variables)=
# Random Variables

Here we summarize some properties of random variables.  Let $X$, $Y$, etc. be random
variables with probability distribution functions (PDFs) $P_X(x)$, $P_Y(y)$ etc.

:::{admonition} Example: Normal (Gaussian) Distributions

A normally distributed variable with mean $\mu$ and variance $\sigma$ has PDF:

\begin{gather*}
  P_X(x) = \frac{1}{\sqrt{2\pi \sigma}} e^{-(x-\mu)^2/2\sigma^2}.
\end{gather*}

A [multivariate normal distribution] of $N$ variables with mean $\vect{\mu}$ and
covariance matrix $\mat{\Sigma}$ has the following PDF:

\begin{gather*}
  \newcommand{\mat}[1]{\boldsymbol{#1}}
  \newcommand{\vect}[1]{\boldsymbol{#1}}
  P_X(\vect{x}) = \frac{1}{\sqrt{(2\pi)^N\det\mat{\Sigma}}} 
  \exp\left(\frac{
    (\vect{x} - \vect{\mu})^T\cdot\mat{\Sigma}^{-1}\cdot(\vect{x} - \vect{\mu})
    }{2}\right).
\end{gather*}
:::

Random variables can be combined using the [algebra of random varables].  Some important
results are:

## Sum of Independent Random Variables 

The distribution of the sum $Z = X+Y$ of two independently distributed random variavles
is the convolution $P_{X+Y} = P_X * P_Y$ of the distributions:

\begin{gather*}
  P_{X+Y}(z) = \int_{-\infty}^{\infty}\!\!\!\d{x}\;P_X(x)P_Y(z-x).
\end{gather*}

:::{admonition} Example: Sum of Independent Normal Distributions

The [sum or normally distributed random variables] over the same space is also normal with
the following mean and covariance matrix

\begin{gather*}
  \vect{\mu}_Z = \vect{\mu}_X + \vect{\mu}_Y, \qquad
  \mat{\Sigma}_{Z} = \mat{\Sigma}_X + \mat{\Sigma}_Y.
\end{gather*}

If the spaces are not the same, then the vectors and matrices must be organized
appropriately so corresponding spaces overlap, with the other spaces add in separate
dimensions.

Note: The distributions must be independent, or at least [jointly
normal](https://en.wikipedia.org/wiki/Multivariate_normal_distribution#Joint_normality),
otherwise the resulting distribution might not be a multivariate normal distribution.
:::

## Product of Independent Random Variables

The [distribution of the
product](https://en.wikipedia.org/wiki/Distribution_of_the_product_of_two_random_variables)
 $Z = XY$ of two independently distributed random variables is:

\begin{gather*}
  P_{XY}(z) = \int_{-\infty}^{\infty}\!\!\!\d{x}\frac{P_X(x)P_Y(z/x)}{\abs{x}}.
\end{gather*}

For gaussian distributions with mean $\bar{\vect{x}}$

\begin{gather*}
  P(\delta\vect{x}=\vect{x}-\bar{\vect{x}}) \propto \exp\left(
    \frac{-\delta\vect{x}^T\cdot\mat{\Sigma}^{-1}\cdot\delta\vect{x}}{2}
  \right).
\end{gather*}

## Function of a Random Variable

Let $z=f(x)$ be some function.  The variable $Z=f(X)$ has PDF

\begin{align*}
  P_Z(z) &= \int \delta\Bigl(z - f(x)\Bigr) P_X(x)\d{x}
         = \int \delta\Bigl(z - f(x)\Bigr) P_X(x)
         \overbrace{\left\lvert\diff{z}{x}\right\rvert}^{\abs{1/f'(x)}}\d{z}\\
         &= \sum_{x | f(x)=z}\frac{P_X(x)}{\abs{f'(x)}},
\end{align*}

where the sum is over all independent solutions to $f(x) = z$.

:::{admonition} Example: Square of a Normal Variable

Let $X$ be normally distributed, then $Z = X^2$ has the following distribution:

\begin{gather*}
  P_Z(z) = \sum_{x = \pm \sqrt{z}} \frac{P_X(x)}{2\abs{x}}
           =
           \Theta(z)
           \frac{e^{-(\sqrt{z}-\mu)^2/2\sigma^2} + e^{-(-\sqrt{z}-\mu)^2/2\sigma^2}}
                {2\sqrt{2\pi z \sigma^2}}.
\end{gather*}

If the mean is zero, then this simplifies:

\begin{gather*}
  P_Z(z) = \Theta(z) \frac{e^{-z/2\sigma^2}}{\sqrt{2\pi z \sigma^2}}.
\end{gather*}


If the spaces are not the same, then the vectors and matrices must be organized
appropriately so corresponding spaces overlap, with the other spaces add in separate
dimensions.

Note: The distributions must be independent, or at least [jointly
normal](https://en.wikipedia.org/wiki/Multivariate_normal_distribution#Joint_normality),
otherwise the resulting distribution might not be a multivariate normal distribution.
:::

Working with random variables is fraught with opportunities to make algebraic mistakes,
forgetting factors of 2 etc.  Checking with code is almost trivial, so do it!  (The
hardest part is choosing good parameters for the histograms.)

```{code-cell} ipython3
rng = np.random.default_rng(seed=2)

mu = 3.1
sigma = 1.2

N = 10000
X = rng.normal(loc=mu, scale=sigma, size=N)
Z = X**2
x = np.linspace(mu-4*sigma, mu+4*sigma)
z = np.linspace(-1, 30, 200)

def P_X(x):
    return (np.exp(-(x-mu)**2/2/sigma**2)
            / np.sqrt(2*np.pi * sigma**2))

def P_Z(z):
    x = np.sqrt(abs(z))
    df_dx = 2*abs(x)
    return np.where(z < 0, 0, (P_X(x) + P_X(-x))/df_dx)

kw = dict(histtype='step', alpha=0.8, density=True)
fig, axs = plt.subplots(1, 2, figsize=(10, 3))
ax = axs[0]
ax.hist(X, 200, **kw)
ax.plot(x, P_X(x))
ax.set(xlabel="x", ylabel="$P_X(x)$")

ax = axs[1]
ax.hist(Z, bins=z, **kw)
ax.plot(z, P_Z(z), '-', scaley=False)
ax.set(xlim=(-1, 30), xlabel="$z=x^2$", ylabel="$P_Z(z)$");
```





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
[multvariate normal distribution]: <https://en.wikipedia.org/wiki/Multivariate_normal_distribution>
