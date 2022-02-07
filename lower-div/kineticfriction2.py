#!/usr/bin/env python
# coding: utf-8

# ### Measuring Kinetic Friction More Accurately
# 2020-11-17 16:00
# 
# Last time, I measured the coefficient of kinetic friction using a slope. I only did 5 trials so an obvious way to reduce uncertainty would be to perform the experiment more times. For some reason, Phyphox measured a linear acceleration. After trying to measure the acceleration by pulling a mass along a flat surface, I found that the acceleration was more constant, so it turns out Phyphox doesn't calibrate the phone accelerometer with the slope. Thus, I am changing my experiment setup so that I can find the average acceleration. Also, the surface I used could have been too nonuniform, so I am using a mousepad instead, which is engineered to be uniformly smooth.
# 
# I attached a deck of cards to a hanging mass using a length of string. I then taped my phone on top of the deck of cards. The whole sliding setup was placed on a mousepad. Using the constraint that the length of the string is changing negligibly, and the assumption that the mass of the string is small compared to the rest of the system, I can write and solve Newton's laws (where $M$ is hanging mass and $m$ is mass of phone + card setup):
# 
# $$
# \begin{align}
# Mg &= T \\
# ma &= T - F_f \\
#    &= T - \mu_k mg \\
# ma &= Mg - \mu_k mg \\
# \mu_k &= \frac{Mg - ma}{mg}
# \end{align}
# $$
# 
# The uncertainty should be limited by the precision with which I can measure mass. I am using a gram-scale which measures to the nearest gram so my uncertainty is $0.001\ \mathrm{kg}\ /\,\sqrt{12} = 0.00029$ which is negligibly small.
# 
# The card/phone setup weighs 0.274 kg
# The hanging mass weighs 0.182 kg
# 
# Phyphox gives me a lot of values for acceleration over a length of time, so I manually found the intervals and averaged the values.

# In[9]:


import numpy as np

SLIDING_MASS = 0.274 # kg
HANGING_MASS = 0.182 # kg
GRAV_ACCEL = 9.81 # m/s^2

# list of accelerations for each trial (this is from taking the mean for a suitable time interval)
MEAN_ACCEL = [0.4088760, 0.4970091, 0.5039209, 0.4448318, 0.4888324, 
                     0.5222156, 0.4803040, 0.4228214, 0.5589495, 0.4123901]

mu_k = []
# calculate mu for each trial
for a in MEAN_ACCEL:
    # this is just the equation written above
    mu_k.append((HANGING_MASS * GRAV_ACCEL - SLIDING_MASS * a) / SLIDING_MASS / GRAV_ACCEL)

# output into table
print("Trial | Acceleration | Coefficient")
for i in range(len(mu_k)):
    print("{:>6}|{:^14.8f}|{:^14.8f}".format(str(i + 1) + " ",
          MEAN_ACCEL[i], mu_k[i]))


# In[12]:


mean_mu = np.mean(mu_k)
std_mu = np.std(mu_k)
uncertainty = std_mu / np.sqrt(len(mu_k))
print("COEFFICIENT = {} +/- {}".format(np.round(mean_mu, 4), np.round(uncertainty, 4)))


# ### Conclusion
# 2020-11-17 18:30
# #### Measured Value: 0.6159 +/- 0.0015
# 
# This time, I had a much smaller uncertainty compared to last week. Measuring horizontal acceleration with Phyphox is more reliable than measuring acceleration on a slope since it turned out to be fairly constant over a length of time. However, there was still a fair amount of noise in the data because the accelerometer is so sensitive so it was difficult to pick out the correct intervals when averaging the acceleration. Thus, although Phyphox produces data with more precision, there is a tradeoff in ease of use. 
# 
# Sources of uncertainty in this experiment were the string possibly stretching, human error when choosing the intervals to average over, unevenness in the surfaces, or the hanging mass swinging back and forth. I think the biggest source of error was human error in choosing the intervals to average over. Nonetheless, the uncertainty was quite low compared to last week, where I was getting uncertainties ranging from 0.0023 to 0.0081.
# 
# My lab-mates and I performed the experiment with similar materials, each testing with a deck of cards and a mousepad. We got somewhat similar coefficients of kinetic friction of around 0.4, 0.5, and 0.6. The differences in our measurements can be explained by different methods of collecting data, and differences in the materials themselves (we were not using the exact same deck of cards or mousepads). 
