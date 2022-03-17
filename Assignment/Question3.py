#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

n = 4
r1 = 2.7  # Request Rate 1
r2 = 1.5  # Request Rate 2
w1 = 10.4  # Class 1 Workload
w2 = 15.3  # Class 2 Workload
miu = 70  # µ -- Server Processing Rate

spw1 = (miu / w1)  # µ/w1
spw2 = (miu / w2)  # µ/w2

A1 = np.array([[r1 + r2, -spw1, -spw2, 0, 0, 0, 0, 0, 0],
               [-r1, (spw1 + r1 + r2), 0, -2 * spw1, -spw2, 0, 0, 0, 0],
               [-r2, 0, (spw2 + r1 + r2), 0, -spw1, -2 * spw2, 0, 0, 0],
               [0, -r1, 0, (2 * spw1 + r1 + r2), 0, 0, -3 * spw1, -spw2, 0],
               [0, -r2, -r1, 0, (spw2 + spw1 + r1), 0, 0, -2 * spw1, 0],
               [0, 0, -r2, 0, 0, 2 * spw2, 0, 0, 0],
               [0, 0, 0, -r1, 0, 0, 3 * spw1 + r1, 0, -4 * spw1],
               [0, 0, 0, -r2, -r1, 0, 0, spw2 + 2 * spw1, 0],
               [0, 0, 0, 0, 0, 0, -r1, 0, 4 * spw1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1]])
b1 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
Q3 = np.linalg.lstsq(A1, b1, rcond=None)[0]  # Only want the first output

# Assuming that n = 4, λ 1 = 2.7, λ 2 = 1.5, w1 = 10.4, w2 = 15.3 and µ = 70. Answer the following questions.
print("=" * 100 + "\n")
print("Q3_b_i")
print("P(0,0): ", Q3[0])  # 4 Server(s) Available
print("P(1,0): ", Q3[1])  # 3 Server(s) Available
print("P(0,1): ", Q3[2])  # 2 Server(s) Available
print("P(2,0): ", Q3[3])  # 2 Server(s) Available
print("P(1,1): ", Q3[4])  # 1 Server(s) Available
print("P(0,2): ", Q3[5])  # 0 Server(s) Available
print("P(3,0): ", Q3[6])  # 1 Server(s) Available
print("P(2,1): ", Q3[7])  # 0 Server(s) Available
print("P(4,0): ", Q3[8])  # 0 Server(s) Available


# Calculate the probability of Rejection (Class)
def pro_class_reject(pro_list):
    total = 0
    for i in pro_list:
        total += i
    return total
    # print(total)


# Calculate the probability of Rejection (Overall)
def pro_reject_overall(c_r1, c_r2, reject1, reject2):
    p_class1_income_request = c_r1 / (c_r1 + c_r2)
    p_class1_reject = p_class1_income_request * reject1
    p_class2_reject = (1 - p_class1_income_request) * reject2
    return p_class1_reject + p_class2_reject


# (ii)	Determine the probability that an arriving Class 1 request will be rejected. --> Only happen when servers busy
print("=" * 100 + "\n")
print("Q3_b_ii: ")
class1_reject_list = [Q3[8], Q3[5], Q3[7]]
pro_class1_reject = pro_class_reject(class1_reject_list)
print("Probability of reject Class 1 Request : ", pro_class1_reject)

# (iii)	Determine the probability that an arriving Class 2 request will be rejected. --> Only happen when one Server
print("=" * 100 + "\n")
print("Q3_b_iii: ")
class2_reject_list = [Q3[8], Q3[6], Q3[7], Q3[4], Q3[5]]
pro_class2_reject = pro_class_reject(class2_reject_list)
print("Probability of reject Class 2 Request : ", pro_class2_reject)

# (iv)(iv)	Determine the probability that an arriving request will be rejected.
print("=" * 100 + "\n")
print("Q3_b_iv: ")
print("Probability of Income Request got Rejected: ", pro_reject_overall(r1, r2, pro_class1_reject, pro_class2_reject))


# C) Assuming that λ 1 = 2,7, λ	Assuming that λ 1 = 2,7, λ 2 = 1,5, w1 = 10.4, w2 = 15.3 and µ = 70. What is the
# smallest value of n that can reduce the probability of rejecting an arriving request to a level lower than 0.05? 2
# = 1,5, w1 = 10.4, w2 = 15.3 and µ = 70. What is the smallest value of n that can reduce the probability of
# rejecting an arriving request to a level lower than 0.05?
A2 = np.array([[r1 + r2, -spw1, -spw2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [-r1, (spw1 + r1 + r2), 0, -2 * spw1, -spw2, 0, 0, 0, 0, 0, 0, 0],
               [-r2, 0, (spw2 + r1 + r2), 0, -spw1, -2 * spw2, 0, 0, 0, 0, 0, 0],
               [0, -r1, 0, (2 * spw1 + r1 + r2), 0, 0, -3 * spw1, -spw2, 0, 0, 0, 0],
               [0, -r2, -r1, 0, (spw2+spw1+r1+r2), 0, 0, -2 * spw1, -2*spw2, 0, 0, 0],
               [0, 0, -r2, 0, 0, (2*spw2+r1), 0, 0, -spw1, 0, 0, 0],
               [0, 0, 0, -r1, 0, 0, 3 * spw1 + r1 + r2, 0, 0, -4*spw1, -spw2, 0],
               [0, 0, 0, -r2, -r1, 0, 0, spw2 + 2*spw1 + r1, 0, 0, -3*spw1, 0],
               [0, 0, 0, 0, -r2, -r1, 0, 0, 2*spw2 + spw1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, -r1, 0, 0, 4*spw1+r1, 0, -5*spw1],
               [0, 0, 0, 0, 0, 0, -r2, -r1, 0, 0, spw2+3*spw1, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, -r1, 0, 5*spw1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
               ])
b2 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
Q3c = np.linalg.lstsq(A2, b2, rcond=None)[0]  # Only want the first output

# print("P(0,0): ", Q3c[0])  # 5 Server(s) Available
# print("P(1,0): ", Q3c[1])  # 4 Server(s) Available
# print("P(0,1): ", Q3c[2])  # 3 Server(s) Available
# print("P(2,0): ", Q3c[3])  # 3 Server(s) Available
# print("P(1,1): ", Q3c[4])  # 2 Server(s) Available
# print("P(0,2): ", Q3c[5])  # 1 Server(s) Available
# print("P(3,0): ", Q3c[6])  # 2 Server(s) Available
# print("P(2,1): ", Q3c[7])  # 1 Server(s) Available
# print("P(1,2): ", Q3c[8])  # 0 Server(s) Available
# print("P(4,0): ", Q3c[9])  # 1 Server(s) Available
# print("P(3,1): ", Q3c[10])  # 0 Server(s) Available
# print("P(5,0): ", Q3c[11])  # 0 Server(s) Available

# Class 1 rejection
Q3c_class1_reject_list = [Q3c[11], Q3c[10], Q3c[8]]
Q3c_pro_class1_reject = pro_class_reject(Q3c_class1_reject_list)

# Class 2 rejection
Q3c_class2_reject_list = [Q3c[11], Q3c[10], Q3c[8], Q3c[9], Q3c[7], Q3c[5]]
Q3c_pro_class2_reject = pro_class_reject(Q3c_class2_reject_list)

# Overall
print("=" * 100 + "\n")
print("Q3_c: ")
print("Probability of Income Request got Rejected: ", pro_reject_overall(r1, r2, Q3c_pro_class1_reject, Q3c_pro_class2_reject))