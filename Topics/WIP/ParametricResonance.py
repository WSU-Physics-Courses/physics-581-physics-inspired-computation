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

import mmf_setup;mmf_setup.nbinit(set_path=False)

# $$
#   
# $$

# Here we consider a parametric harmonic oscillator, where the frequency changed at some rate $\omega_p$ about the natural resonance at $\omega_0$.
#
# $$
#   \ddot{x} = -\omega^2(t) x, \qquad
#   \omega(t) = \omega_0\bigl(1 + \alpha \cos(\omega_p t)\bigr)\\
#   \ddot{x} = -(A_k + 2 q \cos(2mt) x)\\
#   \diff{}{t}
#   \begin{pmatrix}
#     x\\
#     \dot{x}
#   \end{pmatrix}
#   = \begin{pmatrix}
#     \dot{x}\\
#     -\omega^2(t) x
#   \end{pmatrix}.
# $$

# +
# %pylab inline --no-import-all
from scipy.integrate import solve_ivp
import math

w0 = 1.0
h = 0.1
n = 1
wp0 = 2*w0/n
deps = n**(2*n-3)*h**n * w0/(2**(3*(n-1))*math.factorial(n-1)**2)
wp = wp0

def get_w2(t, wp=wp, w0=w0, h=h):
    return (w0**2 * (1 + h * np.cos(wp*t)))

def get_E(t, y):
    x, dx = y
    E = dx**2/2 + get_w2(t)*x**2/2
    return E
    
def f(t, y, wp=wp):
    x, dx = y
    ddx = -get_w2(t, wp=wp)*x
    return (dx, ddx)

y0 = (0, 1)
T = 200
sol = solve_ivp(f, (0,T), y0=y0)#, rtol=1e-8, method='DOP853')
t, y = sol.t, sol.y
x, dx = y
plt.semilogy(t, get_E(t, y))
#plt.figure(figsize=(20,2))
#plt.plot(t, x)

# -

@np.vectorize
def get_amp(wp, T=1600, y0=(0, 1), **kw):
    sol = solve_ivp(lambda t, y: f(t, y, wp=wp), (0,T), y0=y0, **kw)
    t, y = sol.t, sol.y
    E = get_E(t, y)
    return max(E/E[0])


# +
wps = np.linspace(wp - 2*deps, wp + 2*deps, 100)
amps = get_amp(wps)

plt.plot(wps, amps)
plt.axvline([wp])

# +

w0 =1.0
wp = w0/3
alpha = 0.3
wps = np.linspace(wp-0.01, wp+0.01, 100)
amps = get_amp(wps)
# -

plt.plot(wps, amps)

plt.plot(wps, amps)

# + active=""
# A:=(k^2+g^2*Phi^2);
# q:=g^2*Phi^2/2;
# w0:=sqrt(A);
# h:=2*q/w0^2;
# gam:=2;
# epsilon:=gam-2*w0/n;
# alpha:=3*H;
# lam:=alpha/2;
# -

g = 0.1
k, phi = np.meshgrid(np.linspace(0.9, 3.5, 100), 
                     np.linspace(0.3, 3.5, 100))
plt.contour(k, phi, np.sqrt(k**2+g**2*phi**2),
            levels=[1, 2, 3, 4, 5])
plt.colorbar()


plt.contourf(k, phi, g**2*phi**2/np.sqrt(g**2*phi**2+k**2)/6)
plt.colorbar()


