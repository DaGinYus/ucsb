#!/usr/bin/env python
# coding: utf-8

# In[1]:


# setting plots up and importing necessary modules
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

plt.rcParams['figure.figsize'] = [12, 10]
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['font.size'] = 16
plt.rcParams['lines.linewidth'] = 2.0
plt.rcParams['lines.markersize'] = 8


# In[2]:


# data in time, voltage format (imported from webplotdigitizer)
# each unit corresponds to one division in the oscilloscope
# with my settings:
# HORIZ: 0.5 ms/div
# VERT: 8 V/div

RAW_DATA = [(-2.310763888888889, -0.6176315438034186),
            (-2.2171140491452994, -0.4521834935897431),
            (-2.1484375, -0.31441417378917436),
            (-2.067274305555556, -0.17141235500610552),
            (-1.9757055733618234, -0.03658631588319139),
            (-1.8737313034188037, 0.10534521901709404),
            (-1.7426215277777777, 0.24275507478632452),
            (-1.6052684294871793, 0.3647836538461542),
            (-1.4679153311965814, 0.4572983440170937),
            (-1.330562232905983, 0.5299479166666661),
            (-1.1932091346153846, 0.5861378205128198),
            (-1.0683426816239314, 0.6262464387464384),
            (-0.9185029380341878, 0.6604901175213675),
            (-0.7811498397435894, 0.6814903846153837),
            (-0.6437967414529915, 0.6945446047008543),
            (-0.5064436431623927, 0.7053285256410251),
            (-0.3690905448717947, 0.7053285256410251),
            (-0.23173744658119588, 0.7058961004273501),
            (-0.09438434829059794, 0.7053285256410251),
            (0.05268058523266905, 0.6990852029914527),
            (0.18032184829059883, 0.6922743055555549),
            (0.31767494658119677, 0.6735443376068369),
            (0.4175681089743595, 0.5517427884615378),
            (0.48000133547008605, 0.41438969017093985),
            (0.548677884615385, 0.2859853543447297),
            (0.6298410790598297, 0.14788900335775246),
            (0.7234909188034191, 0.008066447983440028),
            (0.8296274038461542, -0.12305137956179557),
            (0.9447820216049392, -0.24504392212725534),
            (1.0918469551282053, -0.36682024572649574),
            (1.2292000534188041, -0.45706463675213627),
            (1.366553151709402, -0.5263087606837606),
            (1.5039062500000009, -0.5790932158119659),
            (1.6412593482905988, -0.6199586004273501),
            (1.7786124465811977, -0.648904914529914),
            (1.9159655448717956, -0.669905181623931),
            (2.078291933760685, -0.6846621260683756),
            (2.215645032051283, -0.6931757478632479),
            (2.3529981303418808, -0.6931757478632479),
            (2.4903512286324796, -0.6931757478632479),
            (2.6277043269230775, -0.6892027243589745),
            (2.7650574252136764, -0.6806891025641022),
            (2.9024105235042743, -0.6710403311965809),
            (3.014790331196582, -0.6619591346153841)]


# In[3]:


# separate data into time, voltage arrays
time = []
voltage = []
for plotpoint in RAW_DATA:
    t = plotpoint[0]
    v = plotpoint[1]
    time.append(t)
    voltage.append(v)
    
time = np.array(time)
voltage = np.array(voltage)


# In[7]:


# plot the data I have
plt.plot(time, voltage)
plt.ylim(-3,3)
plt.show()


# In[5]:


# the cusp is at (0.31767494658119677, 0.6735443376068369)
# get the index of the cusp so I can split the data accordingly
cusp = RAW_DATA.index((0.31767494658119677, 0.6735443376068369))

# slice the arrays
charge_t = time[:cusp]
charge_v = voltage[:cusp]
disch_t = time[cusp+1:]
disch_v = voltage[cusp+1:]


# In[6]:


# get a fit for discharge cycle
def func(t, a, b, c, d):
    return a * np.exp(-b * (t - c)) + d

# returns fit and covariance matrix
popt, pcov = curve_fit(func, disch_t, disch_v)
perr = np.sqrt(np.abs(np.diag(pcov)))
print(f"sigma b = {perr[1]}")
plt.plot(disch_t, disch_v, label="discharge")
plt.plot(disch_t, func(disch_t, *popt), label="fit: a=%5.3f, b=%5.3f, c=%5.3f, d=%5.3f" % tuple(popt))
plt.legend()
plt.show()

