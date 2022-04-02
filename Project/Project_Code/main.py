#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This program reads in an input, triples it and then writes the result
to a file.
"""

import sys
import numpy as np
import os

import sup_Function
import trace_mode
import random_mode
from decimal import *


def main(file_number):
    # Read/Output file from Folder (name)
    readFolder = "config"
    outputFolder = "output"

    # construct Value
    idle_server_Value = "Idle, ∞"

    # Path of necessary filename
    Mode_file = os.path.join(readFolder, 'mode_' + file_number + '.txt')
    Para_file = os.path.join(readFolder, 'Para_' + file_number + '.txt')
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
        output_SJ_departure, mrt_SJ = trace_mode.trace_mode_simulation(processing_mode, Para_file, inter_arrival_file,
                                                                       service_file, idle_server_Value)


    ########################################
    #         Random Mode                  #
    ########################################
    elif processing_mode == "random":
        output_SJ_departure, mrt_SJ = random_mode.random_mode_simulation(processing_mode, Para_file,
                                                                                       inter_arrival_file, service_file,
                                                                                       idle_server_Value)
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


if __name__ == "__main__":
    main("7")