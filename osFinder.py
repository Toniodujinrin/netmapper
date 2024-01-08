import subprocess
import re

def calculateResponseTime(exception_flag, viewing_array, data_lock):
    counter = 0 
    while not exception_flag.is_set():
        if(len(viewing_array) > counter):
            host = viewing_array[counter]
            try:
               # data_lock.acquire(blocking=False)
                ip_address = host.get("ip_address",0)
                ping_process = subprocess.run(
                    ["ping", "-c","5", ip_address ], text=True, capture_output=True)
                if (ping_process.stdout):
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
                return 
            counter += 1 
            
    
        
            