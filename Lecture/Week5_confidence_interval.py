#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMP9334

Demonstration on computing confidence interval
"""

import numpy as np
from scipy import stats

# mean response times from 5 independent replications
mrt = np.array([0.31, 0.37, 0.34, 0.36, 0.39])

# Confidence interval percentage (95% confidence interval)
alpha = 0.05

# Calculate mean and sample standard deviation
mean_mrt = np.mean(mrt)
std_mrt = np.std(mrt, ddof=1)  # SEE NOTES AT THE END OF THE FILE
print("mean and sample standard deviation: ", std_mrt)

# %% Calculations

# Number of tests
n = len(mrt)

mf = stats.t.ppf(1 - alpha / 2, n - 1) / np.sqrt(n)

confidence_interval = mean_mrt + np.array([-1, 1]) * mf * std_mrt

print('confidence interval: ', confidence_interval)



# %% Notes:
#
# If you use the numpy library to calculate sample standard deviation,
# you need to use include the option on ddof, i.e. you need to write
#
# np.std(mrt, ddof=1)
#
# for the example above.
# If you use the default, np.std(mrt) divides by sample size,
# not (sample size - 1)
#
# If you use the scipy.stats library to calculate sample standard deviation,
# you need to write
#
# np.std(mrt) <--- this is incorrect
#
# stats.tstd(mrt) <-- correct command
#
# for the example above.
