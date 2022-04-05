#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This program reads in an input, triples it and then writes the result
to a file.
"""

import sys
import numpy as np
import os
import math
import random
import tabulate


def main(file_number):
    # Read/Output file from Folder (name)
    readFolder = "config"
    outputFolder = "output"
    logMaterialFolder = "support_material"

    # construct Value
    idle_server_Value = "Idle, ∞"

    # Path of necessary filename
    Mode_file = os.path.join(readFolder, 'mode_' + file_number + '.txt')
    Para_file = os.path.join(readFolder, 'para_' + file_number + '.txt')
    inter_arrival_file = os.path.join(readFolder, 'interarrival_' + file_number + '.txt')
    service_file = os.path.join(readFolder, 'service_' + file_number + '.txt')

    # Initial Variable for Read file
    processing_mode = open(Mode_file, "r").read().strip()  # Read mode and clear all newline and space
    server_NO, threshold, end_time = 0, 0, 0
    lamb, a2l, a2u, p_sequence, arrival_time_array = 0, 0, 0, [], []
    job_NO, max_sub_job, sub_job_service_time_list, mu, alpha = 0, 0, [], 0, 0

    ########################################
    #          Pre_define_Valuable         #
    ########################################
    Simulation_start = True
    inter_arrival_value_list_store = []
    sub_job_Service_time_List_Store = []
    sub_job_random_uniform_Store = []
    job_Response_Time_Store = []
    no_job_arrival = 0
    master_clock = 0
    next_departure_time = math.inf
    high_pri_queue = []
    low_pri_queue = []
    arrival_true = True

    ########################################
    #   Read value from the Input file     #
    ########################################
    if processing_mode == "trace":
        server_NO, threshold = read_para_file(processing_mode, Para_file)
        arrival_time_array = read_inter_arrival_file(processing_mode, inter_arrival_file)
        job_NO, max_sub_job, sub_job_service_time_list = read_service_file(processing_mode, service_file)
        server_status_list = [idle_server_Value] * server_NO
        next_arrival_time = arrival_time_array[no_job_arrival]
        server_available_NO = server_NO
    else:  # Random Mode
        server_NO, threshold, end_time = read_para_file(processing_mode, Para_file)
        lamb, a2l, a2u, p_sequence = read_inter_arrival_file(processing_mode, inter_arrival_file)
        mu, alpha = read_service_file(processing_mode, service_file)
        next_arrival_time = generate_inter_arrival_time(a2l, a2u, lamb)
        inter_arrival_value_list_store.append(next_arrival_time)
        server_status_list = [idle_server_Value] * server_NO
        server_available_NO = server_NO

    ########################################
    #          Simulation Output           #
    ########################################
    temp_output_sub_job_departure = []
    output_cumulative_Response_time = 0

    ########################################
    #          Simulation Start            #
    ########################################
    while Simulation_start:
        # End the Simulation
        if no_job_arrival == job_NO and server_available_NO == server_NO and processing_mode == "trace":
            break

        elif master_clock >= end_time and processing_mode == "random":
            break

        # Define the Next Event Type
        if next_arrival_time < next_departure_time:
            next_event_type = "Arrival"
        else:
            next_event_type = "Departure"

        ########################################
        #          Arrival event Type          #
        ########################################
        if next_event_type == "Arrival":
            master_clock = next_arrival_time

            if processing_mode == "trace":
                # Get Sub-job Info
                sj_service_list = sub_job_service_time_list[no_job_arrival]
                sj_number = len(sj_service_list)

                # Server Allocation Complete and Update Task_arrival_counter
                no_job_arrival = no_job_arrival + 1
                # Handle Next Arrival Time Update
                if no_job_arrival >= job_NO:
                    next_arrival_time = math.inf
                else:
                    next_arrival_time = arrival_time_array[no_job_arrival]

            else:  # Random Mode
                interval_arrival_time = generate_inter_arrival_time(a2l, a2u, lamb)
                inter_arrival_value_list_store.append(interval_arrival_time)  # Record - List of inter arrival job
                next_arrival_time = master_clock + interval_arrival_time
                no_job_arrival = no_job_arrival + 1  # Record - Number of income Job

                # Generate k sub-job
                sj_number = generate_NO_sub_job(p_sequence)

                # Generate Service Time
                temp_random_list = []
                sj_service_list = []
                for i in range(0, sj_number):
                    random_value = random.uniform(0, 1)
                    value = round(((-math.log(1 - random_value)) ** (1 / alpha)) / mu, 4)
                    if (master_clock + value) < end_time:
                        sj_service_list.append(value)
                        temp_random_list.append(random_value)
                    else:
                        arrival_true = False

                sub_job_random_uniform_Store.append(temp_random_list)
                sub_job_Service_time_List_Store.append(sj_service_list)  # Record - Store inter-arrival Time

            if arrival_true:
                # Loop According number of Sub-Job
                for sj_index in range(0, sj_number):
                    ########################################
                    #          Queueing Handling           #
                    ########################################
                    if server_available_NO == 0:
                        # Check If its priority List
                        queue_status_value = "(" + str(no_job_arrival) + "," + str(sj_index + 1) + "), " + str(
                            master_clock) + ", " + str(sj_service_list[sj_index])
                        if sj_number <= threshold:
                            high_pri_queue.append(queue_status_value)
                        else:
                            low_pri_queue.append(queue_status_value)

                    ########################################
                    #        Allocate Task to Server       #
                    ########################################
                    else:
                        # Find the first available server from the List (from server 1 to server 4)
                        locate_avail_server = server_status_list.index(idle_server_Value)

                        Temp_Departure_val = round(master_clock + sj_service_list[sj_index], 4)
                        server_status_value = "Busy, " + str(Temp_Departure_val) + ", " + str(
                            master_clock) + ", (" + str(
                            no_job_arrival) + "," + str(sj_index + 1) + ")"

                        server_status_list[locate_avail_server] = server_status_value

                        # Server In-use
                        server_available_NO = server_available_NO - 1

            ########################################
            #     Find Earliest Departure Time     #
            ########################################
            next_departure_time = earliest_departure_Server(server_status_list)

        ########################################
        #        Departure event Type          #
        ########################################
        else:
            master_clock = next_departure_time

            # find the job departure server from the Server list
            for i in range(0, server_NO):
                # Get Departure Info
                sj_departure_info = server_status_list[i].split(", ")

                # Find Departure Server
                if (server_status_list[i] != idle_server_Value) & (sj_departure_info[1] == str(next_departure_time)):
                    # Update from Busy state to Idle
                    server_status_list[i] = idle_server_Value
                    next_event_type = next_event_type + " - Server " + str(i + 1)

                    # Write Output Value ---
                    temp_subjob_value = [sj_departure_info[2], sj_departure_info[1]]
                    temp_output_sub_job_departure.append(temp_subjob_value)
                    # print(temp_output_sub_job_departure)

                    # After Departure, Check if Queue are empty, and process it.
                    if high_pri_queue:
                        # Split value into [Sub Job], [Arrival Time], [Service Time]
                        data = high_pri_queue[0].split(", ")

                        # Convert the Data to Server Status form
                        server_status_value = "Busy, " + str(round(master_clock + float(data[2]), 4)) + ", " + data[
                            1] + ", " + data[0]

                        # Assign Value to Server
                        server_status_list[i] = server_status_value

                        high_pri_queue.pop(0)

                    elif low_pri_queue:
                        # Split value into [Sub Job], [Arrival Time], [Service Time]
                        data = low_pri_queue[0].split(", ")

                        # Convert the Data to Server Status form
                        server_status_value = "Busy, " + str(round(master_clock + float(data[2]), 4)) + ", " + data[
                            1] + ", " + data[0]

                        # look for the fist available Server
                        locate_avail_server = server_status_list.index(idle_server_Value)

                        # Assign Value to Server
                        server_status_list[locate_avail_server] = server_status_value

                        low_pri_queue.pop(0)

                    else:
                        # Job departure, available server + 1
                        server_available_NO = server_available_NO + 1

            next_departure_time = earliest_departure_Server(server_status_list)

    ########################################
    #     Convert Stored Data to Output    #
    ########################################
    temp_counter = 0
    output_sub_job_departure = ""
    # Output Departure String
    for arr in temp_output_sub_job_departure:
        output_sub_job_departure = output_sub_job_departure + str(arr[0]) + " " * 3 + str(arr[1]) + "\n"
        temp_counter = temp_counter + 1

    # Calcualte Response Time
    myDic = {}
    output_response_time = 0

    # Find all the sub-job of a same job but compare the departure value to find the job response time of each job
    for i in temp_output_sub_job_departure:
        if i[0] not in myDic:
            myDic[i[0]] = i
        else:
            if float(myDic[i[0]][1]) < float(i[1]):
                myDic[i[0]] = i

    # loop the Dic and get the total response time
    for i in myDic:
        output_response_time = output_response_time + float(myDic[i][1]) - float(myDic[i][0])
        job_Response_Time_Store.append(float(myDic[i][1]) - float(myDic[i][0]))

    ########################################
    #     Write Output to file             #
    ########################################
    dep_file = os.path.join(outputFolder, 'dep_' + file_number + '.txt')
    mrt_file = os.path.join(outputFolder, 'mrt_' + file_number + '.txt')

    # Write Txt to file
    with open(dep_file, "w") as file:
        file.write(output_sub_job_departure)

    with open(mrt_file, "w") as file:
        file.write(str(round(output_response_time / no_job_arrival, 4)))

    ########################################
    #     Write logs                       #
    ########################################
    # Log file path
    inter_arr_log_file = os.path.join(logMaterialFolder, "inter_arrival_" + file_number + ".txt")
    Sub_job_number_log_file = os.path.join(logMaterialFolder, "sub_job_service_time_" + file_number + ".txt")
    job_Service_time_log_file = os.path.join(logMaterialFolder, "job_Response_time_" + file_number + ".txt")
    if processing_mode == "random":
        # Log inter-arrival Time
        with open(inter_arr_log_file, "w") as file:
            value = str(lamb) + "\n" + str(inter_arrival_value_list_store).replace("[", "").replace("]", "")
            file.write(value)

        # log Number of Sub job
        with open(Sub_job_number_log_file, "w") as file:
            value = str(p_sequence) + "\n" + str(sub_job_Service_time_List_Store) + "\n" + str(
                sub_job_random_uniform_Store)
            file.write(value)

        # log Number of Sub job
        with open(job_Service_time_log_file, "w") as file:
            value = str(job_Response_Time_Store)
            file.write(value)

    print("Simulation ", file_number, " Done")
    return output_sub_job_departure, round(output_response_time / no_job_arrival, 4)


#  Calculate the Inter-arrival Time
def generate_inter_arrival_time(a2l, a2u, lamb):
    a1k = random.expovariate(float(lamb))
    a2k = random.uniform(a2l, a2u)
    return a1k * a2k


# Get Number of Server Base on percentage
def generate_NO_sub_job(prob_array):
    temp_sub_job = []
    temp_P_sequence = []
    for i in range(0, len(prob_array)):
        temp_sub_job.append(int(i + 1))
        temp_P_sequence.append(float(prob_array[i]))

    value = random.choices(temp_sub_job, temp_P_sequence)
    return value[0]


# Find earliest departure
def earliest_departure_Server(Server_Status_List):
    depart_time = math.inf

    for i in Server_Status_List:
        if i != "Idle, ∞":
            TAB = i.split(", ")[1].strip()
            temp_depart_time = float(TAB)

            if depart_time >= temp_depart_time:
                depart_time = temp_depart_time

    return depart_time


# Every event will create a temporary table array that used to append to Actual Table array
def Temp_table_array(master_clock, event_type, next_arrival_time, servers_status_array, high_pri_Queue, low_pri_Queue):
    Temp_table_arr = [master_clock, event_type, next_arrival_time]

    temp_high_pri_array = []
    temp_low_pri_array = []

    for server in servers_status_array:
        Temp_table_arr.append(server)

    if not high_pri_Queue:
        Temp_table_arr.append("-")
    else:
        for value in high_pri_Queue:
            temp_high_pri_array.append(value)
        Temp_table_arr.append(temp_high_pri_array)

    if not low_pri_Queue:
        Temp_table_arr.append("-")
    else:
        for value in low_pri_Queue:
            temp_low_pri_array.append(value)
        Temp_table_arr.append(temp_low_pri_array)

    return Temp_table_arr


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
            inter_arrival_time_data[i] = round(arrival_time_cumulative, 4)

        return inter_arrival_time_data
    else:
        f = open(filePath)
        first_line = f.readline().split()
        second_line = f.readline().split()
        return float(first_line[0]), float(first_line[1]), float(first_line[2]), second_line


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
            for i in range(max_number_of_sub_job - 1, 0, -1):
                if np.isnan(data[arr][i]):
                    data[arr].pop(i)

        return numbers_jobs, max_number_of_sub_job, data
    else:
        data = np.loadtxt(filepath)
        return data[0], data[1]  # Mu & alpha


if __name__ == "__main__":
    main(str(sys.argv[1]))

    # #### Reproducibility Test
    # logMaterialFolder = "support_material"
    # Reproducibility_log_file = os.path.join(logMaterialFolder, "Reproducibility_random_100.txt")
    # mrt_list = []
    # for i in range(0, 50):
    #     print(i+1)
    #     mrt = main("100")
    #
    #     mrt_list.append(mrt)
    #
    # with open(Reproducibility_log_file, "w") as file:
    #     value = mrt_list
    #     file.write(str(value))

