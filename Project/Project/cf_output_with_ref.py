#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMP9334 Project sample file 

This file compares the output files against their reference.

For trace mode, it checks mrt_*.txt and dep_*.txt

For random mode, it checks mrt_*.txt only 

Assumptions on file location: This file assumes that the output/ and ref/
sub-directories are below the directory that this file is located.
    
    Directory containing cf_output_with_ref.py
    |
    |
    |---- Sub-directory: config
    |---- Sub-directory: output
    |---- Sub-directory: ref
    

This version: 14 March 2022

@author: ctchou
"""

# import sys for input argument 
import sys
import os 

# import numpy for easy comparison 
import numpy as np

def main():
    
    # Check whether there is an input argument 
    if len(sys.argv) == 2:
        # t = int(sys.argv[1])
        t = 1
    else:
        print('Error: Expect the test number as the input argument')
        print('Example usage: python3 cf_output_with_ref.py 1')   
        return
    
    # Location of the folders
    out_folder = 'output'
    ref_folder = 'ref'
        
    # Definitions
    file_ext = '.txt' # File extension
    
    # For trace mode, an absolute tolerance is used
    ABS_TOL = 1e-3  # Absolute tolerance 
    
    # For tests 5, 6 and 7 (which are in radnom mode), the mean response time is expected
    # to be within the range 
    MRT_TOL = [[1.3908, 1.7239],[1.3656, 1.6749],[2.2102, 2.7143]]
    
    # Read test number from the input argument 
       
    # t is the test number
    # Tests 1, 2 and 3 are trace mode
    # Test 4 is radnom mode
    if t in {1,2,3,4}: 
    
        # Compare mrt against the reference
        out_file = os.path.join(out_folder,'mrt_'+str(t)+file_ext)
        ref_file = os.path.join(ref_folder,'mrt_'+str(t)+'_ref'+file_ext)
        
        if os.path.isfile(out_file):
            mrt_stu = np.loadtxt(out_file)
        else:
            print('Error: File ',out_file,'does NOT exist')    
            return
        
        if os.path.isfile(ref_file): 
            mrt_ref = np.loadtxt(ref_file)
        else:
            print('Error: File ',ref_file,'does NOT exist')    
            return           
        
        if np.isclose(mrt_stu,mrt_ref,atol=ABS_TOL):
            print('Test '+str(t)+': Mean response time matches the reference')
        else: 
            print('Test '+str(t)+': Mean response time does NOT match the reference')
    
        # Compare dep against the reference  
        out_file = os.path.join(out_folder,'dep_'+str(t)+file_ext)
        ref_file = os.path.join(ref_folder,'dep_'+str(t)+'_ref'+file_ext)
        
        if os.path.isfile(out_file):
            dep_stu = np.loadtxt(out_file)
        else:
            print('Error: File ',out_file,'does NOT exist')    
            return            
        
        if os.path.isfile(ref_file):
            dep_ref = np.loadtxt(ref_file)
        else:
            print('Error: File ',ref_file,'does NOT exist')    
            return                      
        
        if np.all(np.isclose(dep_stu,dep_ref,atol=ABS_TOL)):
            print('Test '+str(t)+': Departure times match the reference')
        else: 
            print('Test '+str(t)+': Departure times do NOT match the reference')
    
  
    
    elif t in {5,6,7}: 
        out_file = os.path.join(out_folder,'mrt_'+str(t)+file_ext)
       
        if os.path.isfile(out_file):
            mrt_stu = np.loadtxt(out_file)
        else:
            print('Error: File ',out_file,'does NOT exist')    
            return        
    
        
        if MRT_TOL[t-5][0] <= mrt_stu <= MRT_TOL[t-5][1]:
            print('Test '+str(t)+': Mean response time is within tolerance')
        else: 
            print('Test '+str(t)+': Mean response time is NOT within tolerance')
            print('You should try to run a new simulation round with new random numbers.')
            print('Your output need to be within the tolerance for most of the rounds.')
        
        
if __name__ == '__main__':
    dep_error = main()            