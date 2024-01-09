import threading
import socket 
import struct
import fcntl
from discover import discover
from concurrent.futures import ThreadPoolExecutor
import ipaddress
from colorama import Fore
from get_responses import calculateResponseTime
import sys
from time import sleep
from get_mac_details import get_mac_details
from port_scanner import get_open_ports
from tabulate import tabulate


options = {}
exception_flag = threading.Event()
data_lock = threading.Lock()
viewing_array = []



def get_host_ip_subnetmask ():
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sock:
        sock.connect(("8.8.8.8",80))
        ip,port = sock.getsockname()
        subnet_mask = fcntl.ioctl(sock.fileno(), 0x891b, struct.pack(
        '256s', "wlan0".encode()))[20:24]
        subnet_mask = socket.inet_ntoa(subnet_mask)
        sock.close()
        return (ip,subnet_mask)

def binaryAnd(ip_address, subnet_mask):
    subnet_mask_array = subnet_mask.split(".")
    ip_address_array = ip_address.split(".")
    result_binary = []
    #convert to binary 
    index = 0 
    while index < 4:
        ip_address_binary = str(bin(int(ip_address_array[index]))).replace("0b","")
        subnet_mask_binary = str(bin(int(subnet_mask_array[index]))).replace("0b","")
        def fill(binary):
            if(len(binary)<8):
                remainder = 8- len(binary)
                fill = "0"*remainder
                return fill+binary
            else: 
                return binary
        ip_address_array[index] = fill(ip_address_binary)
        subnet_mask_array[index] = fill(subnet_mask_binary)
        index += 1
    k = 0 

    #binary and
    while k < 4:
        ip_address_binary = ip_address_array[k]
        subnet_mask_binary = subnet_mask_array[k]
        l = 0
        anded_string = ""
        while l < 8:
            single_ip_binary_digit = ip_address_binary[l]
            single_subnet_binary_digit  = subnet_mask_binary[l]
            if(int(single_subnet_binary_digit) and int(single_ip_binary_digit)):
                anded_string += "1"
            else:
                anded_string += "0"
            l+=1 
        result_binary.append(anded_string)
        k+=1 
    
    #convert network address to decimal
    for index,i in enumerate(result_binary):
        result_binary[index] = int(i,2)
    return (result_binary)

def logger():
    while True:
        sys.stdout.write("\033[H\033[J")
        header = options["header"]
        res = []
        for viewing_output in viewing_array:
            #sort output to conform to logging order 
            sorted_output = [""]*len(header)
            output  = viewing_output.items()
            for title,value in output: 
                for i in range(0,len(header)):
                    if(header[i]==title):
                        sorted_output[i] = value
            res.append(sorted_output)
        res.insert(0,header)
        print(tabulate(res))
        sleep(1)
        




       
     

            

def mainLoop(network_address,subnet_mask):
    network_address_string = [str(i) for i in network_address]
    network_address_string =  ".".join(network_address_string)
    network = ipaddress.IPv4Network(f"{network_address_string}/{subnet_mask}", strict=False)
    if(options["response"]):
        threading.Thread(target=calculateResponseTime,kwargs={"data_lock":data_lock ,"exception_flag":exception_flag, "viewing_array":viewing_array}, daemon=True).start()
    if(options["hardware"]):
        threading.Thread(target=get_mac_details,kwargs={"data_lock":data_lock ,"exception_flag":exception_flag, "viewing_array":viewing_array}, daemon=True).start()
    if(options["scan"]):
        threading.Thread(target=get_open_ports, kwargs={"exception_flag":exception_flag, "viewing_array":viewing_array}, daemon=False).start()
    with ThreadPoolExecutor(max_workers=options['max_threads']) as executor:
        for host in network.hosts():
            if(exception_flag.is_set()):
                return
            executor.submit(discover,ip_address=str(host),exception_flag=exception_flag,viewing_array=viewing_array)
        
            

def main():
    try:
        print(options)
        print(Fore.GREEN+"[+] getting native networking configuration")
        ip,subnet = get_host_ip_subnetmask()
        print(Fore.GREEN+"[+] getting network details")
        network_add = binaryAnd(ip,subnet)
        print(Fore.GREEN+"[+] starting discovery process")
        print(Fore.RESET)
        if(options['should_log']):
             threading.Thread(target=logger, daemon=True).start()
        mainLoop(network_add,subnet)
        
    except KeyboardInterrupt:
        exception_flag.set()
        exit(1)
    except Exception as e:
        print("err",e)
        exception_flag.set()
        exit(1)






