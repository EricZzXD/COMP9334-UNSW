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


def main(file_number):
    # Read/Output file from Folder (name)
    readFolder = "config"
    outputFolder = "output"

    # construct Value
    idle_server_Value = "Idle, ∞"

    # Path of necessary filename
    Mode_file = os.path.join(readFolder, 'mode_' + file_number + '.txt')
    Para_file = os.path.join(readFolder, 'para_' + file_number + '.txt')
    inter_arrival_file = os.path.join(readFolder, 'interarrival_' + file_number + '.txt')
    service_file = os.path.join(readFolder, 'service_' + file_number + '.txt')

    # Read Processing Mode from File
    processing_mode = open(Mode_file, "r").read().strip()  # Read mode and clear all newline and space

    output_SJ_departure = ""
    mrt_SJ = ""

    ########################################
    #         Trace Mode                   #
    ########################################
    if processing_mode == "trace":
        output_SJ_departure, mrt_SJ = trace_mode_simulation(processing_mode, Para_file, inter_arrival_file, service_file, idle_server_Value)

    ########################################
    #         Random Mode                  #
    ########################################
    elif processing_mode == "random":
        output_SJ_departure, mrt_SJ = random_mode_simulation(processing_mode, Para_file, inter_arrival_file, service_file, idle_server_Value)
    else:
        print("Error")

    # Output file path
    dep_file = os.path.join(outputFolder, 'dep_' + file_number + '.txt')
    mrt_file = os.path.join(outputFolder, 'mrt_' + file_number + '.txt')

    # Write Txt to file
    with open(dep_file, "w") as file:
        file.write(output_SJ_departure)

    with open(mrt_file, "w") as file:
        file.write(str(mrt_SJ))

    print("Simulation ", file_number, " Done")


# Trace Mode Simulation
def trace_mode_simulation(processing_mode, Para_file, inter_arrival_file, service_file, idle_server_Value):
    ########################################
    #   Read value from the Input file     #
    ########################################
    server_NO, threshold = read_para_file(processing_mode, Para_file)
    arrival_time_array = read_inter_arrival_file(processing_mode, inter_arrival_file)
    job_NO, max_sub_job, sub_job_service_time_list = read_service_file(processing_mode, service_file)

    ########################################
    #          Pre_define_Valuable         #
    ########################################
    # 1) Temp Value for Simulation use
    Simulation_start = True
    task_arrival_counter = 0
    server_status_list = [idle_server_Value] * server_NO
    server_available_NO = server_NO
    master_clock = 0
    next_event_type = "-"
    next_arrival_time = arrival_time_array[task_arrival_counter]
    next_departure_time = math.inf
    high_pri_queue = []
    low_pri_queue = []
    sub_job_completed = 0

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
        if task_arrival_counter == job_NO and server_available_NO == server_NO:
            Simulation_start = False
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

            # Get Sub-job Info
            sj_service_list = sub_job_service_time_list[task_arrival_counter]
            sj_number = len(sj_service_list)

            # Loop According number of Sub-Job
            for sj_index in range(0, sj_number):

                ########################################
                #          Queueing Handling           #
                ########################################
                if server_available_NO == 0:
                    # Check If its priority List
                    queue_status_value = "(" + str(task_arrival_counter + 1) + "," + str(sj_index + 1) + "), " + str(
                        next_arrival_time) + ", " + str(sub_job_service_time_list[task_arrival_counter][sj_index])
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

                    Temp_Departure_val = round(next_arrival_time + sj_service_list[sj_index], 4)
                    server_status_value = "Busy, " + str(Temp_Departure_val) + ", " + str(master_clock) + ", (" + str(
                        task_arrival_counter + 1) + "," + str(sj_index + 1) + ")"

                    server_status_list[locate_avail_server] = server_status_value

                    # Server In-use
                    server_available_NO = server_available_NO - 1

            # Server Allocation Complete and Update Task_arrival_counter
            task_arrival_counter = task_arrival_counter + 1
            # Handle Next Arrival Time Update
            if task_arrival_counter >= job_NO:
                next_arrival_time = math.inf
            else:
                next_arrival_time = arrival_time_array[task_arrival_counter]

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
                sj_depature_info = server_status_list[i].split(", ")

                # Find Departure Server
                if (server_status_list[i] != idle_server_Value) & (sj_depature_info[1] == str(next_departure_time)):
                    # Update from Busy state to Idle
                    server_status_list[i] = idle_server_Value
                    # Job departure, available server + 1
                    server_available_NO = server_available_NO + 1
                    next_event_type = next_event_type + " - Server " + str(i + 1)

                    # Write Output Value
                    sub_job_completed = sub_job_completed + 1
                    temp_subjob_value = [sj_depature_info[2], sj_depature_info[1]]
                    temp_output_sub_job_departure.append(temp_subjob_value)

                # After Departure, Check if Queue are empty, and process it.
                if high_pri_queue and server_available_NO != 0:
                    # Split value into [Sub Job], [Arrival Time], [Service Time]
                    data = high_pri_queue[0].split(", ")

                    # Convert the Data to Server Status form
                    server_status_value = "Busy, " + str(round(master_clock + float(data[2]), 4)) + ", " + data[1] + ", " + data[0]

                    # look for the fist available Server
                    locate_avail_server = server_status_list.index(idle_server_Value)

                    # Assign Value to Server
                    server_status_list[locate_avail_server] = server_status_value

                    # Update number of available of server & clear value from the queue
                    server_available_NO = server_available_NO - 1
                    high_pri_queue.pop(0)

                elif low_pri_queue and server_available_NO != 0:
                    # Split value into [Sub Job], [Arrival Time], [Service Time]
                    data = low_pri_queue[0].split(", ")

                    # Convert the Data to Server Status form
                    server_status_value = "Busy, " + str(round(master_clock + float(data[2]), 4)) + ", " + data[
                        1] + ", " + data[0]

                    # look for the fist available Server
                    locate_avail_server = server_status_list.index(idle_server_Value)

                    # Assign Value to Server
                    server_status_list[locate_avail_server] = server_status_value

                    # Update number of available of server & clear value from the queue
                    server_available_NO = server_available_NO - 1
                    low_pri_queue.pop(0)

            next_departure_time = earliest_departure_Server(server_status_list)

    ########################################
    #     Convert Stored Data to Output    #
    ########################################
    temp_output_resp = 0
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
        output_response_time = round(output_response_time + round(float(myDic[i][1]) - float(myDic[i][0]), 4), 4)

    return output_sub_job_departure, round(output_response_time / job_NO, 4)


# Random Mode Simulation
def random_mode_simulation(processing_mode, Para_file, inter_arrival_file, service_file, idle_server_Value):
    ########################################
    #   Read value from the Input file     #
    ########################################
    # Read value from the Input file
    server_NO, threshold, end_time = read_para_file(processing_mode, Para_file)
    lamb, a2l, a2u, p_sequence = read_inter_arrival_file(processing_mode, inter_arrival_file)
    mu, alpha = read_service_file(processing_mode, service_file)

    ########################################
    #          Pre_define_Valuable         #
    ########################################
    # Define Future Use variable
    inter_arrival_value_list_store = []
    sub_job_Service_time_List_Store = []
    temp_output_sub_job_departure = []

    # Define variable
    master_clock = 0
    next_event_type = "-"
    next_arrival_time = generate_inter_arrival_time(a2l, a2u, lamb)
    inter_arrival_value_list_store.append(next_arrival_time)
    next_departure_time = math.inf
    server_available_NO = server_NO
    server_status_list = [idle_server_Value] * server_available_NO
    task_arrival_counter = 0
    high_pri_queue = []
    low_pri_queue = []
    no_job_arrival = 0
    sub_job_completed = 0
    arrival_true = True

    ########################################
    #          Simulation Start            #
    ########################################

    while master_clock < end_time:
        # Define the Next Event Type
        if next_arrival_time < next_departure_time:
            next_event_type = "Arrival"
        else:
            next_event_type = "Departure"

        ########################################
        #          Arrival event Type          #
        ########################################
        if next_event_type == "Arrival":
            # update Master clock value and other info
            master_clock = next_arrival_time
            next_arrival_time = round(master_clock + generate_inter_arrival_time(a2l, a2u, lamb), 4)
            inter_arrival_value_list_store.append(next_arrival_time)  # Record - List of inter arrival job
            no_job_arrival = no_job_arrival + 1  # Record - Number of income Job

            # Generate k sub-job
            sj_number = generate_NO_sub_job(p_sequence)

            # Generate Service Time
            temp_subjob_service_list = []
            for i in range(0, sj_number):
                value = round(((-math.log(1 - random.uniform(0, 1))) ** (1 / alpha)) / mu, 4)
                if (master_clock + value) < end_time:
                    temp_subjob_service_list.append(value)
                else:
                    arrival_true = False

            sj_service_list = temp_subjob_service_list
            sub_job_Service_time_List_Store.append(sj_service_list)  # Record - Store inter-arrival Time

            if arrival_true:
                # Loop According number of Sub-Job
                for sj_index in range(0, sj_number):
                    ########################################
                    #          Queueing Handling           #
                    ########################################
                    if server_available_NO == 0:
                        # Check If its priority List
                        queue_status_value = "(" + str(task_arrival_counter) + "," + str(sj_index + 1) + "), " + str(
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
                            master_clock) + ", (" + str(task_arrival_counter) + "," + str(sj_index + 1) + ")"

                        server_status_list[locate_avail_server] = server_status_value

                        # Server In-use
                        server_available_NO = server_available_NO - 1

                # Server Allocation Complete and Update Task_arrival_counter
                task_arrival_counter = task_arrival_counter + 1

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

                    # After Departure, Check if Queue are empty, and process it.
                    if high_pri_queue:
                        # Split value into [Sub Job], [Arrival Time], [Service Time]
                        data = high_pri_queue[0].split(", ")

                        # Convert the Data to Server Status form
                        server_status_value = "Busy, " + str(master_clock + float(data[2])) + ", " + data[
                            1] + ", " + data[0]

                        # Assign Value to Server
                        server_status_list[i] = server_status_value

                        high_pri_queue.pop(0)

                    elif low_pri_queue:
                        # Split value into [Sub Job], [Arrival Time], [Service Time]
                        data = low_pri_queue[0].split(", ")

                        # Convert the Data to Server Status form
                        server_status_value = "Busy, " + str(master_clock + float(data[2])) + ", " + data[
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

    # print(tabulate(table_array, headers=col_names, tablefmt="fancy_grid"))

    return output_sub_job_departure, round(output_response_time / no_job_arrival, 4)


#  Calculate the Inter-arrival Time
def generate_inter_arrival_time(a2l, a2u, lamb):
    a1k = random.uniform(a2l, a2u)
    a2k = random.expovariate(float(lamb))
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
            for i in range(max_number_of_sub_job-1, 0, -1):
                if np.isnan(data[arr][i]):
                    data[arr].pop(i)

        return numbers_jobs, max_number_of_sub_job, data
    else:
        data = np.loadtxt(filepath)
        return data[0], data[1]  # Mu & alpha


# Define Header Names
def table_header_names(Number_of_servers):
    col_names = ["Master Clock", "Event Type", "Next Arrival Time"]
    for i in range(0, Number_of_servers):
        server_counter = "server " + str(i + 1)
        col_names.append(server_counter)

    col_names.append("High Priority Queue")
    col_names.append("Low Priority Queue")

    return col_names


if __name__ == "__main__":
    # main("1")
    main(str(sys.argv[1]))