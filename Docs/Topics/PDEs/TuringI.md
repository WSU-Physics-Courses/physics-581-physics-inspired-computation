---
jupytext:
  encoding: '# -*- coding: utf-8 -*-'
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
execution:
  timeout: 200
---

```{code-cell} ipython3
:tags: [hide-input]

%pylab inline --no-import-all
from IPython.display import clear_output
import mmf_setup;mmf_setup.nbinit()
```

# Turing Patterns

* https://en.wikipedia.org/wiki/Turing_pattern
* https://en.wikipedia.org/wiki/Reaction%E2%80%93diffusion_system

:::{math}
:class: full-width

\begin{gather*}
  \diff{}{t}\begin{pmatrix}
    u\\
    \tau v
  \end{pmatrix} = 
  \begin{pmatrix}
     d_u^2\nabla^2 + \frac{f(u)}{u} & -\sigma\\
     1 & d_v^2\nabla^2 - 1,
  \end{pmatrix}
  \cdot
  \begin{pmatrix}
    u\\
    v
  \end{pmatrix}, \qquad
  f(u) = \lambda u - u^3 - \kappa
\end{gather*}
:::

```{code-cell} ipython3
from functools import partial
from IPython.display import clear_output
from scipy.integrate import solve_ivp
try:
    from mmfutils.performance.fft import get_fftn_pyfftw, get_ifftn_pyfftw
except Exception:
    get_fftn_pyfftw = get_ifftn_pyfftw = None


class FitzHughNagumo(object):
    # Parameters from 
    # https://ipython-books.github.io/124-simulating-a-partial-differential-equation-reaction-diffusion-systems-and-turing-patterns/
    du = 2.8e-4  # a
    dv = 5e-3  # b
    tau = 0.1  # tau
    sigma = 1.0  #
    lam = 1.0  #
    kappa = 0.005  # -k

    def __init__(self, Nxy=(100, 100), Lxy=(2.0, 2.0), seed=2, **kw):
        self.__dict__.update(kw)
        self.Nxy = tuple(Nxy)
        self.Lxy = tuple(Lxy)
        self.seed = seed
        self.init()

    def fft(self, u):
        return self._fftn(u)

    def ifft(self, u):
        return self._ifftn(u)

    def init(self):
        """Perform all initialization calculations.

        Call after changing parameters or before starting a computation.
        """
        self._d2 = np.asarray([self.du, self.dv]) ** 2

        # Setup the Fourier components for computing gradients/laplacian
        self.xy = np.meshgrid(
            *(np.arange(_N) * _L / _N - _L / 2 for (_N, _L) in zip(self.Nxy, self.Lxy)),
            indexing="ij",
            sparse=True,
        )
        self.kxy = np.meshgrid(
            *(
                2 * np.pi * np.fft.fftfreq(_N, d=_L / _N)
                for (_N, _L) in zip(self.Nxy, self.Lxy)
            ),
            indexing="ij",
            sparse=True,
        )

        self.k2 = sum(_k ** 2 for _k in self.kxy)

        # Random initial state
        np.random.seed(self.seed)
        self.uv = np.random.random((2,) + self.Nxy)
        if get_fftn_pyfftw:
            self._fftn = get_fftn_pyfftw(self.uv, axes=(-2, -1))
            self._ifftn = get_ifftn_pyfftw(self.uv, axes=(-2, -1))
        else:
            self._fftn = partial(np.fft.fftn, axes=(-2, -1))
            self._ifftn = partial(np.fft.ifftn, axes=(-2, -1))
        self.t = 0

    def pack(self, uv):
        return np.asarray(uv).ravel()

    def unpack(self, y):
        return np.reshape(y, (2,) + self.Nxy)

    def f(self, u):
        return -self.kappa + u * (self.lam - u ** 2)

    def compute_dy_dt(self, t, y):
        u, v = uv = self.unpack(y)
        duv = self.ifft(-self.k2[None, ...] * self.fft(uv)).real
        duv[0] *= self.du
        duv[1] *= self.dv
        duv[0] += self.f(u) - self.sigma * v
        duv[1] += u - v
        duv[1] /= self.tau
        return self.pack(duv)

    def callback(self, y, t):
        if not hasattr(self, "_step"):
            self._step = 0
        skip = getattr(self, "_skip", 1)
        step = self._step
        self._step += 1
        if step % skip != 0:
            return
        self.plot(uv=self.unpack(y), t=t)
        display(plt.gcf())
        plt.close("all")
        clear_output(wait=True)

    def plot(self, uv=None, t=None, ax=None):
        if uv is None:
            uv = self.uv
        if t is None:
            t = self.t
        u, v = uv
        x, y = [_x.ravel() for _x in self.xy]
        _args = dict(shading="auto", cmap="copper")
        if ax is None:
            fig, axs = plt.subplots(1, 2, figsize=(10, 5))
            axs[0].pcolormesh(x, y, u.T, **_args)
            axs[1].pcolormesh(x, y, v.T, **_args)
            ax = axs[0]
        else:
            ax.pcolormesh(x, y, u.T, **_args)
        ax.set_title(f"t={t:.2f}")

    def evolve_to(self, t, **kw):
        y0 = self.pack(self.uv)
        self._sol = solve_ivp(self.compute_dy_dt, t_span=(self.t, t), y0=y0, **kw)
        self.uv = self.unpack(self._sol.y[:, -1])
        self.t = t
```

```{code-cell} ipython3
%%time
s = FitzHughNagumo()
fig, axs = plt.subplots(3, 3, figsize=(10,10))
for _n, t in enumerate(np.arange(9)):
    #%time s.evolve_to(t, method='RK45')
    %time s.evolve_to(t, method='RK23')
    s.plot(ax=axs.ravel()[_n])
    display(fig)
    clear_output(wait=True)
```

```ipython3
%%time
# Explicit compuatation using Euler's method... not accurate, but simple
y = s.pack(s.uv)
dt = 0.0002
t = 0
s._skip = 100
while t < 10:
    dy_dt = s.compute_dy_dt(0, y)
    y += dt * dy_dt
    t += dt
    s.callback(y, t)
```
