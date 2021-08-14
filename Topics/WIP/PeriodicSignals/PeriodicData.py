# -*- coding: utf-8 -*-
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

# This notebook points to some data sources where you can download real data about various periodic signals.

# ## Questions and Comments

# When considering the extraction of a periodic signal, one should consider the following:
#
# 1. Do you have a model for the signal?  If so, fitting the model will probably do a much better job than just applying a generic algorithm.
# 2. Are there any trends that should first be removed?
# 3. Is the data sampled at a regular interval?  If so, then Fourier techniques might be useful.
# 4. Is the data accurate?  Do any points need to be excluded from the analysis (e.g. broken detector)?

# # Stock Prices

# This can be downloaded using the [yfinance](https://github.com/ranaroussi/yfinance) package:

# %pip install -q yfinance

# +
# %pylab inline --no-import-all
plt.rcParams['figure.figsize'] = [6, 4]
plt.rcParams['figure.dpi'] = 100

import yfinance as yf
# Here are the stock prices for Zoom
data = zoom_data = yf.download(tickers=["ZM"], start="2019-01-01", period="1d")
data
# -

# Here we plot the data.  Can you find any patterns?  If so, maybe you can use this to get rich!

data['Adj Close'].plot()   # Pandas formats x-labels nicely
plt.fill_between(data.index, data['Low'], data['High'], color="C1", alpha=0.5)
plt.ylabel("Price (USD)");

# ## Questions/Comments
#
# 1. People typically thing of financial data from the perspective of growth: i.e. a stock value went up or down by $x$%.  Thus, it is often analyzed from the perspective of the log of the daily gains.
# 2. Trading only takes place about 250 days of the year (no weekends or holidays).  How does this affect your potential analysis?

close_price = data['Adj Close']
assert not np.any(np.isnan(close_price))  # Check that data is complete
# Compute daily gains
gains = close_price.values[1:]/close_price.values[:-1]
plt.plot((gains-1)*100)
ax = plt.gca()
ax.set(title="Zoom daily gains (%)", xlabel="day", ylabel="daily gain [%]")

# # Temperature Data

# There are several databases for temperature data.  You can order data from the [NOAA Website](https://www.ncdc.noaa.gov/cdo-web/datatools) for example.  Here I have downloaded data from the Pullman/Moscow airport.
#
# ```
# Processing Completed	2021-06-17
# Stations	
# GHCND:USW00094129
# Begin Date	1998-06-07 00:00
# End Date	2021-06-14 23:59
# Data Types	
# TAVG TMAX TMIN
# Units	
# Metric
# Custom Flag(s)	
# Station Name
# Eligible for Certification	No
# ```

import numpy as np
import pandas as pd
data = pullman_data = pd.read_csv('_data/2617192.csv')
pullman_data

# Set the date as the index, and extract onlt the temperature
data = pullman_data.set_index('DATE')[['TMAX', 'TMIN']]
fig, ax = plt.subplots(1, 1, figsize=(20,2))
data.plot(ax=ax)
ax.set(ylabel='T [C]', title="Temperature at Pullman/Moscow Airport")

# This data clearly contains an annual cycle due to the change in inclination of the earth's axis – the [tropical year](https://en.wikipedia.org/wiki/Tropical_year).
#
# Here is one more dataset to play with: this time, from Moab UT:

moab_data = pd.read_csv('_data/2478833.csv')
moab_data

data = moab_data.set_index('DATE')[['TMAX', 'TMIN']]
fig, ax = plt.subplots(1, 1, figsize=(20,2))
data.plot(ax=ax)
ax.set(ylabel='T [C]', title="Temperature at Moab UT")

# ## Questions and Comments

# Since the main cycle comes from a well-established physical principle, we are pretty certain that there should be a periodic signal.  Unlike the financial data, we thus expect to be able to fit this with a model, allowing a highly accurate extraction of the period, especially if we can formulate an underlying model.
#
# 1. How accurately can you determine the [tropical year](https://en.wikipedia.org/wiki/Tropical_year) from this data?  How does the accuracy of your answer depend on things like $T$, the overall period over which the data is accumulated, $d{t}$, the sampling rate (this data is daily).  What if you only have some data from the start and from the end: does the data in the middle help much?  *(I.e. If you wanted to get funding for a weather station for the sole purpose of determining the period of the tropical year, would it be worth taking continuous data or would it perhaps be more economical to take data at widely separated intervals?)*
# 2. How accurate do you think the data is?  How might you deal with inaccuracies or strong fluctuations?
#     * *(For example, if you do something like a least-"squares" fit, how do your results depend on the choice of "norm"?)*
# 3. Will your algorithm work if there is missing or incomplete data?
# 4. Although we expect this data to be periodic with high accuracy, this does not mean that the signal is purely sinusoidal.  How can you account for departures from pure sinusoids?  Can you explain the deviations?  *(Hint: does Pullman's latitude play any role here?)
# 5. Do you see any other features in this data beyond the yearly cycle?  *(For example, there is an 11-year [solar cycle](https://en.wikipedia.org/wiki/Solar_cycle): can you see any evidence for this in the data?)

# # Magnitude of an RR Lyrae variable star

# Here we consider fluctuations in the [magnitude](https://en.wikipedia.org/wiki/Magnitude_(astronomy)) of an [RR Lyrae variable](https://en.wikipedia.org/wiki/RR_Lyrae_variable) star of type [RRab](https://en.wikipedia.org/wiki/RR_Lyrae_variable#Classification).  This data (courtesy of Michael Allen) consists of the magnitude and error organized by [barycentric Julian date](https://en.wikipedia.org/wiki/Barycentric_Julian_Date) (BJD) which corrects for the motion of the earth.  *(This is an example of pre-processing the data to remove some known trends that might impact the signal.)*

import pandas as pd
pd.options.display.max_rows = 10
data = pd.read_csv('_data/V1_calibExcel.csv', 
                   index_col=0,
                   names=["barycentric julian date", "magnitude", "magnitude_err"])
data

day = data.index - data.index.min()  # Relative date from start of observations
y, dy = data["magnitude"], data["magnitude_err"]
plt.errorbar(day, y, yerr=dy, fmt="+")
ax = plt.gca()
ax.set(xlabel="day [BJD]", ylabel='apparent magnitude');

# ## Black-Box Investigation

# This data is unevenly spaced, so Fourier techniques are not the first choice.  Instead, we can consider the [Lomb-Scargle periodogram](https://iopscience.iop.org/article/10.3847/1538-4365/aab766) as implemented in [`scipy.signal.lombscargle`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.lombscargle.html).

from scipy.signal import lombscargle
Ts = 10**np.linspace(np.log10(0.01), np.log10(2), 500)
pgram = lombscargle(day, y, freqs=2*np.pi/Ts, precenter=True)
T0 = Ts[np.argmax(pgram)]
plt.semilogx(Ts, pgram)
ax = plt.gca()
ax.set(xlabel="Period (days)", title=rf"Period $T\approx{T0:.3f}$ days");

Ts = np.linspace(0.9*T0, 1.1*T0, 100)
pgram = lombscargle(day, y, freqs=2*np.pi/Ts, precenter=True)
T0 = Ts[np.argmax(pgram)]
dT = 0.01 # Estimated by eye
plt.plot(Ts, pgram)
plt.axvline(T0, c='y', ls=':')
plt.axvspan(T0-dT, T0+dT, color='y', alpha=0.5)
ax = plt.gca()
ax.set(xlabel="Period (days)", title=f"Period T={T0:.3f}(10)days");

# ## Questions/Comments

# 1. The Lomb-Scargle periodogram is being used here as a black box.  There is a nice explanation by Jacob VanderPlas: ["Understanding the Lomb–Scargle Periodogram"](https://iopscience.iop.org/article/10.3847/1538-4365/aab766), but one should definitely not rely on this without understand the details.  Can you quickly check the results?
#     > For example, if you do not read the [`lombscargle` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.lombscargle.html) carefully, you might forget that `freq=2*np.pi/Ts` is an **angular** frequency, and hence forget the factor of $2\pi$.  Then you might report the period as $0.1$ days, and be ridiculed by your colleagues.
# 2. How accurate is our result?  Note that we have not made use of the uncertainties in the magnitudes.  How could you go about testing the hypothesis that the period is indeed $T=0.626(10)$ days?    


