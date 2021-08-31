---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.1
kernelspec:
  display_name: Python 3 (phys-581-2021)
  language: python
  name: phys-581-2021
---

```{code-cell} ipython3
:cell_style: center
:hide_input: false

import mmf_setup;mmf_setup.nbinit(quiet=True)
%pylab inline --no-import-all
```

# Assignment 0

+++

Complete the following in one of two ways:

1. A simple brute force solution that you completely understand but which may not be fully accurate.
2. A more sophisticated solution that is accurate to close to machine precision.

For the second method, please feel free to use any tools in the [NumPy](https://numpy.org/doc/stable/) or [SciPy](https://docs.scipy.org/doc/scipy/reference/) libraries.  (You may use [mpmath](https://mpmath.org) to check, but don't use it as part of your solution.) 

+++

## Series

+++

Numerically check the following formula:

$$
  \sum_{n=1}^{M} n = \frac{M(M+1)}{2}
$$

```{code-cell} ipython3

```

$$
  \sum_{n=1}^{\infty} \frac{1}{n^{2}} = \zeta(2) = \frac{\pi^2}{6}
$$

where $\zeta(s)$ is the [Riemann zeta function](https://en.wikipedia.org/wiki/Riemann_zeta_function).

```{code-cell} ipython3

```

## Integrals

+++

Numerically check the following integrals for all viable values of $p$ (both positive and negative):

$$
  \int_0^1 x^p \d{x} = \frac{1}{p+1}
$$

```{code-cell} ipython3

```

$$
  \int_{-\infty}^{\infty} e^{-x^2} \d{x} = \sqrt{\pi}
$$

```{code-cell} ipython3

```

$$
  \int_0^{\infty} e^{-x^2}\sin^2\frac{1}{x}\d{x} = \frac{\sqrt{\pi}}{4} G_{14}^{13}\left(
    \left.
    \begin{matrix}
      \tfrac{1}{2}\\
      \tfrac{1}{2} & \tfrac{1}{2} & 0 & -\tfrac{1}{2}
    \end{matrix}
    \right| z=1
  \right)
  =
  0.32006330909018418888\cdots, %37810082287661243051390948375855688739690521501945667936210716620524245639515708
$$
where $G_{mn}^{pq}\bigl(\begin{smallmatrix}\vect{a}_p\\ \vect{b}_q\end{smallmatrix}\big|z\bigr)$ is the [Meijer G-function](https://en.wikipedia.org/wiki/Meijer_G-function).

```{code-cell} ipython3

```

## Roots

+++

Find all solutions $x$ to the following equations:

$$
  x^2 - (1+\epsilon)x + \epsilon = 0, \qquad
  x = \{1, \epsilon\}
$$

for $\epsilon \in \{1, 10^{-10}, 10^{-20}\}$.

```{code-cell} ipython3

```

$$
  xe^x = w, \qquad
  x = L_0(1)
$$

for $w = 1$.


The function $w = W_k(x)$ is the [Lambert W function](https://en.wikipedia.org/wiki/Lambert_W_function).

```{code-cell} ipython3
x = np.linspace(-10, 2, 100)
plt.plot(x, )
```
