#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import random
import sys
from scipy import stats

import matplotlib.pyplot as plt
import numpy as np
import os


def Generate_inter_arrival_time_plot(File_Number):
    inter_arrival_file = os.path.join('inter_arrival_' + str(File_Number) + ".txt")
    f = open(inter_arrival_file, "r")
    lamb = float(f.readline())
    x = f.readline().split(", ")
    inter_arrival_list = list(np.float_(x))

    len_inter_arrival = len(inter_arrival_list)

    counter = 0
    for i in inter_arrival_list:
        counter = counter + i

    freq, bin_edges = np.histogram(inter_arrival_list, bins=50, range=(0, np.max(inter_arrival_list)))
    # Lower and upper limits of the bins
    bin_lower = bin_edges[:-1]
    bin_upper = bin_edges[1:]

    bin_center = (bin_lower + bin_upper) / 2
    bin_width = bin_edges[1] - bin_edges[0]
    y_expected = len_inter_arrival * (np.exp(-lamb * bin_lower) - np.exp(-lamb * bin_upper))
    plt.xlabel('Inter-arrival time, Lambda = ' + str(lamb))
    plt.hist(inter_arrival_list, bins=50, density=0, facecolor="blue", edgecolor="black")
    plt.plot(bin_center, y_expected, 'r--', label='Expected')
    plt.legend()
    plt.title('Random Mode - ' + str(File_Number) + ' - Exponentially Distributed Inter-arrival Times')
    plt.savefig("Inter_Arrival_graph_" + str(File_Number) + ".png")


def Generate_subJob_plot(File_Number):
    no_sub_job_file = os.path.join('sub_job_service_time_' + str(File_Number) + ".txt")
    f = open(no_sub_job_file, "r")
    p_sequence = np.float_(eval(f.readline()))
    num_sub_Job = eval(f.readline())
    max_subjob_no = len(p_sequence)

    # x-Axis show
    sub_job_X_axis = []
    for i in range(0, len(p_sequence)):
        sub_job_X_axis.append(i + 1)

    # Get Job Counter
    sub_num_counter = np.int_(list(("0" * max_subjob_no)))
    sub_num_counter_in_percentage = []
    for i in range(0, len(num_sub_Job)):
        if num_sub_Job[i]:
            sub_num_counter[len(num_sub_Job[i]) - 1] = sub_num_counter[len(num_sub_Job[i]) - 1] + 1

    for i in range(0, max_subjob_no):
        sub_num_counter_in_percentage.append(round(sub_num_counter[i] / len(num_sub_Job), 3))

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(sub_job_X_axis, sub_num_counter_in_percentage, color='maroon', width=0.4)

    plt.xlabel("sub_job number")
    plt.ylabel("Number of sub-job per arrival / Total Number of Sub-job (Percentage)")
    plt.title("Probability Distribution of Number of sub-jobs - Sample " + str(File_Number) + "\n" + str(p_sequence))
    plt.savefig("Sub_job_prob_" + str(File_Number) + ".png")


def Generate_uniform_random(File_Number):
    no_sub_job_file = os.path.join('sub_job_service_time_' + str(File_Number) + ".txt")
    f = open(no_sub_job_file, "r")
    p_sequence = np.float_(eval(f.readline()))
    num_sub_Job = eval(f.readline())
    uniform_number_generate = eval(f.readline())

    temp_list = []

    for i in range(0, len(uniform_number_generate)):
        for j in range(0, len(uniform_number_generate[i])):
            temp_list.append(uniform_number_generate[i][j])

    plt.xlabel("Probability")
    plt.title(
        "Random.Uniform Distributed Number - Sample " + str(File_Number) + "\n" + "Sample Size: " + str(len(temp_list)))
    plt.hist(temp_list, bins=50, facecolor="blue", edgecolor="black")
    plt.savefig("Random_Uniform_Sample_" + str(File_Number) + ".png")


def Generate_subJob_Service_time(File_Number):
    no_sub_job_file = os.path.join('sub_job_service_time_' + str(File_Number) + ".txt")
    f = open(no_sub_job_file, "r")
    p_sequence = np.float_(eval(f.readline()))
    num_sub_Job = eval(f.readline())
    max_subjob_no = len(p_sequence)

    temp_List = []
    temp_Smallest = math.inf
    temp_Largest = 0

    for i in range(0, len(num_sub_Job)):
        for j in range(0, len(num_sub_Job[i])):
            if num_sub_Job[i][j] > temp_Largest:
                temp_Largest = num_sub_Job[i][j]
            if num_sub_Job[i][j] < temp_Smallest:
                temp_Smallest = num_sub_Job[i][j]
            temp_List.append(num_sub_Job[i][j])

    plt.hist(temp_List, bins=50, facecolor="blue", edgecolor="black")

    print("temp_Largest: ", temp_Largest)
    print("temp_Smallest: ", temp_Smallest)

    plt.xlabel("Service Time (Generate by CDF Function)")
    plt.title("Service Time Distribution - Sample " + str(File_Number))
    plt.savefig("Servce_Time_Distribution_" + str(File_Number) + ".png")


def generate_Reproducibility_plot():
    f = open("Reproducibility_random_100.txt", "r")
    value = eval(f.read())

    temp_max = 0
    temp_min = math.inf
    for i in value:
        if i > temp_max:
            temp_max = i
        elif i < temp_min:
            temp_min = i

    print(temp_min)
    print(temp_max)

    plt.ylim([1, 3])
    plt.plot(value)
    plt.xlabel("Times")
    plt.ylabel("Mean response Time")
    plt.savefig("Reproducibility_random.png")


def Generate_Job_Response_Time_Plot(File_Number):
    job_service_time = os.path.join('job_Response_time_' + str(File_Number) + ".txt")
    f = open(job_service_time, "r")
    service_time_val = eval(f.readline())
    print(len(service_time_val))

    line_array_list = []
    add_together = 0
    n = 2000
    counter = 1
    for i in range(0, len(service_time_val)):
        add_together = add_together + service_time_val[i]
        line_array_list.append(add_together/counter)
        counter = counter + 1

    y = [n, n]
    x = [0, 3]

    plt.plot(line_array_list)
    plt.plot(y, x)
    # plt.hist(service_time_val, bins=50, color='maroon', width=0.4)
    plt.title("Mean Response Time Line Graph")
    plt.xlabel("Number of jobs, h = 5, end_time = 5000")
    plt.ylabel("Mean Response Time")
    plt.show()
    # plt.savefig("Job_Response_Time_" + str(File_Number) + ".png")


if __name__ == "__main__":
    # Generate Graph for Internal Arrival Time
    for i in range(5, 8, 1):
        Generate_inter_arrival_time_plot(i)
        Generate_subJob_plot(i)
        Generate_subJob_Service_time(7)

    generate_Reproducibility_plot()
