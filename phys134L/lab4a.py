#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import constants, interpolate
get_ipython().run_line_magic('matplotlib', 'inline')

plt.rcParams["figure.figsize"] = (16, 12)
plt.rcParams["axes.titlesize"] = 16
plt.rcParams["axes.labelsize"] = 14


# In[2]:


specfiles = ("f05", "f10", "f15")
specpaths = [os.path.join("data", f+".dat") for f in specfiles]
spec = {specfiles[i]: np.loadtxt(specpaths[i]) 
        for i, p in enumerate(specfiles)}
lams = {key: val[:,0] for key, val in spec.items()}
flams = {key: val[:,1] for key, val in spec.items()}


# In[3]:


def planck(lam, T, scale):
    h = constants.h * 10**7
    c = constants.c * 10**10
    kb = constants.Boltzmann * 10**7
    s = scale * 10**11
    return s*2*h*c**2/lam**5/(np.exp(h*c/lam/kb/T)-1)

temps = (9550, 6110, 4350)
# figure out normalization
# we want these close to 100
# minimize difference between Planck function at 5500 and 100
scalerange = np.linspace(0, 20, 2001)
scales = []
for t in temps:
    scales.append(scalerange[np.argmin(
        np.abs(100 - planck(5500, t, scalerange)
              ))])
print(scales)

colors1 = ("C0", "C1", "C2")
colors2 = ("blue", "red", "green")
for i, k in enumerate(lams):
    plt.plot(lams[k], flams[k], c=colors1[i],
             label=f"{temps[i]} K")
    plt.plot(lams[k], planck(lams[k], temps[i], scales[i]), 
             c=colors2[i], lw=2.5)
plt.title("Stellar Spectra")
plt.xlabel(r"Wavelength $\left( \AA \right)$")
plt.ylabel(r"Flux $\propto \mathrm{erg\ } \mathrm{s}^{-1}"
           r"\mathrm{cm}^{-2} \AA^{-1}$")
plt.legend()
plt.show()


# In[4]:


def riemann(f, a, b, N):
    """A function to approximate integrals using the Riemann sum.
       Input: a function, start/endpoints a & b, N subdivisions
       Output: the value of the integral
    """
    dx = (b - a) / (N + 1)
    x = np.linspace(a, b, N + 1)
    return np.sum(f(x) * dx)

# integrate sin(x) from 0 to 1
# the value from Wolfram Mathematica is 0.459697694131861
val = 0.459697694131861
sin2000 = riemann(np.sin, 0, 1, 2000)
sin500 = riemann(np.sin, 0, 1, 500)
print("2000 subdivisions")
print(sin2000)
print(f"with error of {np.abs(sin2000 - val)}")
print("500 subdivisions")
print(sin500)
print(f"with error of {np.abs(sin500 - val)}")


# In[5]:


filtfiles = ("B", "V")
filtpaths = [os.path.join("data", f+"filt.dat") for f in filtfiles]
filt = {filtfiles[i]: np.loadtxt(filtpaths[i]) 
        for i, p in enumerate(filtfiles)}


# In[6]:


def fmul(f, g):
    """A function to return the multiplication of two functions."""
    return lambda x : f(x)*g(x)

# integrating the wavelengths in spectral data
# intrapolate functions first
# these are dictionaries of interpolated functions
Flams = {name: interpolate.interp1d(data[:,0], data[:,1],
                                    kind="cubic", fill_value=0,
                                    bounds_error=False)
         for name, data in spec.items()}
Filts = {name: interpolate.interp1d(func[:,0], func[:,1],
                                    kind="cubic", fill_value=0,
                                    bounds_error=False)
         for name, func in filt.items()}

# combine these into a dict of integral values,
# e.g. energy_flux["Bf05"] yields 
# riemann(T(x)F(x)dx) from 0 to Fmax
energy_flux = {}
for flam_name, f in Flams.items():
    for filt_name, g in Filts.items():
        fg = fmul(f, g)
        start = 0
        end = np.max(lams[flam_name])
        N = 2000
        energy_flux[filt_name+flam_name] = riemann(fg, start, end, N)
        
calc_mag = {key: -2.5*np.log10(val) for key, val in energy_flux.items()}
        
for name in specfiles:
    print(f"{'B'+name}: {calc_mag['B'+name]:.6f}")
    print(f"{'V'+name}: {calc_mag['V'+name]:.6f}")
    print(f"{'B-V'+name}: "
          f"{calc_mag['B'+name]-calc_mag['V'+name]:.6f}")


# In[30]:


evofiles = ("0.8", "1.0", "1.3", "1.8", "2.6")
evopaths = [os.path.join("data", "evol_M"+f+".dat") for f in evofiles]
evo = {evofiles[i]: np.loadtxt(evopaths[i])
       for i, p in enumerate(evofiles)}
evotemps = {key: val[:,0] for key, val in evo.items()}
evolumin = {key: val[:,1] for key, val in evo.items()}
evoage = {key: val[:,2] for key, val in evo.items()}


# In[73]:


# stellar evolutionary tracks
annotations = {"1": (3.758, -0.22),
               "2": (3.776, 0.14),
               "3": (3.761, 0.35),
               "4": (3.693, 0.41),
               "5": (3.637, 1.81)}
for key, data in evotemps.items():
    plt.plot(data, evolumin[key],
             label=f"M{key}")
for label, loc in annotations.items():
    plt.annotate(label, loc, fontsize=16)
plt.xlim(4.1, 3.6)
plt.title("Stellar Evolutionary Tracks")
plt.ylabel("log(Luminosity)")
plt.xlabel("log(Temperature)")
plt.legend()
plt.show()


# In[139]:


# plotting isochrones
agegyrvals = (0.01, 0.1, 0.6, 5)
agedata = {str(k): [[], []] for k in agegyrvals}
for star, ages in evoage.items():
    for gyrval in agegyrvals:
        # exclude stars for which the star was too young
        if np.max(ages) > gyrval:
            ageindex = np.argmin(np.abs(ages - gyrval))
            agedata[str(gyrval)][0].append(evotemps[star][ageindex])
            agedata[str(gyrval)][1].append(evolumin[star][ageindex])

fig, axes = plt.subplots(len(agegyrvals), figsize=(16, 56))
for ax in axes:
    ax.set_xlim(4.1, 3.6)
    ax.set_ylabel("log(Luminosity)")
    ax.set_xlabel("log(Temperature)")
    for key, data in evotemps.items():
        ax.plot(data, evolumin[key], c="black")
for i, (isochrone, data) in enumerate(agedata.items()):
    axes[i].set_title(f"{isochrone} Gyr Isochrone")
    axes[i].plot(data[0], data[1], c="green", lw = 5)
fig.subplots_adjust(hspace=0.15)
plt.show()


# In[189]:


m1plotdata = [[], []]
for i in range(1, 13):
    m1index = np.argmin(np.abs(evoage["1.0"] - i))
    m1plotdata[0].append(evotemps["1.0"][m1index])
    m1plotdata[1].append(evolumin["1.0"][m1index])
    plt.annotate(str(i), (evotemps["1.0"][m1index],
                         evolumin["1.0"][m1index]),
                         xytext=(6, 2), fontsize=14,
                         textcoords='offset pixels',
                         c="blue")
    
plt.plot(evotemps["1.0"], evolumin["1.0"], c="black", lw=2)
plt.scatter(m1plotdata[0], m1plotdata[1], c="green", lw=3)
plt.xlim(3.9, 3.6)
plt.title("M1.0 Star with 1-12 Gyr Isochrone Labels")
plt.ylabel("log(Luminosity)")
plt.xlabel("log(Temperature)")
plt.show()


# In[ ]:




