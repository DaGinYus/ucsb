#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# plot setup
plt.rcParams['figure.figsize'] = [12, 10]
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['font.size'] = 16
plt.rcParams['lines.linewidth'] = 2.0
plt.rcParams['lines.markersize'] = 8


# In[2]:


R = np.array([2.630, 2.565, 2.404, 2.032, 1.361, 0.747, 0.1807, 0.0763]) # kilo-ohms
u_R = 0.015 * R # from pamphlet
V = np.array([3.575, 3.730, 3.663, 3.474, 2.992, 2.222, 0.789, 0.3765]) # volts
u_V = 0.008 * V # from pamphlet

rho = stats.linregress(R, V)
x = np.arange(0, 3, 0.001)
y_fit = rho.slope * x + rho.intercept
y_upper = (rho.slope + rho.stderr) * x + (rho.intercept + rho.intercept_stderr)
y_lower = (rho.slope - rho.stderr) * x + (rho.intercept - rho.intercept_stderr)
print(f"{rho.slope} +/- {rho.stderr}")


# In[3]:


plt.errorbar(R, V, u_V, u_R, marker='x', ms=12, ls='', capsize=4)
plt.plot(x, y_fit, '-', label="V/R Fit")
plt.plot(x, y_upper, 'r--', label="Fit Stderr")
plt.plot(x, y_lower, 'r--')

plt.ylabel("Voltage(V)")
plt.xlabel("Resistance (Ohms)")
plt.minorticks_on()
plt.title("Voltage vs Resistance")
plt.legend()
plt.show()


# In[ ]:




