import socket 

end_port_range = 1000

def get_open_ports():
    ip = "140.193.240.24"
    open_ports = []
    for i in range(1,end_port_range):  
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            res = sock.connect_ex((ip,i))
            print(i,res)
            if (res == 0 or res == 11 ): 
               
                open_ports.append(str(i))

get_open_ports()
                
            