#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


SLOPE_LENGTH = 45 # centimeters
PUCK_HEIGHTS = np.array([23.9, 23.1, 23.4, 23.3, 22.2, 25.1, 24.5, 23.9, 23.4, 26.3])
puck_angle = np.arcsin(PUCK_HEIGHTS / SLOPE_LENGTH) # theta = arcsin(h/l)
puck_static_mu = np.tan(puck_angle)


# In[3]:


# output into table
print("Hockey Puck")
print("Trial| Height (cm) | Angle (rad) | Coefficient ")
for i in range(len(PUCK_HEIGHTS)):
    print("{:>5}|{:^13}|{:^13.8f}|{:^13.8f}".format(str(i + 1) + " ",
          PUCK_HEIGHTS[i], np.round(puck_angle[i], 8), np.round(puck_static_mu[i], 8)))


# In[4]:


puck_static_mu_avg = np.mean(puck_static_mu)
puck_static_mu_sigma = np.std(puck_static_mu, ddof=1)
print("Hockey Puck Static Coefficient of Friction = {} +/- {}".format(puck_static_mu_avg, puck_static_mu_sigma))


# In[5]:


CAN_HEIGHTS = np.array([11.5, 11.7, 10.2, 10.8, 10.6, 9.2, 11.3, 8.9, 8.1, 8.7])
can_angle = np.arcsin(CAN_HEIGHTS / SLOPE_LENGTH)
can_static_mu = np.tan(can_angle)


# In[6]:


print("Tin Can")
print("Trial| Height (cm) | Angle (rad) | Coefficient ")
for i in range(len(CAN_HEIGHTS)):
    print("{:>5}|{:^13}|{:^13.8f}|{:^13.8f}".format(str(i + 1) + " ",
          CAN_HEIGHTS[i], np.round(can_angle[i], 8), np.round(can_static_mu[i], 8)))


# In[7]:


can_static_mu_avg = np.mean(can_static_mu)
can_static_mu_sigma = np.std(can_static_mu, ddof=1)
print("Tin Can Static Coefficient of Friction = {} +/- {}".format(can_static_mu_avg, can_static_mu_sigma))

