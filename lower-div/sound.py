#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np

LENGTH = 0.5495
DATA = np.array([456, 447, 468, 468, 458, 458, 444, 458, 454, 476])
vel = 4 / 3 * LENGTH * DATA

print(vel)
print(f"{np.mean(vel)} +/- {np.std(vel, ddof=1)}")


# In[ ]:




