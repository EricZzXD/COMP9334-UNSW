#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMP9334 Week 4B, Lecture

Generate exponentially distributed random numbers


"""

import random
import matplotlib.pyplot as plt
import numpy as np

# To produce 10,000 numbers that are exponentially distributed
lamb = 2
n = 10000
x = []
for i in range(n):
    x.append(random.expovariate(lamb))

# To check the numbers are really exponentially distributed
# Plot an histogram of the number
nb = 50 # Number of bins in histogram
freq, bin_edges = np.histogram(x, bins = nb, range=(0,np.max(x)))

# Lower and upper limits of the bins
bin_lower = bin_edges[:-1]
bin_upper = bin_edges[1:]
# expected number of exponentially distributed numbers in each bin
y_expected = n*(np.exp(-lamb*bin_lower)-np.exp(-lamb*bin_upper))

bin_center = (bin_lower+bin_upper)/2
bin_width = bin_edges[1]-bin_edges[0]

plt.bar(bin_center,freq,width=bin_width)
plt.plot(bin_center,y_expected,'r--',label = 'Expected')
plt.legend()
plt.title('Histogram of 10^4 exponentially distributed psuedo-random numbers')
plt.savefig('hist_expon.png')

