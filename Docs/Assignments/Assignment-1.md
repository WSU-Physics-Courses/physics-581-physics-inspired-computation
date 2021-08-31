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

# Assignment 1: Monty Hall

+++

Write a function {func}`phys_581_2021.assignment1.sample_monty_hall` which returns an array or list of $N$ sample Monty-Hall games which we can analyze with a histogram to find the probability of winning.

+++

## Evaluating Functions

+++

Write a function {func}`phys_581_2021.assignment_0.quadratic_equation` which returns the roots of the equation

$$
  ax^2 + bx + c = 0.
$$

For example:

$$
  x^2 - 3x + 2 = (x-2)(x-1)
$$

so we expect

```{code-cell} ipython3
from phys_581_2021.assignment_0 import quadratic_equation
np.allclose(quadratic_equation(a=1, b=-3, c=2), [1, 2])
```

Note: if you attempt to blindly use the quadratic formula, you will encounter errors when $b \approx \pm \sqrt{b^2 - 4ac}$ because the two terms can cancel.  This is the main source of error associated with floating point comptations.

1. When will this become a problem?
2. How can you overcome this issue?
3. How will you test your code to make sure it works well?

The goal should be for every function to return an answer that has a relative error comparable to the **machine precision** of the computer: sometimes called $\epsilon = $`eps`.  This is not always possible if the problem is ill-conditioned.

+++

## Floating Point Numbers

+++

**Readings:**
* {cite:p}`Gezerlis:2020` Chapter 2.  Try some of the "experiments" Alex suggests.
* {cite:p}`Goldberg:1991` "What Every Computer Scientist Should Know About Floating-Point Numbers."  This is a rather technical, but complete account about floating point numbers, and contains a detailed analysis of this assignment.

We can use NumPy to see the properties of the floating point numbers.  The defult `float` in python is the IEEE double-precision floating point number which has $64 = 52 + 11 + 1$ bits. 52 of these are used for the **mantissa**, 11 for the **exponent** and 1 for the sign.  Roughly, the relative error in a floating point number is `eps`=$\epsilon = 1/2^{52}\approx 2.22\times 10^{-16}$ (16 digits of precision in decimal), with an exponent that can range from $\pm 2^{10} = \pm 1024$ with a smallest value of `tiny`$\approx 2^{-1024} \approx 5.56\times 10^{-309}$ and largest value of `max`$=2^{1024}\approx 1.798\times 10^{208}$.

*Try to compute these numbers!  In particular, `2**1024.0` causes an overflow... how can you compute $2^{1024}\approx 1.798\times 10^{208}$ using floating point numbers?  Hint:*

$$
  2^n = a\times 10^m, \qquad
  n\log_{10}(2) = \log_{10}(a) + m.
$$

The actual values are a little different as we see below (e.g. `tiny`$=2^{-1022}=2.225\times 10^{-308}$) because of some subtleties in the actual implementation of the IEEE standard. See
The actual

```{code-cell} ipython3
import numpy as np
print(np.finfo(float))
```

## Roundoff vs Truncation Error

+++

Consider computing the derivative of a function using finite-difference techniques:

$$
  f'(x) = \lim_{h\rightarrow 0} \frac{f(x+h) - f(x)}{h}.
$$

We can estimate the error computing this by using the Taylor series for the function:

$$
  f(x\pm h) = f(x) \pm h f'(x) + \frac{h^2}{2}f''(x) \pm \frac{h^3}{3!}f'''(x) +  \sum_{n=4}^{\infty} \frac{(\pm h)^n}{n!}f^{(n)}(x),\\
  D^+_h f(x) = \frac{f(x+h) - f(x)}{h} = f'(x) + \frac{h}{2}f''(x) + \order(h^2).
$$

This *forward-difference* approximation thus has a **truncation-error** that scales as $hf''(x)/2$.  We can do a bit better if we take the centered-difference approximation:

$$
  D_h f(x) = \frac{f(x+h) - f(x-h)}{2h} + \frac{h^2}{6}f'''(x) + \order(h^3). 
$$

However, this is not the only source of error.  If all goes well, the values $f(x\pm h)$ will be computed with a relative error of machine precision $\epsilon$, which means they will have have an absolute error of $\approx \epsilon f(x)$.  Dividing this error by $2h$, however, means that the whole expression will have an absolute error of about $\epsilon f(x)/2h$ because of **roundoff error**.  Notice that this gets significantly **worse** as $h$ gets small.

With this formula, the best we can do is to choose

$$
  h \approx \sqrt[3]{3\epsilon \left\lvert\frac{f(x)}{f'''(x)}\right\rvert}
$$


The following plot shows that these estimates are accurate.

```{code-cell} ipython3
:hide_input: false

eps = np.finfo(float).eps
h = 10 ** np.linspace(-12, 1, 100)
x = 1.0
f = np.sin
df = np.cos
d3f = lambda x: -np.sin(x)
Df_x = (f(x + h) - f(x - h)) / 2 / h  # Centered difference approx
err = abs(Df_x - df(x))
truncation_err = abs(h ** 2 * d3f(x) / 6)
roundoff_err = abs(eps * f(x) / 2 / h)
h_opt = (3*eps*abs(f(x)/d3f(x)))**(1/3)
fig, ax = plt.subplots()
ax.loglog(h, err)
ax.plot(h, truncation_err, "--", label="Truncation error: $h^2 f'''(x)/6$")
ax.plot(h, roundoff_err, ":", label="Roundoff error: $f(x)/2h$")
ax.axvline(h_opt, c='y', ls='-.', label='optimal $h$')
ax.set(xlabel="h", ylabel="abs err", ylim=(1e-16, 1))
ax.legend()
```

Notice that the truncation error is smooth, but the roundoff error appears random.  As Alex discusses {ref}`Gezerlis:2020` (see Fig. 2.3), roundoff errors are not random.  We can see this by zooming in:

```{code-cell} ipython3
h = 10 ** np.linspace(-11, -11.0002, 1000)
Df_x = (f(x + h) - f(x - h)) / 2 / h  # Centered difference approx
err = abs(Df_x - df(x))
fig, ax = plt.subplots()
ax.semilogy(h, err)
ax.set(xlabel="h", ylabel="abs err");
```

```{code-cell} ipython3

```
