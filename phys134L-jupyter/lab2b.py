#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime
import os
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy import coordinates, time
from astropy import units as u
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


specfiles = ["spectrum1.dat", "spectrum2.dat", "spectrum3.dat"]
spectra = [np.loadtxt(x) for x in specfiles]
lams = [spectra[i][:, 0] for i in range(3)]
flams = [spectra[i][:, 1] for i in range(3)]
print(lams)


# In[3]:


def plot_spectrum(index):
    """plots the data corresponding to a certain index
       in lams/flams.
    """
    plt.figure(figsize=(14, 12))
    plt.plot(lams[index], flams[index])
    plt.title("Star Spectrum", fontsize=18)
    plt.ylabel(r"Flux Density "
           r"$ \left(\frac{\mathrm{erg}}{s \ cm^2 \ \AA}\right) $",
           fontsize=16)
    plt.xlabel(r"Wavelength $\left( \AA \right)$", fontsize=16)
    
plot_spectrum(0)
plt.show()


# In[4]:


plot_spectrum(1)
plt.show()


# In[5]:


plot_spectrum(2)
plt.show()


# The Planck function is
# $$
# L(\lambda,  T) = \frac{2hc^2}{\lambda^5} \frac{1}{e^{hc/\lambda k_B T}-1}
# $$
# where
# 
# $h = 6.626196 \times 10^{-27} erg \ s$
# 
# $c = 2.997924562 \times 10^{18} \text{angstrom} \ s^{-1}$
# 
# $k_B = 1.380622 \times 10^{-16} erg \ K^{-1}$
# 
# $\lambda = \mathrm{wavelength\ in\ angstrom}$

# In[6]:


# implementation of Planck function
def L(l, T):
    """INPUT: wavelength (A), temperature (K)
       OUTPUT: the spectral radiance
    """
    h = 6.626196 * 10**-27 # erg s
    c = 2.997924562 * 10**18 # A s^-1
    k = 1.380622 * 10**-16 # erg K^-1
    return 2*h*c**2 / l**5 / (np.exp(h*c/l/k/T) - 1)

def plot_planck(T, scale):
    """INPUT: T (K) and scale factor
       OUTPUT: Plot of Planck function
    """
    lambdas = np.arange(1000, 30000, dtype=np.float64)
    plt.plot(lambdas, L(lambdas, T)*scale)


# In[7]:


plot_spectrum(0)
plot_planck(5050, 1/7000)
plt.show()


# In[8]:


plot_spectrum(1)
plot_planck(7000, 12)
plt.show()


# In[9]:


plot_spectrum(2)
plot_planck(7000, 1/700)
plt.show()


# #### Best-Fit Values:
# |        | Temperature ($K$) | Constant ($sr A^2/cm^2$) |
# | ------ | --------------- | ---------------------- |
# | Star 1 | 5050            | 0.00014286             |
# | Star 2 | 7000            | 12                     |
# | Star 3 | 7000            | 0.00142857             |
# 
# Converting to square milliarcseconds using $1\  sr = (180/\pi \ deg)^2$, and converting the Angstrom term,
# 
# |        | Angular Area ($deg^2$) |
# | ------ | -----------------------|
# | Star 1 | 4.69e-17               |
# | Star 2 | 3.94e-12               |
# | Star 3 | 4.69e-16               |
# 
# Multiply by $(3.6 \times 10^6)^2$ to get mas:
# 
# |        | Angular Area ($mas^2$) |
# | ------ | ---------------------- |
# | Star 1 | 6.07e-4                |
# | Star 2 | 51.1                   |
# | Star 3 | 6.07e-3                |
# 
# Convert from angular area to radius by dividing by $\pi$ and taking the square root:
# 
# |        | Angular Radius ($mas$) |
# | ------ | ---------------------- |
# | Star 1 | 0.0139                 |
# | Star 2 | 4.033                  |
# | Star 3 | 0.0779                 |
# 
# The distances to each star (given by parallaxes) are calculated by $r = a/p$ where a = 1 au:
# 
# |        | Distance ($pc$) |
# | ------ | --------------- |
# | Star 1 | 1369.86         |
# | Star 2 | 7.68049         |
# | Star 3 | 88.4956         |
# 
# Multiplying $a = pr$, where a is the approx. physical radius, we find 
# 
# |        | Radius ($au$) |
# | ------ | ------------- |
# | Star 1 | 0.01904       |
# | Star 2 | 0.03098       |
# | Star 3 | 0.006894      |
# 
# Converting au to solar radius using $1\ R_s = 0.00465047\ au$, we find
# 
# |        | Radius ($R_s$) |
# | ------ | -------------- |
# | Star 1 | 4.094          |
# | Star 2 | 6.661          |
# | Star 3 | 1.482          |
