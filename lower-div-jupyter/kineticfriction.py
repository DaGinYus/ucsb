#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams['figure.figsize'] = [12, 10]
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['font.size'] = 16
plt.rcParams['lines.linewidth'] = 2.0
plt.rcParams['lines.markersize'] = 8


# In[2]:


# reads in each trial from excel file
# filenames are trial1.xls, trial2.xls, ...
trials = []
for i in range(5):
    trial = pd.read_excel("kineticfriction/trial" + str(i + 1) + ".xls")
    trials.append(trial)


# In[3]:


# I looked at the data manually to figure out the time intervals
# I set them each manually here (ugly, I know)
sets = [(14,102), (41,124), (34,104), (49,119), (68,148)]
for i in range(len(sets)):
    trials[i] = trials[i][sets[i][0]:sets[i][1]].reset_index()

# clean up the indices and redefine the time for them
TIMESTEP = 0.0100469999888446 # this is phyphox's polling frequency

for trial in trials:
    trial.insert(0, "Time", value = np.arange(0, len(trial.index)*TIMESTEP, TIMESTEP))
    trial.set_index("Time", inplace=True)


# In[4]:


# this is the data I got from phyphox
# I'm interested in the time from where the acceleration is nonzero but before the large spikes
for trial in trials:
    accel_plot = trial["Absolute acceleration (m/s^2)"].plot()
accel_plot.set_ylabel("Absolute acceleration (m/s^2)")
accel_plot.set_xlabel("Time (s)")


# In[5]:


# calculate friction
LENGTH = 58.2 # cm
HEIGHT = 30.0 # cm
theta = np.arcsin(HEIGHT / LENGTH)

for trial in trials:
    coefficient = []
    for index in trial.index:
        a = trial["Absolute acceleration (m/s^2)"][index]
        mu_k = np.tan(theta) - a / 9.8 / np.cos(theta)
        coefficient.append(mu_k)
    trial.insert(0, "Friction Coefficient", value=coefficient)
    friction_plot = trial["Friction Coefficient"].plot()
friction_plot.set_ylabel("Friction Coefficient")
friction_plot.set_xlabel("Time (s)")


# In[8]:


# find and plot mean friction coefficient at intervals of 0.1 seconds
# 0.1 seconds is roughly 10 intervals
plot_time = []
plot_data = []
for trial in trials:
    times = []
    datapoints = []
    for time, datapoint in trial["Friction Coefficient"].iloc[:70:10].iteritems(): # take every 10th datapoint
        times.append(time)
        datapoints.append(datapoint)
    plot_time = times
    plot_data.append(datapoints)
avg_friction = np.mean(plot_data, axis=0)
sigma_friction = np.std(plot_data, axis=0) / np.sqrt(len(plot_data))
print(avg_friction)
print(sigma_friction)


# In[9]:


plt.errorbar(plot_time, avg_friction, sigma_friction, marker='x', ms=15, ls='', capsize=5)
plt.ylabel("Friction Coefficient")
plt.xlabel("Time (s)")
plt.minorticks_on()
plt.title("Friction Coefficient vs Time")
plt.show()


# In[ ]:




