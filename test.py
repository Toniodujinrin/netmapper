import socket 

end_port_range = 700

def get_open_ports():
    ip = "10.0.0.205"
    open_ports = []
    for i in range(1,end_port_range):  
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            res = sock.connect_ex((ip,i))
            if (res == 0): 
                print(i)
                open_ports.append(str(i))
    print(open_ports)

get_open_ports()
                
            