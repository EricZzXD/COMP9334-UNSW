import sup_Function
from tabulate import tabulate
import numpy as np
from math import inf


def trace_mode_simulation(processing_mode, Para_file, inter_arrival_file, service_file, idle_server_Value):
    ########################################
    #   Read value from the Input file     #
    ########################################
    server_NO, threshold = sup_Function.read_para_file(processing_mode, Para_file)
    arrival_time_array = sup_Function.read_inter_arrival_file(processing_mode, inter_arrival_file)
    job_NO, max_sub_job, sub_job_service_time_list = sup_Function.read_service_file(processing_mode, service_file)

    ########################################
    #          Pre_define_Valuable         #
    ########################################
    # 1) table Value: Col_name: Table_header_name     Table_array: Table Array Value
    col_names = sup_Function.table_header_names(server_NO)
    table_array = []  # used to Create Table

    # 2) Temp Value for Simulation use
    Simulation_start = True
    task_arrival_counter = 0
    server_status_list = ["Idle, ∞"] * server_NO
    server_available_NO = server_NO
    master_clock = 0
    next_event_type = "-"
    next_arrival_time = arrival_time_array[task_arrival_counter]
    next_departure_time = inf
    high_pri_queue = []
    low_pri_queue = []

    # 3) Append Value to Table Array
    table_array.append(sup_Function.Trace_Temp_table_array(master_clock, next_event_type, next_arrival_time, server_status_list, [], []))

    ########################################
    #          Simulation Output           #
    ########################################
    output_dep = ""

    ########################################
    #          Simulation Start            #
    ########################################
    while Simulation_start:
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
                    queue_status_value = "(" + str(task_arrival_counter + 1) + "," + str(sj_index + 1) + "), " + str(next_arrival_time) + ", " + str(sub_job_service_time_list[task_arrival_counter][sj_index])
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
                    server_status_value = "Busy, " + str(Temp_Departure_val) + ", " + str(master_clock) + ", (" + str(task_arrival_counter + 1) + "," + str(sj_index + 1) + ")"

                    server_status_list[locate_avail_server] = server_status_value

                    # Server In-use
                    server_available_NO = server_available_NO - 1

            # Server Allocation Complete and Update Task_arrival_counter
            task_arrival_counter = task_arrival_counter + 1
            # Handle Next Arrival Time Update
            if task_arrival_counter >= job_NO:
                next_arrival_time = inf
            else:
                next_arrival_time = arrival_time_array[task_arrival_counter]

            ########################################
            #     Find Earliest Departure Time     #
            ########################################
            next_departure_time = sup_Function.earliest_departure_Server(server_status_list)

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

                    output_dep = output_dep + sj_depature_info[2] + " " * 3 + sj_depature_info[1] + "\n"

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
                    server_status_value = "Busy, " + str(round(master_clock + float(data[2]), 4)) + ", " + data[1] + ", " + data[0]

                    # look for the fist available Server
                    locate_avail_server = server_status_list.index(idle_server_Value)

                    # Assign Value to Server
                    server_status_list[locate_avail_server] = server_status_value

                    # Update number of available of server & clear value from the queue
                    server_available_NO = server_available_NO - 1
                    low_pri_queue.pop(0)

            next_departure_time = sup_Function.earliest_departure_Server(server_status_list)

        # Update The Table value
        insert_value = sup_Function.Trace_Temp_table_array(master_clock, next_event_type, next_arrival_time, server_status_list, high_pri_queue, low_pri_queue)
        table_array.append(insert_value)

        # End the Simulation
        if task_arrival_counter == job_NO and server_available_NO == server_NO:
            Simulation_start = False

    print(tabulate(table_array, headers=col_names, tablefmt="fancy_grid"))

    return output_dep