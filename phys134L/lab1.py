#!/usr/bin/env python
# coding: utf-8

# ## Matthew Wong, Chris Temby, Lab 1

# In[1]:


import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from astropy.io import fits
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# import object.fits file
imagefile = os.path.join("object.fits")
image = fits.open(imagefile)[0].data


# Here I defined the function that shows the image. This was defined for convenience so I didn't have to copy and paste the plotting code every time.

# In[3]:


def plot_image(image):
    """
    INPUT: .fits image data
    OUTPUT: matplotlib plot
    DESC: plots the image data using log scaling and bone colormap
    and predetermined min/max values
    """
    
    FIG_X = 16
    FIG_Y = 14
    plt.figure(figsize=(FIG_X, FIG_Y))

    # hard-coded min, max values
    MIN = 40
    MAX = 600

    pcm = plt.pcolormesh(image, cmap="bone", shading="auto",
                         norm=colors.LogNorm(vmin=MIN, vmax=MAX))
    cb = plt.colorbar(pcm, extend="max")
    TICKS = [100, 200, 500, 1000]
    cb.set_ticks(TICKS)
    cb.set_ticklabels(TICKS)
    plt.axis("off")

plot_image(image)
plt.show()


# In[4]:


# import object.cat file
catalogfile = os.path.join("object.cat")
catalog = np.loadtxt(catalogfile)


# In[5]:


# extract the columns from the catalog
x_from_cat = catalog[:, 5]
y_from_cat = catalog[:, 6]
flags = catalog[:, 9]

plot_image(image)
plt.plot(x_from_cat, y_from_cat, marker='.', ls='', 
         alpha=0.6, color="green")
plt.show()


# In[6]:


# separate flagged and unflagged objects
x_flagged = x_from_cat[np.where(flags != 0)]
y_flagged = y_from_cat[np.where(flags != 0)]
x_unflagged = x_from_cat[np.where(flags == 0)]
y_unflagged = y_from_cat[np.where(flags == 0)]

plot_image(image)
plt.plot(x_flagged, y_flagged, marker='.', ls='', 
         color="green", alpha=0.6, label="Flagged")
plt.plot(x_unflagged, y_unflagged, marker='.', ls='', 
         color="red", alpha=0.5, label="Unflagged")
plt.legend(loc="lower right")
plt.show()


# The flagged points seem to be brighter than the unflagged ones. There are still some bright unflagged objects though. There are more flagged points in the galaxy and the bright stars of the image are mostly highlighted green. According to the SExtractor manual, flags highlight errors, with the flag '2' corresponding to a deblended object.

# In[7]:


flux = catalog[:, 1]

def peak_value(x, y, r=2):
    """
    INPUT: x and y coordinates and (optional) 
           radius of pixels to search around
    OUTPUT: the peak value inside the region
    DESC.: this function looks at a certain part of the image 
           and outputs the greatest image value
           in the region defined by x +/- r and y +/- r
    """
    # ensure whole number
    x = int(np.round(x))
    y = int(np.round(y))
    w = len(image)
    h = len(image[0])
    # make sure the coordinates are actually in the image
    if x in range(len(image)+1) and y in range(len(image[0])+1):
        # if x-r would be negative, then take 
        # the distance between the left edge and x
        x_min = min(x, np.abs(x-r)) 
        # and if x+r would be greater than the width of the image, 
        # take the distance between the right edge and x
        x_max = w - min(np.abs(w - (x+r)), w - x)
        # do the same for y
        y_min = min(y, np.abs(y-r))
        y_max = h - min(np.abs(h - (y+r)), h - y)
        
        # the image coords are flipped for some reason
        search_area = image[y_min:y+r, x_min:x+r] 
        return np.amax(search_area)


# Below I test the peak value function. I took the first 3 data points in the objects.cat file and input their coordinates to the peak value function.

# In[13]:


peak_a = peak_value(1774, 29) # flux = 137552.5
peak_b = peak_value(1677, 26) # flux = 3778.12
peak_c = peak_value(965, 20)  # flux = 114508.3
flux_a = 137552.5
flux_b = 3778.12
flux_c = 114508.3
print(f"Peak values: {peak_a:.6f}, {peak_b:.6f}, {peak_c:.6f}")
# these are the ratios for flux/peak for each star
print(f"Peak/flux ratios: {flux_a / peak_a:.6f}"
      f"{flux_b / peak_b:.6f}, {flux_c / peak_c:.6f}")


# There seems to be a correlation between the peak value and the flux. The flux is roughly 20-ish times the peak value but varies due to photon noise.

# In[14]:


# pick out stars between 1990 and 2010
stars_x = x_from_cat[np.where(np.logical_and(flux >= 1990, 
                                             flux <= 2010))]
stars_y = y_from_cat[np.where(np.logical_and(flux >= 1990, 
                                             flux <= 2010))]

peak_values = [peak_value(stars_x[i], stars_y[i]) 
               for i in range(len(stars_x))]
print(f"Peak values: {peak_values}")

stdev = np.std(peak_values)
print(f"Std. Deviation: {stdev:.6f}")

# square root rule
# sigma^2 = mean counts
mean_peak_values = np.mean(peak_values)
print(f"Mean peak values: {mean_peak_values:.6f}")
print(f"Estimated Std. Deviation: {np.sqrt(mean_peak_values):.6f}")

# examine the data without the outlier
# created a copy to manipulate
peak_values_2 = peak_values.copy()
peak_values_2.pop(3)
stdev_2 = np.std(peak_values_2)
print(f"Std. Deviation (without outlier): {stdev_2:.6f}")
mean_peak_values_2 = np.mean(peak_values_2)
print(f"Mean peak values (without outlier): {mean_peak_values_2:.6f}")
print(f"Estimated Std. Deviation (without outlier): "
      f"{np.sqrt(mean_peak_values_2):.6f}")


# The actual standard deviation was higher than the estimated standard deviation using the square root rule for Poisson distributions in both cases. With the outlier removed it was a lot closer to the estimate. We think this is due to the image data being influenced by photon noise. The recorded peak values vary quite a bit from the mean, even though the flux data indicates the peak values should all be close to each other. Earlier, we showed that the ratio between flux and peak value measurement was very roughly 15:1 to 20:1. Given that we are analyzing a flux range of 20, this should correspond to the peak values being very close together. I would expect the peak values to be within 10 of each other, if this ratio were accurate. However, image noise caused the peak values to vary wildly, even introducing an outlier four times greater than expected. Another possible explanation could be due to the four smaller values bringing the mean down enough that the mean doesn't reflect the standard deviation particularly well. However, given that removing the outlier only dropped the standard deviation estimate by around 1.5, this explanation may not hold.

# In[10]:


# generate histograms for the fluxes
plt.figure(figsize=(12, 12))
plt.hist(flux)
plt.title("Stellar Flux Histogram")
plt.ylabel("Number of Stars")
plt.xlabel("Flux")
plt.show()


# In[11]:


plt.figure(figsize=(12, 12))
plt.hist(flux)
plt.yscale("log")
plt.title("Stellar Flux Histogram on a Logarithmic Scale")
plt.ylabel("Number of Stars")
plt.xlabel("Flux")
plt.show()


# The log scaled plot is much more informative because most of the plot points have very low flux so the unscaled plot only shows that there are a lot of objects with low brightness. The other bars are so small that it is too difficult to tell how many stars there are in the higher bins. With the scaled plot, it is much easier to see the frequency of stars with higher flux. It also shows that there is one really bright point, which we deduce to be the supernova.

# In[ ]:




