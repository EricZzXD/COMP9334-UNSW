# Search departure Sub_job from server
for i in range(0, server_NO):
    sj_departure_info = server_status_list[i].split(", ")

    # Find match Departure Job
    if sj_departure_info[1] == str(next_departure_time):
        server_status_list[i] = idle_server_Value
        next_event_type = next_event_type + " - Server " + str(i + 1)

        # Write Output Value
        temp_subjob_value = [sj_departure_info[2], sj_departure_info[1]]
        temp_output_sub_job_departure.append(temp_subjob_value)

        if high_pri_queue:
            # Split value into [Sub Job], [Arrival Time], [Service Time]
            data = high_pri_queue[0].split(", ")

            # Convert the Data to Server Status form
            server_status_value = "Busy, " + str(round(master_clock + float(data[2]), 4)) + ", " + data[1] + ", " + \
                                  data[0]
            # Assign Value to Server
            server_status_list[i] = server_status_value
            high_pri_queue.pop(0)

        elif low_pri_queue:
            # Split value into [Sub Job], [Arrival Time], [Service Time]
            data = low_pri_queue[0].split(", ")
            # Convert the Data to Server Status form
            server_status_value = "Busy, " + str(round(master_clock + float(data[2]), 4)) + ", " + data[1] + ", " + \
                                  data[0]
            # Assign Value to Server
            server_status_list[i] = server_status_value
            low_pri_queue.pop(0)

        else:
            server_available_NO = server_available_NO + 1