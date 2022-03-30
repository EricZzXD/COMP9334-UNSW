import sup_Function
from tabulate import tabulate


def random_mode_simulation(processing_mode, Para_file, inter_arrival_file, service_file):
    # Read value from the Input file
    server_NO, threshold, end_time = sup_Function.read_para_file(processing_mode, Para_file)
    lamb, a2l, a2u, p_sequence = sup_Function.read_inter_arrival_file(processing_mode, inter_arrival_file)
    mu, alpha = sup_Function.read_service_file(processing_mode, service_file)


    print("random")
