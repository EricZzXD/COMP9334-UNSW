# This py include all the necessary function for calculation

import math

# Read inter-arrival file According to mode
import numpy as np


# Read para_*.txt
#     data[0]: Number of server
#     data[1]: Threshold
#     data[2]: time_end (only for random mode)
def read_para_file(mode, filePath):
    data = np.loadtxt(filePath)
    if mode == "trace":
        return int(data[0]), int(data[1])
    else:
        return int(data[0]), int(data[1]), data[2]


# Read inter arrival file and output value
def read_inter_arrival_file(mode, filePath):
    if mode == "trace":
        inter_arrival_time_data = np.loadtxt(filePath)

        # Convert inter-arrival time to arrival time
        arrival_time_cumulative = 0
        for i in range(0, len(inter_arrival_time_data)):
            arrival_time_cumulative += inter_arrival_time_data[i]
            inter_arrival_time_data[i] = arrival_time_cumulative

        return inter_arrival_time_data
    else:
        f = open(filePath)
        first_line = f.readline().split()
        second_line = f.readline().split()
        return first_line[0], first_line[1], first_line[2], second_line


# Read service_*.txt and data format
def read_service_file(mode, filepath):
    if mode == "trace":
        data = np.loadtxt(filepath)

        # data.shape[0] ----> Number of jobs
        numbers_jobs = data.shape[0]
        # data.shape[1] ----> Max number of sub-job per job
        max_number_of_sub_job = data.shape[1]

        # convert numpy.array to list
        data = data.tolist()

        # If value is NaN, pop the value from list and return clean list (without NaN)
        for arr in range(0, numbers_jobs):
            for i in range(0, max_number_of_sub_job):
                if np.isnan(data[arr][i]):
                    data[arr].pop(i)

        return numbers_jobs, max_number_of_sub_job, data
    else:
        data = np.loadtxt(filepath)
        return data[0], data[1]  # Mu & alpha


# Every event will create a temporary table array that used to append to Actual Table array
def Trace_Temp_table_array(master_clock, event_type, next_arrival_time, servers_status_array,
                           high_pri_Queue, low_pri_Queue):
    Temp_table_arr = [master_clock, event_type, next_arrival_time]

    # Append value in the order of {Master Clock, Event_type, Next_arrival_time, server1_status, ...serverN_status,
    # High_priority_queue, low_priority_queue}

    for server in servers_status_array:
        Temp_table_arr.append(server)

    if not high_pri_Queue:
        Temp_table_arr.append("-")
    else:
        Temp_table_arr.append(high_pri_Queue)

    if not low_pri_Queue:
        Temp_table_arr.append("-")
    else:
        Temp_table_arr.append(low_pri_Queue)

    return Temp_table_arr


# Define Header Names
def table_header_names(Number_of_servers):
    col_names = ["Master Clock", "Event Type", "Next Arrival Time"]
    for i in range(0, Number_of_servers):
        server_counter = "server " + str(i + 1)
        col_names.append(server_counter)

    col_names.append("High Priority Queue")
    col_names.append("Low Priority Queue")

    return col_names


# Generate k random service times for the k sub-jobs (Project-v1.00 - P15)
def cdf_subJob_service_time(mu, subT, a):
    if mu < 0 or a < 0:
        return EOFError

    return 1 - math.exp(-(mu * subT) ** a)

