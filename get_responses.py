import subprocess
import re
import os 
def calculateResponseTime(exception_flag, viewing_array, data_lock):
    counter = 0 
    while not exception_flag.is_set():
        if(len(viewing_array) > counter):
            host = viewing_array[counter]
            try:
               # data_lock.acquire(blocking=False)
                ip_address = host.get("ip_address",0)
                ping_process = None 
                #os specific pings 
                if os.name == "nt":
                    ping_process = subprocess.run(
                        ["ping", "-n","5", ip_address ], text=True, capture_output=True)
                else:
                    ping_process = subprocess.run(
                        ["ping", "-c","5", ip_address ], text=True, capture_output=True)
                    
                if (ping_process.stdout):
                    ttl = []
                    response_times = []
                    #os specific code 
                    if (os.name == "nt"):
                        ttl = re.findall(
                            r"TTL=([\d.]+)", ping_process.stdout
                        )
                        response_times = re.findall(
                            r"time=([\d.]+)", ping_process.stdout)
                    else:
                        ttl = re.findall(
                            r"ttl=([\d.]+)", ping_process.stdout
                        )
                        response_times = re.findall(
                            r"time=([\d.]+) ms", ping_process.stdout)

                    response_times = [float(x) for x in response_times]
                    sum = 0 
                    for i in response_times:
                        sum += i
                    if(sum):
                        sum /= len(response_times)
                    host["average_response_time"]=sum
                    if(len(ttl)):
                        host["ttl"] = ttl[0]
                    else:
                        host["ttl"] = "N/A"
               # data_lock.release()
            except Exception as e :
                print(e)
            counter += 1 
            
    
        
            