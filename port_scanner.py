import socket 

end_port_range = 1000

def get_open_ports(exception_flag, viewing_array):
    counter = 0 
    while not exception_flag.is_set():
        if(len(viewing_array)> counter):
            host = viewing_array[counter]
            ip = host.get("ip_address",0)
            ports = []
            for i in range(1,end_port_range):  
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    res = sock.connect_ex((ip,i))
                    if (res == 0 or res == 11 ): 
                        ports.append(str(i))
            if(len(ports) > 0 and len(ports)<10):
                host["open_ports"] = ",".join(ports)
            elif(len(ports)>10):
                host["open_ports"] = f"{len(ports)} open ports "
            else: host["open_ports"] = "N/A"
            counter +=1



            

