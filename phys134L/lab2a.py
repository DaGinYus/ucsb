#!/usr/bin/env python
# coding: utf-8

# ## Matthew Wong, Alice Yu Lab 2
# 

# In[1]:


import datetime
import os
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy import coordinates, time
from astropy import units as u
get_ipython().run_line_magic('matplotlib', 'inline')


# #### Part 2

# In[2]:


# import object.fits file
imagefile = os.path.join("object.fits")
image = fits.open(imagefile)[0].data
header = fits.open(imagefile)[0].header

# set MJD-OBS (Modified Julian Date)
mjd = header["MJD-OBS"]


# In[3]:


# create coordinate, loc, and time objects
radec = coordinates.SkyCoord(header["RA"], header["DEC"], 
                             unit=(u.hourangle, u.deg))
location = coordinates.EarthLocation(lon=header["LONGITUD"], 
                                     lat=header["LATITUDE"])
t = time.Time(header["MJD-OBS"], format="mjd")

# reference frame definition
frame_altaz = coordinates.AltAz(obstime=t, location=location)

# local sidereal time
lst = t.sidereal_time("apparent", header["LONGITUD"])
print(lst)


# The LST in the header file is 13:56:45.76, which is pretty close to the returned value of 13:56:46.03

# In[4]:


coord_altaz = radec.transform_to(frame_altaz)
altitude = coord_altaz.alt
print(altitude)


# The altitude value in the header file is 74.1248588 degrees. If we take 74 + 7/60 + 30.38196351/360 (converting the format to just degrees), we get 74.20106101 degrees.

# In[5]:


# define function to check values at different times
def time_shifted_alt(header, hr):
    """
    INPUT: Header file, Hour offset (signed float)
    OUTPUT: Altitude values in deg-min-sec
    DESC.: Outputs the altitude value in degrees based on an offset from 
    the MJD in the header file.
    """
    mjd = header["MJD-OBS"]
    new_mjd = mjd + hr/24
    new_t = time.Time(new_mjd, format="mjd")
    
    radec = coordinates.SkyCoord(header["RA"], header["DEC"], 
                                 unit=(u.hourangle, u.deg))
    location = coordinates.EarthLocation(lon=header["LONGITUD"], 
                                         lat=header["LATITUDE"])
    frame_altaz = coordinates.AltAz(obstime=new_t, 
                                    location=location)
    coord_altaz = radec.transform_to(frame_altaz)
    return coord_altaz.alt


# In[6]:


# answers to questions 1-5 on page 6
# question 1
print(f"Altitude 1 Hour Before: {time_shifted_alt(header, -1)}")
# question 2
print(f"Altitude 2 Hours After: {time_shifted_alt(header, 2)}")

# question 3
# zenith when object passes through N-S plane
# take abs(declination - latitude) to find the zenith angle
# LST corresponds to the RA of the object
zenith = np.abs(radec.dec.degree - header["LATITUDE"])
print(f"Zenith Angle: {zenith} deg")
print(f"LST at Zenith: {header['RA']}")

# question 4
# find the altitude at a range of 1000 evenly spaced times after
# the observation time, up to 12 hours after, then compare to 
# elevation angle of 40
times = np.linspace(0, 12, 1000)
elev_angle = coordinates.Angle(40, unit=u.deg)
for delta_t in times:
    current_alt = time_shifted_alt(header, delta_t)
    angle_diff = current_alt - elev_angle
    if (angle_diff >= 0
        and angle_diff < coordinates.Angle(0.1, unit=u.deg)):
        time_diff = delta_t
        break
print(f"Time until 40 deg elevation: "
      f"{datetime.timedelta(hours=time_diff)}")

