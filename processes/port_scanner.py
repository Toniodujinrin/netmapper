import socket
import threading  

end_port_range = 10000

def connect(ip:str,port:int,ports:list):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        res = sock.connect_ex((ip,port))
        if (res == 0): 
            ports.append(str(port))



def get_open_ports(exception_flag, viewing_array:list, discovery_finished):
    counter = 0 
    while not exception_flag.is_set() and not (discovery_finished.is_set() and counter == len(viewing_array)):
        if(len(viewing_array)> counter):
            host = viewing_array[counter]
            ip = host.get("ip_address",0)
            ports = []
            for i in range(1,end_port_range):  
                threading.Thread(target=connect,kwargs={"ip":ip,"ports":ports,"port":i}).start() 
            if(len(ports) > 0 and len(ports)<30):
                host["open_ports"] = ",".join(ports)
            else:
                host["open_ports"] = f"{len(ports)} open ports "
           
            counter +=1
            



            

