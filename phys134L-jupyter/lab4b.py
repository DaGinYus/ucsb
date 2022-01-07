#!/usr/bin/env python
# coding: utf-8

# In[98]:


import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from astropy.io import fits
from astropy.visualization import make_lupton_rgb
from astropy.stats import (biweight_location, 
                           sigma_clipped_stats)
from photutils.aperture import aperture_photometry
from photutils.aperture import CircularAperture
from photutils.detection import DAOStarFinder
from photutils.segmentation import make_source_mask
get_ipython().run_line_magic('matplotlib', 'inline')


# In[251]:


def img_preprocess(fpath, fext=".fits", bprefix="c_b_",
                   dprefix="c_d_", fprefix="c_f_",
                   eprefix="c_e_", filters=["B", "V", "i"],
                   expfilters=["B", "V", "i"],
                   searchstring=""):
    """Preprocesses a given image given bias, dark, and flat frames.
       Input:
           fpath: file path to image data as a list-like object
           fext: the file extension
           bprefix: the prefix for bias frames
           dprefix: the prefix for dark frames
           fprefix: the prefix for flat frames
           eprefix: the prefix for exposures
           filters: the filter names for flat frames
           expfilters: the filter names for exposures
           searchstring: a specific name to look for in
                         the filenames
       Output: Reduced .fits image files per each filter, 
               written to out/(processed images).fits
    """
    prefixes = {"bias": bprefix,
                "dark": dprefix, 
                "flat": fprefix, 
                "exp": eprefix}
    imgpaths = {name: os.path.join(*fpath, pre+"*"+fext)
                for name, pre in prefixes.items()}
    images = {name: glob.glob(imgpath)
              for name, imgpath in imgpaths.items()}
    print(f"{len(images)} images found")
    frame = {}
    # bias
    biasframes = [fits.open(img)[0].data
                  for img in images["bias"]]
    print(f"{len(biasframes)} bias frames found")
    frame["bias"] = np.median(np.array(biasframes), axis=0)
    print("bias correction complete")
    # dark
    darkframes = [(fits.open(img)[0].data - frame["bias"])
                  for img in images["dark"]]
    print(f"{len(darkframes)} dark frames found")
    frame["dark"] = np.median(np.array(darkframes), axis=0)
    print("dark correction complete")
    # flat
    # do this per filter
    filtframes = {filt: [] for filt in filters}
    for filt in filters:
        for img in images["flat"]:
            if "_"+filt+fext in img:
                exptime = fits.open(img)[0].header["EXPTIME"]
                filtframes[filt].append(fits.open(img)[0].data
                                        - frame["bias"] 
                                        - exptime*frame["dark"])
                filtframes[filt][-1] /= np.median(filtframes[filt][-1])
        print(f"{len(filtframes[filt])}"
              f" flats processed for {filt} filter")
    filtframes = {key: np.median(np.array(val), axis=0)
                  for key, val in filtframes.items()}
    frame["flat"] = {key: val / np.median(val)
                     for key, val in filtframes.items()}
    print("flat field correction complete")
    # image stacking
    for efilt in expfilters:
        scistack = []
        for img in images["exp"]:
            if "_"+efilt+fext in img and searchstring in img:
                hdu = fits.open(img)[0]
                sci = ((hdu.data - frame["bias"] - frame["dark"])
                      /frame["flat"][filt])
                hdu.data = sci
                outfile = os.path.join(*fpath, "out", 
                                       os.path.basename(img))
                outfile = outfile.replace(".fits", "_cal.fits")
                with open(outfile, mode="wb") as f:
                    hdu.writeto(f, overwrite=True)
                scistack.append(sci)
        print(f"{len(scistack)} images calibrated for {efilt} filter")
        scistack = np.median(np.array(scistack), axis=0)
        hdulist = fits.HDUList(fits.PrimaryHDU(scistack))
        outfile = os.path.join(*fpath, "out",
                               "median_combined_image_"+efilt+".fits")
        hdulist.writeto(outfile, overwrite=True)
    print("image preprocessing complete")


# In[261]:


img_preprocess(("data", "20110428_raw"), searchstring="m51")


# In[262]:


# side by side comparison
# m51-001_B calibrated vs uncalibrated

uncal = fits.open(os.path.join("data", "20110428_raw",
                  "c_e_20110428_m51-001_B.fits"))[0].data
cal = fits.open(os.path.join("data", "20110428_raw", "out",
                "c_e_20110428_m51-001_B_cal.fits"))[0].data

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 20))
ax1.imshow(uncal, cmap="gray", norm=LogNorm(vmin=1300, vmax=1400),
           interpolation="none")
ax2.imshow(cal, cmap="gray", norm=LogNorm(vmin=60, vmax=150),
           interpolation="none")
ax1.set_title("uncalibrated", fontsize=16)
ax2.set_title("calibrated", fontsize=16)
ax1.axis("off")
ax2.axis("off")
fig.subplots_adjust(wspace=0.05)
plt.show()


# In[264]:


# generating an RGB image
image_r = fits.open(os.path.join("data", "20110428_raw", "out",
                    "median_combined_image_i.fits"))[0].data
image_g = fits.open(os.path.join("data", "20110428_raw", "out",
                    "median_combined_image_V.fits"))[0].data
image_b = fits.open(os.path.join("data", "20110428_raw", "out",
                    "median_combined_image_B.fits"))[0].data
r = image_r/np.max(image_r)*12
g = image_g/np.max(image_g)*20
b = image_b/np.max(image_b)*90
print([np.median(val) for val in (r, g, b)])
rgb_image = make_lupton_rgb(r, g, b, Q=0.1, stretch=0.7, minimum=0.09)
plt.figure(figsize=(12, 10))
plt.imshow(rgb_image, origin="lower", interpolation="none")
plt.axis("off")
plt.show()


# In[265]:


# m67 processing
img_preprocess(("data", "20110427_raw"), filters=["B", "V"],
               expfilters=["Bl", "Vl"], searchstring="m67")


# In[273]:


# photometry
B_imagepath = os.path.join("data", "20110427_raw", "out",
                           "median_combined_image_Bl.fits")
V_imagepath = os.path.join("data", "20110427_raw", "out",
                           "median_combined_image_Vl.fits")

# background subtraction
BV_images = [fits.open(f)[0].data 
             for f in (B_imagepath, V_imagepath)]
BV_mask = [make_source_mask(img, nsigma=2, npixels=5)
             for img in BV_images]
BV_sigma_clips = [sigma_clipped_stats(img, sigma=3.0, mask=BV_mask[i]) 
                  for i, img in enumerate(BV_images)]
BV_bg_median = [BV_sigma_clips[i][1]
                for i,j in enumerate(BV_sigma_clips)]
BV_bg_std = [BV_sigma_clips[i][2] 
             for i,j in enumerate(BV_sigma_clips)]
# find sources
BV_daofind = [DAOStarFinder(fwhm=6.0, threshold=4*bg_std)
              for bg_std in BV_bg_std]
BV_sources = [BV_daofind[i](img - BV_bg_median[i])
              for i, img in enumerate(BV_images)]
for sources in BV_sources:
    for col in sources.colnames:
        sources[col].info.format = '%.8g'
    
BV_positions = [np.transpose((sources['xcentroid'], sources['ycentroid']))
                for sources in BV_sources]
BV_apertures = [CircularAperture(positions, r=1)
                for positions in BV_positions]
BV_phot = [aperture_photometry(img - BV_bg_median[i], BV_apertures[i])
           for i, img in enumerate(BV_images)]
print(BV_phot)


# In[283]:


# cross matching between lists
B_coords = list(zip(BV_phot[0]["xcenter"].value, 
                    BV_phot[0]["ycenter"].value))
V_x = BV_phot[1]["xcenter"].value
V_y = BV_phot[1]["ycenter"].value
r_threshold = 2
xoffset = 0.2762
yoffset = -0.7264
matched_coords = [[], []]
for i, coord in enumerate(B_coords):
    # minimize distance
    r = np.sqrt((V_x - coord[0] - xoffset)**2
               +(V_y - coord[1] - yoffset)**2)
    thresh = np.where(r < r_threshold)[0]
    if thresh.size:
        matched_coords[0].append(i)
        matched_coords[1].append(thresh[np.argmin(r[thresh])])
print(f"{len(matched_coords[0])} cross matches found")


# In[292]:


def star_match(pos):
    """Finds the star nearest to specified coords.
       Outputs the data in B, V rows respectively.
    """
    out = []
    match_thresh = 5
    x = [BV_phot[i]["xcenter"].value 
         for i,p in enumerate(BV_phot)]
    y = [BV_phot[i]["ycenter"].value 
         for i,p in enumerate(BV_phot)]
    r = [np.sqrt((x[i] - pos[0])**2 + (y[i] - pos[1])**2)
         for i,p in enumerate(x)]
    thresh = [np.where(r[i] < match_thresh)[0]
              for i,p in enumerate(r)]
    if thresh[0].size and thresh[1].size:
        apsum = [BV_phot[i]["aperture_sum"]
                 [thresh[i][np.argmin(r[i][thresh[i]])]]
                 for i,p in enumerate(BV_phot)]
        return(-2.5*np.log10(np.array(apsum)))

# finding 5 stars for absolute calibration
# TYC814-1795-1
# located at (1100, 738) from ds9
print("\nTYC814-1795-1")
print(star_match((1100, 738)))
# TYC814-2331-1
# located at (955, 736) from ds9
print("\nTYC814-2331-1")
print(star_match((955, 736)))
# TYC814-1515-1
# located at (633, 540) from ds9
print("\nTYC814-1515-1")
print(star_match((633, 540)))
# TYC814-1823-1
# located at (280, 840) from ds9
print("\nTYC814-1823-1")
print(star_match((280, 840)))
# TYC814-1531-1
# located at (814, 456) from ds9
print("\nTYC814-1531-1")
print(star_match((814, 456)))


# In[312]:


# making HR diagram
B_aper = BV_phot[0]["aperture_sum"].value[matched_coords[0]]
V_aper = BV_phot[1]["aperture_sum"].value[matched_coords[1]]
B_mags = -2.5*np.log10(B_aper)
V_mags = -2.5*np.log10(V_aper)
# mean ZP manually calculated from sky-map comparison
B_mean_zp = np.mean((22.0, 22.551, 22.612, 21.981, 22.367))
V_mean_zp = np.mean((22.432, 22.709, 22.72, 22.598, 22.501))
# add this mean to get absolute B, V
B_abs = B_mags + B_mean_zp
V_abs = V_mags + V_mean_zp
BV_color = B_abs - V_abs

# isochrones
isochrones = np.loadtxt("lj98m01757.txt")

plt.figure(figsize=(16, 14))
plt.scatter(BV_color, V_abs)
plt.title("HR Diagram", fontsize=16)
plt.xlabel("B-V Color", fontsize=14)
plt.ylabel("V magnitude", fontsize=14)
plt.show()


# In[ ]:




