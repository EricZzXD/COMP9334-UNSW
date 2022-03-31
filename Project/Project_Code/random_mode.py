import sup_Function
from tabulate import tabulate
from math import inf
import random
import math


def random_mode_simulation(processing_mode, Para_file, inter_arrival_file, service_file, idle_server_Value):
    ########################################
    #   Read value from the Input file     #
    ########################################
    # Read value from the Input file
    server_NO, threshold, end_time = sup_Function.read_para_file(processing_mode, Para_file)
    lamb, a2l, a2u, p_sequence = sup_Function.read_inter_arrival_file(processing_mode, inter_arrival_file)
    mu, alpha = sup_Function.read_service_file(processing_mode, service_file)

    ########################################
    #          Pre_define_Valuable         #
    ########################################
    master_clock = 0
    Number_Job_Served = 0
    next_arrival_time = get_inter_arrival_time(a2l, a2u, lamb)
    next_departure_time = inf
    server_available_no = server_NO
    server_status_list = idle_server_Value * server_available_no
    max_no_subjob = len(p_sequence)

    # for future use
    inter_arrival_value = []

    print(next_arrival_time)
    print(p_sequence)

    print(cdf_subJob_service_time(mu, 3, alpha))

    ########################################
    #          Simulation Start            #
    ########################################
    # while master_clock < end_time:
    #     # Define the Next Event Type
    #     if next_arrival_time < next_departure_time:
    #         next_event_type = "Arrival"
    #     else:
    #         next_event_type = "Departure"
    #
    # print("random")


########################################
#          Necessary Function          #
########################################

#  Calculate the Inter-arrival Time
def get_inter_arrival_time(a2l, a2u, lamb):
    a1k = round(random.uniform(a2l, a2u), 4)
    a2k = round(random.expovariate(float(lamb)), 4)
    return round(a1k + a2k, 4)


# Generate k random service times for the k sub-jobs (Project-v1.00 - P15)
def cdf_subJob_service_time(mu, subT, a):
    if mu < 0 or a < 0:
        return EOFError
    return 1 - math.exp(-(mu * subT) ** a)


# Get Number of Server Base on percentage
def get_Server_size(arr):
    value = random.randint(0, 100) / 100
    cumulate = arr[0]
    server_counter = 1

    for i in range(0, len(arr)):
        if value <= cumulate:
            return server_counter
        else:
            cumulate = round(cumulate + arr[i + 1], 4)
            server_counter = server_counter + 1


