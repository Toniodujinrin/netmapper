import subprocess
import re

def calculateResponseTime(queue):
    while True:
        if(not queue.empty()):
             
            host = queue.get(block=False, timeout=None)
            if(host):
                try:
                    ip_address = host.get("ip_address",0)
                    if(not ip_address): return 
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
                        queue.task_done()
                        queue.put(host)
                except Exception as e :
                    print(e)
                    return 
        