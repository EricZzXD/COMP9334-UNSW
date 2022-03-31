import sup_Function
from tabulate import tabulate
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
    sub_job_completed = 0

    # 3) Append Value to Table Array
    table_array.append(Trace_Temp_table_array(master_clock, next_event_type, next_arrival_time, server_status_list, [], []))

    ########################################
    #          Simulation Output           #
    ########################################
    temp_output_sub_job_departure = []
    output_cumulative_Response_time = 0

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
                next_arrival_time = inf
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
                    server_status_value = "Busy, " + str(round(master_clock + float(data[2]), 4)) + ", " + data[
                        1] + ", " + data[0]

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

        # Update The Table value
        insert_value = Trace_Temp_table_array(master_clock, next_event_type, next_arrival_time, server_status_list, high_pri_queue, low_pri_queue)
        table_array.append(insert_value)

        # End the Simulation
        if task_arrival_counter == job_NO and server_available_NO == server_NO:
            Simulation_start = False

    print(tabulate(table_array, headers=col_names, tablefmt="fancy_grid"))

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

#############################################################
#       Trace Mode Function
#############################################################


# Find earliest departure
def earliest_departure_Server(Server_Status_List):
    depart_time = inf

    for i in Server_Status_List:
        if i != "Idle, ∞":
            TAB = i.split(", ")[1].strip()
            temp_depart_time = float(TAB)

            if depart_time >= temp_depart_time:
                depart_time = temp_depart_time

    return depart_time


# Every event will create a temporary table array that used to append to Actual Table array
def Trace_Temp_table_array(master_clock, event_type, next_arrival_time, servers_status_array,
                           high_pri_Queue, low_pri_Queue):
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