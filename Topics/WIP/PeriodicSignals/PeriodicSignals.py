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
#     display_name: phys581_periodic_signals
#     language: python
#     name: phys581_periodic_signals
# ---

# # Periodic Signals

# Finding a periodic signal from some data is a common problem across many domains of study. Some examples include: daily temperature, periodic luminosity of stellar objects, finding cycles in stock data, precise measurement of resonances, and pitch detection in music.
#
# To get started, please look in the [PeriodicData.ipynb](PeriodicData.ipynb) notebook which shows you how to load several different signals.  If you have not played much with period finding, try playing with this data.

# # Magnitude of an RR Lyrae variable star

# We will start with the astronomical data presented there looking for the period of a variable star using the data loaded in the [PeriodicData.ipynb](PeriodicData.ipynb#Magnitude-of-an-RR-Lyrae-variable-star) notebook.

# +
# %pylab inline --no-import-all
plt.rcParams['figure.figsize'] = [6, 4]
plt.rcParams['figure.dpi'] = 100

import pandas as pd
pd.options.display.max_rows = 10
data = pd.read_csv('_data/V1_calibExcel.csv', 
                   index_col=0,
                   names=["barycentric julian date", "magnitude", "magnitude_err"])
t = (data.index - data.index.min()).values  # days from start of observations
y, dy = data["magnitude"].values, data["magnitude_err"].values

fig, ax = plt.subplots(1, 1)
ax.errorbar(t, y, yerr=dy, fmt='+')
ax.set(xlabel="$t$ [day]", ylabel="magnitude");
# -

# ## Black Box: the Lomb-Scargle periodogram

# As discussed in [PeriodicData.ipynb](PeriodicData.ipynb#Magnitude-of-an-RR-Lyrae-variable-star), since this data is unevenly spaced, the [Lomb-Scargle periodogram](https://iopscience.iop.org/article/10.3847/1538-4365/aab766) as implemented in [`scipy.signal.lombscargle`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.lombscargle.html) is a good first choice for black-box exploration.  This gives us an estimated period of $T=0.63(1)$ days.  Now we want to test this.
#
# One approach, common in astronomy, is to look at the data modulo the period.  If the period is properly chosen, then it should wrap-around nicely.  Here is an interactive widget you can play with:

# +
from ipywidgets import interact

@interact(T0=(0.60,0.66,0.001))
def draw_mod_data(T0=0.63):
    plt.plot(t % T0, y, '+')
    plt.xlim(0,0.66)
    display(plt.gcf())
    plt.close('all')


# -

# To make this more quantitative, we can sort the data, then look at the differences, trying to minimize these.

# +
@np.vectorize
def get_residual(T0):
    """Return mean of differences of the data sorted mod T."""
    return (abs(np.diff(y[np.argsort(t % T0)]))**2).sum()

fig, axs = plt.subplots(1, 2, figsize=(12, 4))
Ts = np.linspace(0.55, 0.7, 200)
axs[0].plot(Ts, get_residual(Ts))
Ts = np.linspace(0.01, 5.0, 2000)  # Need enough points or we miss it!
axs[1].plot(Ts, get_residual(Ts))
for ax in axs:
    ax.axvspan(0.616, 0.636, color='y', alpha=0.5)
    ax.axvspan(0.621, 0.628, color='g', alpha=0.5)    
# -

# We might argue that this allows us to extract a period of $T=0.6245(35)$, but we again have not used the errors.

# ## Phases

# +
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots(1, 1, figsize=(6, 4))

Ts = np.linspace(0.55, 0.7, 1000)
T0 = Ts[0]
residuals = get_residual(Ts)

_t = t % T0
_inds = np.argsort(_t)
t_y_points, = ax.plot(_t[_inds], y[_inds], '-+')
ax.set(xlim=(0, Ts.max()), ylim=(y.min(), y.max()), 
       ylabel="magnitude",
       xlabel="$t$ (mod $T$)")

axi = ax.inset_axes([0.75, 0.75, 0.25, 0.25])
axi.axis('off')
axi.plot(Ts, residuals)

marker, = axi.plot(Ts[0], residuals[0], 'r.')

def init():
    return [t_y_points, marker]

def animate(T0):
    _t = t % T0
    _inds = np.argsort(_t)
    t_y_points.set_data(_t[_inds], y[_inds])
    marker.set_data(T0, get_residual(T0))
    return [t_y_points, marker]

anim = FuncAnimation(fig, animate, init_func=init, frames=Ts[::2], blit=True)
anim.save("phases.mp4", fps=20, extra_args=['-vcodec', 'libx264'])
# -

# [Phases Movie](phases.mp4)

# +
from IPython.display import clear_output

fig, ax = plt.subplots(1, 1, figsize=(6, 4))

Ts = np.linspace(0.55, 0.7, 1000)
T0 = Ts[0]
residuals = get_residual(Ts)

_t = t % T0
_inds = np.argsort(_t)
t_y_points, = ax.plot(_t[_inds], y[_inds], '+',)
ax.set(xlim=(0, Ts.max()), ylim=(y.min(), y.max()), 
       ylabel="magnitude",
       xlabel="$t$ (mod $T$)")

axi = ax.inset_axes([0.75, 0.75, 0.25, 0.25])
axi.axis('off')
axi.plot(Ts, residuals)

marker, = axi.plot(Ts[0], residuals[0], 'r.')

for T0 in Ts[::5]:
    _t = t % T0
    _inds = np.argsort(_t)
    t_y_points.set_data(_t[_inds], y[_inds])
    marker.set_data(T0, get_residual(T0))
    display(fig)
    clear_output(wait=True)
# -

# ##
