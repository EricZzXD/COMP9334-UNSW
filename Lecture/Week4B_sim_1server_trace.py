#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMP9334 Capacity Planning

This Python file demonstrates trace driven simulation

It computes the mean response time

"""

# Import
from math import inf

############################
# List for arrival times and service times
############################
# Arrival time and service time
arrival_time = [3, 8, 9, 17, 18, 19, 20, 25, 27]
service_time = [4, 3, 4, 6, 3, 2, 2, 3, 2]

###########################
# Accounting parameters
###########################
#  The cumulative response time
response_time_cumulative = 0
# Number of customers served at the end of the simulation
num_customers_served = 0
#
# The mean response time will be given by
# response_time_cumulative/num_customers_served
#

###########################
# Events
###########################
#
# There are two events: An arrival event and a departure event
#
# An arrival event is specified by
#   next_arrival_time = the time at which the next customer arrives
#   service_time_next_arrival = the service time of the next arrival
#
# A departure event is specified by
#   next_departure_time = the time at which the next departure occurs
#   arrival_time_next_departure = the time at which the next departing
#               customer arrives at the system
#

############################
# Initialising the events
############################
#
# Initialising the arrival event
#
next_arrival_time = arrival_time[0]
service_time_next_arrival = service_time[0]
# Initialise a two counters
job_counter = 1  # Points to the next job in the job list
# Variable to store the number of jobs
number_of_jobs = len(arrival_time)
# To store information on departure
departure_info = []

#
# Initialise the departure event to empty
# Note: We use inf (= infinity) to denote an empty departure event
#
next_departure_time = inf

#############################
# Initialising the Master clock, server status, queue_length,
# buffer_content
#
# server_status = 1 if busy, 0 if idle
#
# queue_length is the number of customers in the buffer
#
# buffer_content is a list-of-lists
#
# The inner lists are lists with 2 elements.
# The elements contain the arrival time and service time of a customer.
#
# E.g. If buffer_contents = [[5,7],[8,4]] means there are 2 customers
# in the server.
# For the 1st customer, its arrival and service times are respectively 5 and 7.
# For the 2nd customer, its arrival and service times are respectively 8 and 4.
#
# To add a job to the end of the buffer, use buffer_contents.append()
# To take a job off the front of the buffer, use buffer_contents.pop(0)
#
#############################
#
# Intialise the master clock
master_clock = 0
#
# Intialise server status
server_busy = 0
#
# Initialise buffer
buffer_content = []
queue_length = 0

# Start iteration until the end of simulation time
while True:

    # Find out whether the next event is an arrival or depature
    #
    if next_arrival_time < next_departure_time:
        next_event_time = next_arrival_time
        next_event_type = 'arrival'
    else:
        next_event_time = next_departure_time
        next_event_type = 'departure'

        #
    # update master clock
    #
    master_clock = next_event_time

    #
    # take actions depending on the event type
    #
    if next_event_type == 'arrival':  # an arrival
        if server_busy:
            #
            # add customer to buffer_content and
            # increment queue length
            #
            buffer_content.append([next_arrival_time, service_time_next_arrival])
            queue_length += 1
        else:  # server not busy
            #
            # Schedule departure event where
            # the departure time is arrival time + service time
            # Also, set server_busy to 1
            #
            next_departure_time = next_arrival_time + service_time_next_arrival
            arrival_time_next_departure = next_arrival_time
            server_busy = 1

        # Fetch the next job and schedule its arrival
        if job_counter < number_of_jobs:
            # Get next job
            next_arrival_time = arrival_time[job_counter]
            service_time_next_arrival = service_time[job_counter]
            job_counter += 1
        else:  # If there are no more jobs
            next_arrival_time = inf


    else:  # a departure
        #
        # Update the variables:
        # 1) response_time_cumulative T
        # 2) num_customers_served N
        #
        response_time_cumulative += master_clock - arrival_time_next_departure
        num_customers_served += 1
        departure_info.append([arrival_time_next_departure, master_clock])
        #
        if queue_length:  # buffer not empty
            #
            # Take the first customer in the buffer into the server
            # Schedule the next departure event
            #

            first_job_in_the_buffer = buffer_content.pop(0)
            queue_length -= 1

            next_departure_time = master_clock + first_job_in_the_buffer[1]
            arrival_time_next_departure = first_job_in_the_buffer[0]
            #
            # remove customer from buffer and decrement queue length
            #

        else:  # buffer empty
            next_departure_time = inf
            server_busy = 0

    # Break the while loop if all jobs have departed
    if num_customers_served == number_of_jobs:
        break

# The estimated mean response time
mean_response_time = response_time_cumulative / num_customers_served
print('The estimated mean response time is ', mean_response_time)

