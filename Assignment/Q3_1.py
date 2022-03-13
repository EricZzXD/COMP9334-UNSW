#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMP9334, Week 3B Lecture

Database server example
"""

import numpy as np

n = 4
r1 = 2.7  # Request Rate 1
r2 = 1.5  # Request Rate 2
w1 = 10.4  # Class 1 Workload
w2 = 15.3  # Class 2 Workload
miu = 70  # µ -- Server Processing Rate

spw1 = (miu / w1)  # µ/w1
spw2 = (miu / w2)  # µ/w2

print(spw1)  # µ/w1

A2 = np.array([[r1 + r2, -spw1, -spw2, 0, 0, 0, 0, 0, 0],
               [-r1, (spw1 + r1 + r2), 0, -spw1, -spw2, 0, 0, 0, 0],
               [-r2, 0, (spw2 + r1 + r2), 0, -spw1, -spw2, 0, 0, 0],
               [0, -r1, 0, (spw1 + r1 + r2), 0, 0, -spw1, -spw2, 0],
               [0, -r2, -r1, 0, (spw1 + spw2 + r1), 0, 0, -spw1, 0],
               [0, 0, -r2, 0, 0, spw2, 0, 0, 0],
               [0, 0, 0, -r1, 0, 0, (r1 + spw1), 0, -spw1],
               [0, 0, 0, -r2, -r1, 0, 0, (spw2 + spw2), 0],
               [0, 0, 0, 0, 0, 0, -r1, 0, spw1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1]])
b2 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
x2 = np.linalg.lstsq(A2, b2, rcond=None)[0]  # Only want the first output


# print(x2)

# Assuming that n = 4, λ 1 = 2.7, λ 2 = 1.5, w1 = 10.4, w2 = 15.3 and µ = 70. Answer the following questions.
print("Q3_b_ii")
print("P(0,0): ", x2[0])  # 4 Server(s) Available
print("P(1,0): ", x2[1])  # 3 Server(s) Available
print("P(0,1): ", x2[2])  # 2 Server(s) Available
print("P(2,0): ", x2[3])  # 2 Server(s) Available
print("P(1,1): ", x2[4])  # 1 Server(s) Available
print("P(0,2): ", x2[5])  # 0 Server(s) Available
print("P(3,0): ", x2[6])  # 1 Server(s) Available
print("P(2,1): ", x2[7])  # 1 Server(s) Available
print("P(4,0): ", x2[8])  # 0 Server(s) Available
print("="*100 + "\n")


# (ii)	Determine the probability that an arriving Class 1 request will be rejected. --> Only happen when servers busy
print("Q3_b_ii: ")
print("Probability of reject Class 1 Request : ", x2[8] + x2[7] + x2[3], "\n")

# (iii)	Determine the probability that an arriving Class 2 request will be rejected. --> Only happen when one Server
print("Q3_b_iii: ")
print("Probability of reject Class 2 Request : ", x2[4] + x2[5] + x2[6] + x2[7] + x2[8], "\n")



