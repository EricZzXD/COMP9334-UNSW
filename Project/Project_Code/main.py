#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This program reads in an input, triples it and then writes the result
to a file.
"""

import sys
import os
import numpy as np
from math import inf
import sup_Function
from tabulate import tabulate


def main(file_number):
    # Read file from Folder (name)
    readFolder = "config"

    # construct Value
    idle_server_Value = "Idle, ∞"

    # Path of necessary filename
    Mode_file = os.path.join(readFolder, 'mode_' + file_number + '.txt')
    Para_file = os.path.join(readFolder, 'Para_' + file_number + '.txt')
    inter_arrival_file = os.path.join(readFolder, 'interarrival_' + file_number + '.txt')
    service_file = os.path.join(readFolder, 'service_' + file_number + '.txt')

    # Read Processing Mode from File
    processing_mode = open(Mode_file, "r").read().strip()  # Read mode and clear all newline and space

    # Trace Mode & Random mode Common Pre-define variable
    master_clock = 0
    next_event_type = "-"
    next_departure_time = inf  # departure time is unknown that mark as Inf
    high_pri_queue = []
    low_pri_queue = []
    table_array = []
    arrival_service_counter = 0

    if processing_mode == "trace":
        # Read value from the Input file
        server_NO, threshold = sup_Function.read_para_file(processing_mode, Para_file)
        arrival_time_array = sup_Function.read_inter_arrival_file(processing_mode, inter_arrival_file)
        job_NO, max_sub_job, sub_job_service_time_list = sup_Function.read_service_file(processing_mode, service_file)

        # Pre-define Variable
        col_names = sup_Function.table_header_names(server_NO)
        next_arrival_time = arrival_time_array[arrival_service_counter]
        server_status_list = ["Idle, ∞"] * server_NO
        number_server_available = server_NO

        # Print all Necessary Variable
        print(arrival_time_array)
        print("Service Time: ", sub_job_service_time_list)

        table_array.append(
            sup_Function.Trace_Temp_table_array(master_clock, next_event_type, next_arrival_time,
                                                server_status_list, high_pri_queue, low_pri_queue))

        TestCounter = 0

        print(arrival_time_array)

        # Start the Logic
        while TestCounter < 8:
            if next_arrival_time < next_departure_time:
                next_event_type = "Arrival"
            else:
                next_event_type = "Departure"

            if next_event_type == "Arrival":
                master_clock = next_arrival_time

                # Check Server busy and assign Job
                sub_job_service_time = sub_job_service_time_list[arrival_service_counter]
                sub_job_Servers_require = len(sub_job_service_time)

                for sub_job in range(0, sub_job_Servers_require):
                    if number_server_available == 0:
                        queue_status_value = "(" + str(arrival_service_counter+1) + "," + str(sub_job+1) + "), " + str(next_arrival_time) + ", " + str(sub_job_service_time[sub_job])
                        # Detect whether the Job will go to High_pri or Low_Pri
                        if sub_job_Servers_require <= threshold:
                            high_pri_queue.append(queue_status_value)
                        else:
                            low_pri_queue.append(queue_status_value)
                    else:
                        # Find the first available server from the List (from server 1 to server 4)
                        locate_avail_server = server_status_list.index(idle_server_Value)
                        # Update number of available of server
                        number_server_available = number_server_available - 1

                        # Find Departure_time
                        next_departure_time = next_arrival_time + sub_job_service_time[sub_job]
                        server_status_value = "Busy, " + str(next_departure_time) + ", " + str(next_arrival_time) + \
                                              ", (" + str(arrival_service_counter + 1) + "," + str(sub_job + 1) + ")"

                        server_status_list[locate_avail_server] = server_status_value

                # Update Next Arrival Time
                arrival_service_counter = arrival_service_counter + 1
                next_arrival_time = arrival_time_array[arrival_service_counter]

            else:  # Departure Event
                master_clock = next_departure_time

                # find the job departure server from the Server list
                for i in range(0, server_NO):
                    if (server_status_list[i] != idle_server_Value) & (server_status_list[i].split(", ")[1] == str(next_departure_time)):
                        # Update from Busy state to Idle
                        server_status_list[i] = idle_server_Value
                        # Job departure, available server + 1
                        number_server_available = number_server_available + 1
                        next_event_type = next_event_type + " - Server " + str(i+1)

                    # After Departure, Check if Queue are empty, and process it.
                    if high_pri_queue and number_server_available != 0:
                        # Split value into [Sub Job], [Arrival Time], [Service Time]
                        data = high_pri_queue[0].split(", ")

                        # Convert the Data to Server Status form
                        server_status_value = "Busy, " + str(master_clock + float(data[2])) + ", " + data[1] + ", " + data[0]

                        # look for the fist available Server
                        locate_avail_server = server_status_list.index(idle_server_Value)

                        # Assign Value to Server
                        server_status_list[locate_avail_server] = server_status_value

                        # Update number of available of server & clear value from the queue
                        number_server_available = number_server_available - 1
                        high_pri_queue.pop(0)


                # Update Value
                next_departure_time = inf

            insert_value = sup_Function.Trace_Temp_table_array(master_clock, next_event_type, next_arrival_time, server_status_list, high_pri_queue, low_pri_queue)
            table_array.append(insert_value)

            TestCounter = TestCounter + 1

        # display table
        print(tabulate(table_array, headers=col_names, tablefmt="fancy_grid"))

    elif processing_mode == "random":
        # Read value from the Input file
        server_NO, threshold, end_time = sup_Function.read_para_file(processing_mode, Para_file)
        lamb, a2l, a2u, p_sequence = sup_Function.read_inter_arrival_file(processing_mode, inter_arrival_file)
        mu, alpha = sup_Function.read_service_file(processing_mode, service_file)

    else:
        print("Error")


if __name__ == "__main__":
    main("1")
