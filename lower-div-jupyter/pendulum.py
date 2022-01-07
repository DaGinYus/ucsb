#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['figure.figsize'] = [16, 12]
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['font.size'] = 16
plt.rcParams['lines.linewidth'] = 2.0
plt.rcParams['lines.markersize'] = 8

plt.rcParams['text.usetex'] = True


# In[2]:


get_ipython().run_cell_magic('html', '', '<style>\ntable {float:left}\n</style>')


# ### Data Table
# 
# Time for 10 Oscillations (in seconds):
# 
# | Trial | 20cm | 30cm  | 40cm  | 50cm  |
# |:------|:----:|:-----:|:-----:|:-----:|
# | 1     | 9.20 | 11.30 | 13.31 | 14.61 |
# | 2     | 9.40 | 11.35 | 13.58 | 14.65 |
# | 3     | 9.41 | 11.36 | 13.48 | 14.66 |
# | 4     | 9.45 | 11.36 | 13.38 | 14.68 |
# | 5     | 9.51 | 11.25 | 13.50 | 14.65 |
# | 6     | 9.48 | 11.36 | 13.46 | 14.53 |
# | 7     | 9.46 | 11.35 | 13.45 | 14.63 |
# | 8     | 9.45 | 11.40 | 13.51 | 14.78 |
# | 9     | 9.50 | 11.36 | 13.35 | 14.45 |
# | 10    | 9.45 | 11.33 | 13.45 | 14.70 |

# In[3]:


lengths = np.arange(20, 51, 10) # generate lengths: 20, 30, 40, 50

# data for pendulum measurements
# each row corresponds to a different length: 20cm, 30cm, 40cm, 50cm
data = np.array([[09.20, 09.40, 09.41, 09.45, 09.51, 09.48, 09.46, 09.45, 09.50, 09.45],
                 [11.30, 11.35, 11.36, 11.36, 11.25, 11.36, 11.35, 11.40, 11.36, 11.33],
                 [13.31, 13.58, 13.48, 13.38, 13.50, 13.46, 13.45, 13.51, 13.35, 13.45],
                 [14.61, 14.65, 14.66, 14.68, 14.65, 14.53, 14.63, 14.78, 14.45, 14.70]])

adj_data = np.divide(data, 10) # divide the periods by 10 to get time for one swing


# ### Analysis
# 
# Here I calculate the mean and average standard deviation for each length. I output the mean values into the array `T_avg`, which will be graphed on the y-axis later. `T_sigma` is an array containing the average uncertainty for each length, given by $\sigma_{avg} = \frac{\sigma}{\sqrt{N}}$ where N is the number of trials (in our case, 10).
# 
# The standard deviation, given by `np.std()` is calculated as follows:
# 
# \begin{align}
# \sigma = \sqrt{\frac{1}{N-1}\sum_{i=1}^N(x_i-\bar{x})^2}
# \end{align}

# In[4]:


T_avg = []
T_sigma = []

for item in adj_data:
    T_avg.append(np.mean(item))
    T_sigma.append(np.std(item, ddof=1) / np.sqrt(len(item)))
    
np.array(T_avg)
np.array(T_sigma)


# In[5]:


plt.errorbar(lengths, T_avg, T_sigma, marker='x', ms=15, ls='', capsize=5)
plt.ylabel("Period (s)")
plt.xlabel("Length (cm)")
plt.axis([10, 60, 0.8, 1.6]) # xmin, xmax, ymin, ymax
plt.minorticks_on()
plt.title("Period of Pendulum")
plt.show()


# In[ ]:




