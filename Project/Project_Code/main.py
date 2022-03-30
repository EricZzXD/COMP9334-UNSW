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
import trace_mode
import random_mode
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

    if processing_mode == "trace":
        trace_mode.trace_mode_simulation(processing_mode, Para_file, inter_arrival_file, service_file, idle_server_Value)

    elif processing_mode == "random":
        random_mode.random_mode_simulation(processing_mode, Para_file, inter_arrival_file, service_file)

    else:
        print("Error")


if __name__ == "__main__":
    main("1")
