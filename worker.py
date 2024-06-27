import threading
import socket 
import os 
import subprocess
import struct
from concurrent.futures import ThreadPoolExecutor
import ipaddress
from colorama import Fore
from time import sleep

from processes.discover import discover
from processes.get_responses import calculate_response_time
from processes.get_mac_details import get_mac_details
from processes.port_scanner import get_open_ports
from processes.logger import logger


try:
    import fcntl
except ImportError:
    pass


options = {}
exception_flag = threading.Event()
log_exception_flag = threading.Event()
viewing_array = []
discovery_finsihed = threading.Event()




def get_host_ip_subnetmask ():
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sock:
        sock.connect(("8.8.8.8",80))
        ip,port = sock.getsockname()
        subnet_mask = ""
        if(os.name == "nt"):
            res = subprocess.run("ipconfig",capture_output=True )
            res = res.stdout.decode().replace(". ","").split("\n")
            for item in res:
                if "Subnet Mask" in item:
                    subnet_mask = item 
            subnet_mask = subnet_mask.replace("Subnet Mask :","").strip()
        else:
            subnet_mask = fcntl.ioctl(sock.fileno(), 0x891b, struct.pack(
            '256s', "wlan0".encode()))[20:24]
            subnet_mask = socket.inet_ntoa(subnet_mask)
        sock.close()
        return (ip,subnet_mask)

def get_network_address(ip_address:str, subnet_mask:str):
    subnet_mask_array = subnet_mask.split(".")
    ip_address_array =  ip_address.split(".")
    
    network_address_array = []
    for i in range(len(ip_address_array)):
        network_address_array.append(int(subnet_mask_array[i]) & int(ip_address_array[i]))
    network_address_array = [str(byte) for byte in network_address_array] 
    network_address = ".".join(network_address_array)
    print(network_address)
    return network_address 
     

            
process_threads = []
log_thread = None 
def main_loop(network_address,subnet_mask):
    network = ipaddress.IPv4Network(f"{network_address}/{subnet_mask}", strict=False)
 
    if(options["response"]):
        thread = threading.Thread(target=calculate_response_time,kwargs={"exception_flag":exception_flag, "viewing_array":viewing_array, "discovery_finished":discovery_finsihed})
        thread.start()
        process_threads.append(thread)
    if(options["hardware"]):
        thread = threading.Thread(target=get_mac_details,kwargs={"exception_flag":exception_flag, "viewing_array":viewing_array, "discovery_finished":discovery_finsihed})
        thread.start()
        process_threads.append(thread)
    if(options["scan"]):
        thread =threading.Thread(target=get_open_ports, kwargs={"exception_flag":exception_flag, "viewing_array":viewing_array, "discovery_finished":discovery_finsihed})
        thread.start()
        process_threads.append(thread)
    if(options['should_log']):
        log_thread = threading.Thread(target=logger, kwargs={"exception_flag":exception_flag, "log_exception_flag":log_exception_flag, "viewing_array":viewing_array, "options":options, "discovery_finished":discovery_finsihed})
        log_thread.start()
        
    with ThreadPoolExecutor(max_workers=options['max_threads']) as executor:
        for host in network.hosts():
            if(exception_flag.is_set()):
                print("flag set")
                return
            executor.submit(discover,ip_address=str(host),exception_flag=exception_flag,viewing_array=viewing_array)
        executor.shutdown()
        print("done with discovery")
        discovery_finsihed.set()
        
        
            

def main():
    try:
        print(Fore.GREEN+"[+] getting native networking configuration")
        ip,subnet = get_host_ip_subnetmask()
        print(Fore.GREEN+"[+] getting network details")
        network_address = get_network_address(ip,subnet)
        print(Fore.GREEN+"[+] starting discovery process")
        print(Fore.RESET)
        sleep(3)
        main_loop(network_address,subnet)
        for thread in process_threads:
            thread.join()
        log_exception_flag.set()
        if(log_thread):
            log_thread.join()
        print(Fore.GREEN+"[+] all proccess exited")
        print(Fore.RESET)
    except KeyboardInterrupt:
        exception_flag.set()
        exit(1)
    except Exception as e:
        print(e)
        exception_flag.set()
        exit(1)






