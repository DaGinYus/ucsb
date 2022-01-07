#!/usr/bin/env python
# coding: utf-8

# ## Faham & Matthew Lab 3

# In[1]:


import datetime
import os
import photutils
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.optimize import curve_fit
from scipy.spatial.distance import cdist
from astropy.io import fits
from astropy.stats import (biweight_location, 
                           sigma_clipped_stats)
from astropy import coordinates, time
from astropy import units as u
from photutils.aperture import aperture_photometry
from photutils.aperture import CircularAperture
from photutils.detection import DAOStarFinder
from photutils.segmentation import make_source_mask
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# read .fits and .cat file
imagefile = os.path.join("cluster1.fits")
image = fits.open(imagefile)[0].data
catfile = os.path.join("cluster1.cat")
catalog = np.loadtxt(catfile)


# In[3]:


# plot image overlaid with star position

plot_x = catalog[:, 1]
plot_y = catalog[:, 2]

def plot_image():
    """Plots the star image so I don't have to copy/paste
    """
    plt.figure(figsize=(18, 14))

    # hard-coded min, max values
    MIN = 500
    MAX = 1800

    pcm = plt.pcolormesh(image, cmap="bone", shading="auto",
                         norm=colors.LogNorm(vmin=MIN, vmax=MAX))
    cb = plt.colorbar(pcm, extend="max")
    TICKS = [100, 200, 500, 1000]
    cb.set_ticks(TICKS)
    cb.set_ticklabels(TICKS)
    plt.axis("off")

plot_image()
plt.plot(plot_x, plot_y, marker='.', ls='', 
         alpha=0.6, color="red")
plt.show()


# In[4]:


# extract and plot MAG_ISOCOR, MAGERR_ISOCOR
nums = catalog[:, 0]
mags = catalog[:, 5]
magerrs = catalog[:, 6]

plt.figure(figsize=(16, 14))
plt.errorbar(nums, mags, magerrs, ls='', marker='.', capsize=4)
plt.title("Magnitude of Stars")
plt.xlabel("Stars", fontsize=14)
plt.ylabel("Magnitude", fontsize=14)
plt.show()


# In[5]:


# sorted by magnitude on the horizontal axis
sorted_indices = np.argsort(mags)
sorted_mags = mags[sorted_indices]
sorted_magerr = magerrs[sorted_indices]

plt.figure(figsize=(16, 14))
plt.errorbar(nums, sorted_mags, sorted_magerr, ls='', marker='.', capsize=4)
plt.title("Sorted Magnitudes of Stars", fontsize=16)
plt.xlabel("Stars", fontsize=14)
plt.ylabel("Sorted Magnitudes", fontsize=14)
plt.show()


# In[6]:


# extract flux values
fluxes = catalog[:, 3]
fluxerrs = catalog[:, 4]

plt.figure(figsize=(16, 14))
plt.scatter(mags, fluxes)
plt.yscale("log")
plt.title("Flux vs. Magnitude", fontsize=16)
plt.xlabel("Magnitude", fontsize=14)
plt.ylabel("Flux", fontsize=14)
plt.show()


# In[7]:


# fitting a line to the data
def fit_func(x, a, b):
    return np.exp(-a * x + b)

xscale = np.linspace(np.amin(mags), np.amax(mags), 10)
popt, pcov = curve_fit(fit_func, mags, fluxes)
print(f"Fit: a={popt[0]}, b={popt[1]}")
print(f"b/a = {popt[1]/popt[0]}")
plt.figure(figsize=(16, 14))
plt.scatter(mags, fluxes)
plt.plot(xscale, fit_func(xscale, *popt), c='C1',
        label=f"Fit: a={popt[0]}, b={popt[1]}")
plt.legend()
plt.yscale("log")
plt.title("Fitted Flux/Magnitude Data", fontsize=16)
plt.xlabel("Magnitude", fontsize=14)
plt.ylabel("Flux", fontsize=14)
plt.show()


# In[8]:


fwhm = catalog[:, 12]
flags = catalog[:, -1]
# average fwhm of unflagged stars
avg_fwhm_unflag = np.mean(fwhm[np.where(flags == 0)])
print(avg_fwhm_unflag)

plt.figure(figsize=(16, 14))
plt.scatter(mags, fwhm)
plt.title("FWHM vs. Magnitude", fontsize=16)
plt.xlabel("Magnitude", fontsize=14)
plt.ylabel("FWHM (pixels)", fontsize=14)
plt.show()


# In[9]:


bg = catalog[:, -2]

plt.figure(figsize=(16, 14))
plt.scatter(plot_x, bg)
plt.title("Sky Background Flux (per pixel)", fontsize=16)
plt.xlabel("Position (x-axis, pixels)", fontsize=14)
plt.ylabel("Background Flux")
plt.show()


# In[10]:


plt.figure(figsize=(16, 14))
plt.plot(plot_x, bg, c="r")
plt.title("Bad Plot of Sky Background Flux (per pixel)", fontsize=16)
plt.xlabel("Position (x-axis, pixels)", fontsize=14)
plt.ylabel("Background Flux", fontsize=14)
plt.show()


# In[11]:


# bg flux statistics
print(f"Background Flux Mean: {np.mean(bg):.6f}")
print(f"Background Flux Stdev.: {np.std(bg):.6f}")


# In[12]:


plt.figure(figsize=(16, 14))
plt.scatter(mags, magerrs)
plt.title("Magnitude Error vs. Magnitude", fontsize=16)
plt.xlabel("Magnitude", fontsize=14)
plt.ylabel("Magnitude Error", fontsize=14)
plt.show()


# In[13]:


# overplot expected error in magnitude
def magerr_func(mag):
    """INPUT: x to plot
       OUTPUT: value of function
        
        1.086/sqrt(2.36)/flux * sqrt(exp(0.921*mag + 8.518e-5)+38740)
        
    """
    flux = np.exp(-0.921*mag + 7.85e-05)
    return 1.086/np.sqrt(2.36) * np.sqrt(flux + 38740)/flux

plot_x2 = np.arange(int(np.amin(mags)), int(np.amax(mags)) + 1)

plt.figure(figsize=(16, 14))
plt.scatter(mags, magerrs)
plt.plot(plot_x2, magerr_func(plot_x2), lw=4, color="red")
plt.title("Magnitude Error with Estimate", fontsize=16)
plt.xlabel("Magnitude", fontsize=14)
plt.ylabel("Magnitude Error", fontsize=14)
plt.show()


# The exponential plot seems to blow up too quickly. Some testing shows that the value of 7.85e-05 in the argument of the function seems too small. However, this is what the fitted data told me. Testing a value of 1.5 manually seems to give a better fit, but doing so would interfere with the fit of the flux function.

# In[14]:


# comparing MAG_ISOCOR and MAG_APER
aper = catalog[:, 9]
# there are some extreme outliers
# clean the inputs that are way too big
aper_clean = aper[np.where(aper < 40)]
# exclude the corresponding x-coords
mags_excl = mags[np.where(aper < 40)]

fig, (ax1, ax2) = plt.subplots(2, figsize=(16, 14))
ax1.scatter(mags_excl, aper_clean)
ax1.set_title("Aperture vs. Isophotal Photometry", fontsize=16)
ax1.set_ylabel("Aperture", fontsize=14)
ax1.set_xlabel("Isophotal", fontsize=14)
ax2.scatter(mags_excl, mags_excl-aper_clean)
ax2.set_ylabel("Isophotal, aperture difference", fontsize=14)
ax2.set_xlabel("Isophotal", fontsize=14)
fig.show(warn=False)


# In[15]:


# find the 3 worst outliers
outliers = np.argpartition(aper, -3)[-3:]
outlier_pos = zip(plot_x[outliers], plot_y[outliers])
print(f"Outlier Aperture Value:\n{aper[outliers]}")
print(f"Outlier (x, y) values:")
print([x for x in outlier_pos])


# In[16]:


# stats for background noise
bg_median = np.median(image)
print(f"Median: {bg_median}")
bg_biweight = biweight_location(image)
print(f"Biweight Location: {bg_biweight}")


# In[17]:


# perform sigma clipping stats
print("Mean, Median, Stdev.:")
sigma_clipped = sigma_clipped_stats(image,
                                    sigma=3.0)
print(sigma_clipped)

# perform source masking for an even better estimate
mask = make_source_mask(image, nsigma=2, npixels=5)
masked = sigma_clipped_stats(image, 
                             sigma=3.0, mask=mask)
print(masked)


# In[18]:


# find sources in image
# ripped from photutils documentation:
# https://photutils.readthedocs.io/en/stable/detection.html

(bg_mean, bg_median, bg_std) = masked
daofind = DAOStarFinder(fwhm=6.0, threshold=4*bg_std)
sources = daofind(image - bg_median)
for col in sources.colnames:  
    sources[col].info.format = '%.8g'
print(sources)


# In[19]:


# plot sources
# also ripped from docs
positions = np.transpose((sources['xcentroid'], sources['ycentroid']))
apertures = CircularAperture(positions, r=13)
plot_image()
apertures.plot(color='green', lw=1.5, alpha=0.7)
plt.show()


# In[20]:


# extract photometry
# mostly from https://photutils.readthedocs.io/en/stable/aperture.html
phot_table = aperture_photometry(image - bg_median, apertures)
phot_table["aperture_sum"].info.format = "%.8g"
print(phot_table)


# In[21]:


# plot vs sextractor values
# zip into position tuples to compare tuples directly
sex_pos = np.array(list(zip(plot_x, plot_y)), dtype=float)
phot_pos = np.array(list(zip(phot_table["xcenter"].value,
                             phot_table["ycenter"].value)), 
                    dtype=float)
# sort phot and take corresponding sextractor values
sort = np.argsort(phot_pos[:,0])
phot_sort = phot_pos[sort]
sex_index = []
for pos in phot_sort:
    distances = cdist(np.array([pos]), sex_pos)
    sex_index.append(np.argmin(distances))

# plot our photometry vs sextractor photometry
flux_aper = catalog[:,7]
phot_aper = phot_table["aperture_sum"][sort]
sex_aper = flux_aper[sex_index]

plt.figure(figsize=(16, 14))
x_range = np.linspace(0, np.max(sex_aper), 100)
plt.scatter(sex_aper, phot_aper)
plt.plot(x_range, x_range, c="C1")
plt.title("Aperture Photometry Comparison", fontsize=16)
plt.xlabel("SExtractor Flux", fontsize=14)
plt.ylabel("photutils Flux", fontsize=14)
plt.show()


# In[22]:


# same deal with a different radius
apertures_2 = CircularAperture(positions, r=6)

phot_table_2 = aperture_photometry(image, apertures_2)
# plot vs sextractor values
# zip into position tuples to compare tuples directly
sex_pos_2 = np.array(list(zip(plot_x, plot_y)), dtype=float)
phot_pos_2 = np.array(list(zip(phot_table_2["xcenter"].value,
                               phot_table_2["ycenter"].value)), 
                      dtype=float)
# sort phot and take corresponding sextractor values
sort_2 = np.argsort(phot_pos[:,0])
phot_sort_2 = phot_pos[sort]
sex_index_2 = []
for pos in phot_sort_2:
    distances = cdist(np.array([pos]), sex_pos_2)
    sex_index_2.append(np.argmin(distances))

# plot our photometry vs sextractor photometry
phot_aper_2 = phot_table_2["aperture_sum"][sort_2]
sex_aper_2 = flux_aper[sex_index_2]

plt.figure(figsize=(16, 14))
x_range = np.linspace(0, np.max(sex_aper_2), 100)
plt.scatter(sex_aper_2, phot_aper_2)
plt.plot(x_range, x_range, c="C1")
plt.title("Aperture Photometry Comparison v2", fontsize=16)
plt.xlabel("SExtractor Flux", fontsize=14)
plt.ylabel("photutils Flux", fontsize=14)
plt.show()


# In[23]:


# calculate error array
gain = 2.36
error_array = np.sqrt(image*gain)

SNR_indices = (21, 236, 84)
SNR = [[] for x in range(3)]
radii = np.linspace(0.1, 15, 150)
for rad in radii:
    aper_r = CircularAperture(positions, r=rad)
    phot_r = aperture_photometry(image - bg_median,
                                 aper_r, error=error_array)
    for i, j in enumerate(SNR_indices):
        SNR[i].append(phot_r["aperture_sum"][j]
                      / phot_r["aperture_sum_err"][j])

fig, axes = plt.subplots(3, figsize=(16, 30))
for i, ax in enumerate(axes):
    ax.plot(radii, SNR[i], label=f"Max Radius: {radii[np.argmax(SNR[i])]}")
    ax.set_title(f"Signal to Noise Ratio for Star # {SNR_indices[i]}",
                 fontsize=16)
    ax.set_ylabel("Signal to Noise Ratio", fontsize=14)
    ax.set_xlabel("Radius", fontsize=14)
    ax.legend()
fig.show(warn=False)


# In[24]:


# get aperture values at optimal radii for each star
N_ap = []
N_ap_err = []
for i, star_SNR in enumerate(SNR):
    best_r = radii[np.argmax(star_SNR)]
    aper_r = CircularAperture(positions, r=best_r)
    phot_r = aperture_photometry(image - bg_median,
                                 aper_r, error=error_array)
    N_ap.append(phot_r["aperture_sum"][SNR_indices[i]])
    N_ap_err.append(phot_r["aperture_sum_err"][SNR_indices[i]])

calc_m = []
calc_m_err = []
for i, n in enumerate(N_ap):
    calc_m.append(-2.5 * np.log10(n))
    calc_m_err.append(np.abs(-2.5/np.log(10)/n * N_ap_err[i]))
    
print(calc_m)
print(calc_m_err)


# In[25]:


# find the 4 stars' indices
star_pos = [(706.935, 60.4722), (312.028, 111.861),
            (283.167, 839.0), (1309.33, 771.944)]
star_indices = []
star_SNR = [[] for x in range(4)]
for star in star_pos:
    dist = cdist(np.array([star]), phot_pos)
    star_indices.append(np.argmin(dist))
print(star_indices)
# do the same thing for these stars
for rad in radii:
    aper_r = CircularAperture(positions, r=rad)
    phot_r = aperture_photometry(image - bg_median,
                                 aper_r, error=error_array)
    for i, j in enumerate(star_indices):
        star_SNR[i].append(phot_r["aperture_sum"][j]
                           / phot_r["aperture_sum_err"][j])
N_ap_2 = []
N_ap_err_2 = []
for i, star in enumerate(star_SNR):
    best_r = radii[np.argmax(star)]
    aper_r = CircularAperture(positions, r=best_r)
    phot_r = aperture_photometry(image - bg_median,
                                 aper_r, error=error_array)
    N_ap_2.append(phot_r["aperture_sum"][star_indices[i]])
    N_ap_err_2.append(phot_r["aperture_sum_err"][star_indices[i]])

calc_m_2 = []
calc_m_err_2 = []
for i, n in enumerate(N_ap_2):
    calc_m_2.append(-2.5 * np.log10(n))
    calc_m_err_2.append(np.abs(-2.5/np.log(10)/n * N_ap_err_2[i]))
    
print(calc_m_2)
print(calc_m_err_2)


# In[ ]:




