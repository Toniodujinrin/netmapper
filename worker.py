import threading
from queue import Queue
import socket 
import struct
import fcntl
from discover import discover
from concurrent.futures import ThreadPoolExecutor
import ipaddress
from colorama import Fore
from osFinder import calculateResponseTime


gloabl_queue = Queue()

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


def mainLoop(network_address,subnet_mask):
    network_address_string = [str(i) for i in network_address]
    network_address_string =  ".".join(network_address_string)
    network = ipaddress.IPv4Network(f"{network_address_string}/{subnet_mask}", strict=False)
    max_threads = 10 
    threading.Thread(target=calculateResponseTime,args=(gloabl_queue,), daemon=True).start()
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
     
        for host in network.hosts():
            executor.submit(discover,ip_address=str(host),queue=gloabl_queue)
            

def main():
    print(Fore.GREEN+"[+] getting native networking configuration")
    ip,subnet = get_host_ip_subnetmask()
    print(Fore.GREEN+"[+] getting network details")
    network_add = binaryAnd(ip,subnet)
    print(Fore.GREEN+"[+] starting discovery process")
    mainLoop(network_add,subnet)


