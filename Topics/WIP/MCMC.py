# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python [conda env:work]
#     language: python
#     name: conda-env-work-py
# ---

import mmf_setup;mmf_setup.nbinit()

# # Emcee

# Here we walk through the example given in the [`emcee` documentation](https://emcee.readthedocs.io).

# ## Problem: Line Fitting

# The problem is to fit a line $y=a_1x+a_0$ to a set of data $D=\{(x_i, y_i)\}$ where the measurements have some "noise" described by a distribution $P(D|\vect{a})$ which is called the **liklihood that the measurement  $D=\{(x_i, y_i)\}$ came from the model with parameters $\vect{a}$**.  In the case described, the error model is:
#
# $$
#   y_i = f_{\vect{a}}(x_i) + e_i = a_0 + a_1 x_i + e_i,
# $$
#
# where the errors $e_i = e^0_i + e^1_i$ have two pieces, a normally distributed error $e^0_i$ with standard deviation $0.1 < \sigma_i < 0.6$ (`yerr` in the code) and another piece $e^1_i$ normally distributed with $\sigma=f\abs{y_i}$ where $f=0.534$ *(values taken from the code exmple)*.
#
# $$
#   P(e_i) = N_{\sigma=\sqrt{\sigma_i^2+f^2y_i^2}}(e_i).
# $$
#
# ### Exercise
# > Prove this relationship by showing how to add random variables.  Supposed that $x$ and $y$ have distributions $P_x(x)$ and $P_y(y)$ respectively.  Show that $z=x+y$ is distributed as:
# >
# > $$
#     P_z(z) = \int P_x(x)P_y(z-x)\d{x} = \int P_x(z-y)P_y(y)\d{y}
#   $$
# > 
# > More generally, $z=f(x, y)$ is distributed as
# >
# > $$
#     P_z(z) = \int P_x(x)P_y(y)\delta\bigl(z - f(x, y)\bigr)\d{x}\d{y}.
#   $$
# >
# > Do the integral for two normal distributions with zero mean but different variances to prove the result.

# +
# Numerical check of adding distributions
# %pylab inline --no-import-all
import scipy.stats
np.random.seed(123)
N = 50000
sx, sy = 1, 2
sz = np.sqrt(sx**2+sy**2)
x = sx * np.random.normal(size=N)
y = sy * np.random.normal(size=N)
z = x + y

Px, Py, Pz = [scipy.stats.norm(loc=0, scale=_s)
              for _s in [sx, sy, sz]]

fig, axs = plt.subplots(1, 3, figsize=(9,3))
for ax, v, Pv, l in zip(axs, [x, y, z], [Px, Py, Pz], "xyz"):
    ax.hist(v, bins=50, density=True, alpha=0.5)
    _x = np.linspace(v.min(), v.max())
    ax.plot(_x, Pv.pdf(_x))
    ax.set(xlabel=l)

# +
# %pylab inline --no-import-all
np.random.seed(123)

# "True" parameters
a_true = [4.294, -0.9594]
f_true = 0.534
q_true = a_true + [np.log(f_true)]

def model(x, *a):
    return np.polyval(a[::-1], x)

# Generate synthetic data
N = 50
x = np.sort(10 * np.random.random(N))
yerr = 0.1 + 0.5 * np.random.random(N)
y = model(x, *a_true)
y += np.abs(f_true * y) * np.random.normal(size=N)
y += yerr * np.random.normal(size=N)

def draw_data(ax):
    ax.errorbar(x, y, yerr=yerr, fmt=".k", capsize=0)

    x0 = np.linspace(0, 10, 500)
    ax.plot(x0, model(x0, *a_true), "k", alpha=0.3, lw=3, label='True')
    ax.set(xlim=(0, 10), xlabel="x", ylabel="y");
    return x0

fig, ax = plt.subplots(1,1)
draw_data(ax);


# -

# The MCMC method needs the log-likelihood for obtaining the data
#
# $$
#   \ln P(D|\vect{a}) = -\frac{1}{2}\sum_{i}\left[
#     \frac{\bigl(y_i - f(x_i|\vect{a})\bigr)^2}{s_i^2} + \ln(2\pi s_i^2)
#     \right], \qquad
#     s_i^2 = \sigma_i^2 + f^2 f(x_i|\vect{a})^2.
# $$
#
# Note: this is simply the sum of the logs of normalized normal distributions:
#
# $$
#   N_{\sigma}(x) = \frac{e^{-x^2/2\sigma^2}}{\sqrt{2\pi \sigma^2}}, \qquad
#   \ln N_{\sigma}(x) = -\frac{x^2}{2\sigma^2} - \ln\sqrt{2\pi \sigma^2}
#   =  -\frac{1}{2}\left[\frac{x^2}{\sigma^2} + \ln(2\pi \sigma^2)\right].
# $$
#
# We now assume that this model of error is correct, but assume that we do not know the parameter $f$.  We thus run an optimizer that maximize the log-likelhood as a function of $\vect{q} = (\vect{a}, \ln f)$

def log_likelihood(q, x, y, yerr):
    a, log_f = q[:2], q[2]
    f = np.exp(log_f)
    f_x = model(x, *a)
    s2 = yerr**2 + (f*f_x)**2
    return -0.5 * np.sum((y-f_x)**2 / s2 + np.log(2*np.pi * s2))


# Now we compare three fits to the data:
#
# 1. Standard least squares with the incorrect error estimates $\sigma_i$.
# 2. Standard least squares with the correct error estimates $s_i$.
# 3. Maximum likelihood with unknown $f$.

# +
from scipy.optimize import curve_fit, minimize
from uncertainties import correlated_values, unumpy as unp


a0 = [5, -1]
sigma = yerr
s = np.sqrt(yerr ** 2 + np.abs(f_true * model(x, *a_true) ** 2))

a1 = correlated_values(*curve_fit(model, x, y, a0, sigma=sigma, absolute_sigma=True))
a2 = correlated_values(*curve_fit(model, x, y, a0, sigma=s, absolute_sigma=True))
sol = minimize(lambda q: -log_likelihood(q, x, y, yerr), [5, -1, 1]) 
q3 = correlated_values(sol.x, sol.hess_inv)
a3, f3 = q3[:2], q3[2]
fig, ax = plt.subplots(1, 1)
x0 = draw_data(ax)
for _a, _l in [(a1, 'LS1'), (a2, 'LS2'), (a3, 'ML')]:
    _y = model(x0, *_a)
    _y, _dy = unp.nominal_values(_y), unp.std_devs(_y)
    l, = ax.plot(x0, _y, '--', label=_l)
    ax.fill_between(x0, _y-_dy, _y+_dy, color=l.get_c(), alpha=0.5)
plt.legend()
# -

print("\n".join([", ".join(map("{:+.1uS}".format, _a)) for _a in [a1, a2, a3]]))


# The Bayesian problem we are trying to solve is stated as:
#
# $$
#   P(\vect{q}|D,I) = \frac{P(D|\vect{q},I)P(\vect{q}|I)}{P(D|I)}.
# $$
#
# The various pieces are:
#
# 1. $P(\vect{q}|I)$: This is the **priori probability**.  It describes our prior knowledge about the distribution of the parameters $\vect{q} = (\vect{a}, f)$ which includes the factor $f$ modeling our errors in the current case.
# 2. $P(D|\vect{q},I)$: This is the **direct probability**, which is our likelihood function described above.  It describes how likely it would be to obtain the data $D$ given the parameters $\vect{q}$ and any prior information.
# 3. $P(D|I)$: This is the **prior probability of the data** $D$.  For parameter estimation, this is best thought of as a normalization constant, computed after everything to ensure that the posterior $P(\vect{q}|D,I)$ is normalized.

# ## MCMC

# The MCMC method allows us to construct the 

# +
def log_prior(q):
    """Return the log of the prior."""
    # Note: this does not have to be normalized.
    a, log_f = q[:2], q[2]
    if -5.0 < a[1] < 5.0 and 0.0 < a[0] < 10.0 and -10 < log_f < 1:
        return 0.0
    return -np.inf

def log_probability(q, x, y, yerr):
    lp = log_prior(q)
    return log_prior(q) + log_likelihood(q, x, y, yerr)



# +
import emcee
np.random.seed(123)

q0 = unp.nominal_values(q3)

# Initial distribution of "walkers" about the solution
Nwalkers = 32
Nsamples = 5000
Ndim = len(q0)
pos = q0 + 1e-4 * np.random.normal(size=(Nwalkers, Ndim))
sampler = emcee.EnsembleSampler(Nwalkers, Ndim, log_probability, args=(x, y, yerr))
sampler.run_mcmc(pos, Nsamples, progress=True);
# -

tau = sampler.get_autocorr_time()
print(f"autocorrelation times: {tau}")
discard = int(3*max(tau))
thin = int(max(tau)/2)
flat_samples = sampler.get_chain(discard=discard, thin=thin, flat=True)

import corner
labels = ['$a_0$', '$a_1$', r'$\log(f)$']
fig = corner.corner(
    flat_samples, labels=labels, 
    #truths=[q3[0].n, q3[1].n, q3[2].n]
    truths=[a_true[0], a_true[1], np.log(f_true)]
);

from IPython.display import display, Math
for i in range(ndim):
    mcmc = np.percentile(flat_samples[:, i], [16, 50, 84])
    errs = np.diff(mcmc)
    txt = r",\qquad ".join([
        fr"{labels[i][1:-1]} = {mcmc[1]:.2f}_{{-{errs[0]:.3f}}}^{{{errs[1]:.2f}}}",
         fr"\delta {labels[i][1:-1]} = {mcmc[1]-q_true[i]:.2f}_{{-{errs[0]:.3f}}}^{{{errs[1]:.2f}}}"])
    display(Math(txt))    
