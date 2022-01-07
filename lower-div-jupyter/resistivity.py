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


# from calculated area (meters^2)
AREA = 0.0000196
U_AREA = 0.0000157

# from length measurement (meters)
LENGTH = [0.0749, 0.0607, 0.0448, 0.0309, 0.0147]
U_LENGTH = 0.0003

# from resistance measurement (ohms)
# (each array is the 5 trials for a specific length)
RESISTANCE = [[11.4, 11.9, 12.6, 10.6, 12.1],
              [8.3, 9.0, 10.5, 10.5, 9.6],
              [9.2, 6.0, 5.3, 9.6, 6.5],
              [4.7, 4.5, 3.5, 4.2, 3.9],
              [2.0, 2.5, 2.7, 2.4, 2.2]]

# calculating mean resistances and uncertainties for each length
avg_resistance = []
u_resistance = []
for i in range(len(RESISTANCE)):
    avg_resistance.append(np.mean(RESISTANCE[i]))
    u_resistance.append(1/np.sqrt(5) * np.std(RESISTANCE[i], ddof=1))
print(avg_resistance)
print(u_resistance)

# fitting
rho = stats.linregress(LENGTH, avg_resistance)
x = np.arange(0, 0.08, 0.001)
y_fit = rho.slope * x + rho.intercept
y_upper = (rho.slope + rho.stderr) * x + (rho.intercept + rho.intercept_stderr)
y_lower = (rho.slope - rho.stderr) * x + (rho.intercept - rho.intercept_stderr)
print(f"{rho.slope} +/- {rho.stderr}")


# In[3]:


plt.errorbar(LENGTH, avg_resistance, u_resistance, U_LENGTH, marker='x', ms=12, ls='', capsize=4)
plt.plot(x, y_fit, '-', label="R/L Fit")
plt.plot(x, y_upper, 'r--', label="Fit Stderr")
plt.plot(x, y_lower, 'r--')

plt.ylabel("Resistance (Ohms)")
plt.xlabel("Length (m)")
plt.minorticks_on()
plt.title("Resistivity vs Length")
plt.legend()
plt.show()


# In[ ]:




