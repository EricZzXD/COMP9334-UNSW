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


def Generate_Confidence_interval():
    mrt = np.array([1.8591160398116968, 1.8687710284637469, 1.9109791052396536, 1.835181289200024, 1.9024735951447769,
                    1.9134749376012585, 1.9151210710441453, 1.8719504131787639, 1.8853136503014212, 1.8436460717715752,
                    1.8472342892353049, 1.8889476842478767, 1.87222609841599, 1.8934249287679117, 1.8670341843458658,
                    1.86915061908208, 1.9198113813298177, 1.8890552174729247, 1.8638684676045212, 1.8815109521434765,
                    1.8623439832647433, 1.9016733272898116, 1.8644474127174602, 1.9238560977594927, 1.8854730692582888,
                    1.869697698642329, 1.9054566867794394, 1.8845735297230528, 1.8658270792519382, 1.8900660172983281,
                    1.8889430565824532, 1.9068837286304434, 1.8891153361597521, 1.9149241874928198, 1.881738579692729,
                    1.9097085905686404, 1.9446159398377545, 1.8651498013626902, 1.956473680167565, 1.850891661939084,
                    1.8820327580782132, 1.907870704823437, 1.89549074835089, 1.9089630023846067, 1.9236363923591953,
                    1.859061220772439, 1.8627465576756146, 1.9140714043718616, 1.856546265673434, 1.8932962065647256,
                    1.8753404549957424, 1.9091005451718965, 1.8917064643042347, 1.8622606477358765, 1.9119039908380604,
                    1.9227426915189967, 1.9188556818403961, 1.9225580116703906, 1.8930800344544287, 1.8590187824846929,
                    1.8931681738552104, 1.9114291993432355, 1.8673458419552846, 1.8787187725905177, 1.8787624307937318,
                    1.8987175293173553, 1.9055893873338006, 1.8877676312584644, 1.8984298632157404, 1.898282455118664,
                    1.9015390384989175, 1.8457561924105443, 1.8720306738008414, 1.889827521374864, 1.8592533163179974,
                    1.9217260876399633, 1.8616447471021746, 1.8595038181432582, 1.8749651148929043, 1.90121313828603,
                    1.9221248253791654, 1.895145346544522, 1.9043235404475969, 1.9270331671045309, 1.8866377741566254,
                    1.885087883022754, 1.8936368549459268, 1.91040627606003, 1.8872564344227658, 1.8902575478474826,
                    1.9193135547534026, 1.8812012396511462, 1.9198393037284893, 1.9006042115289663, 1.8973634648115318,
                    1.9376446364728739, 1.8985286625482491, 1.859590603877603, 1.8985316037387803, 1.8802489842334809])

    # Confidence interval percentage (95% confidence interval)
    alpha = 0.05

    # Calculate mean and sample standard deviation
    mean_mrt = np.mean(mrt)
    std_mrt = np.std(mrt, ddof=1)  # SEE NOTES AT THE END OF THE FILE

    # %% Calculations

    # Number of tests
    n = len(mrt)

    mf = stats.t.ppf(1 - alpha / 2, n - 1) / np.sqrt(n)

    confidence_interval = mean_mrt + np.array([-1, 1]) * mf * std_mrt

    print('confidence interval: ', confidence_interval)


if __name__ == "__main__":
    # Generate Graph for Internal Arrival Time
    # for i in range(5, 8, 1):
    #     Generate_inter_arrival_time_plot(i)
    #     Generate_subJob_plot(i)
    #     Generate_subJob_Service_time(7)

    generate_Reproducibility_plot()

    # Generate_Job_Response_Time_Plot(100)

    print("yes")
