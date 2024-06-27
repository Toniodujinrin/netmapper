from tabulate import tabulate
from os import system
from copy import deepcopy

def logger(viewing_array,log_exception_flag, exception_flag,options,discovery_finished):
    old_viewing_arr = []
    
    while not (exception_flag.is_set() or log_exception_flag.is_set()):
        if(str(old_viewing_arr) != str(viewing_array)):
            system("clear")
            header = options["header"]
            rows = []
            for viewing_output in viewing_array:
                #sort output to conform to logging order 
                sorted_output = [""]*len(header)
                for title,value in viewing_output.items(): 
                    for i in range(0,len(header)):
                        if(header[i]==title):
                            sorted_output[i] = value
                rows.append(sorted_output)
            rows.insert(0,header)
            print(tabulate(rows))
            old_viewing_arr = deepcopy(viewing_array)
        
        
