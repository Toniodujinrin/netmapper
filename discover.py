from scapy.all import *
import requests

conf.verb = 0 

def get_mac_details(mac):
    try:
        res = requests.get(f"https://www.macvendorlookup.com/api/v2/{mac}")
        company = res.json()[0].get("company",0)
        return company
    except Exception as x:
        return "N/A"
    



def discover(ip_address, queue, exception_flag):
    if(not exception_flag.is_set()):
        try:
            mac = ""
            hostName = ""
            responses, unanswered = srp(
                Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address), retry=3, timeout=3)
            for req, res in responses:
                mac = res.src
            try:
                hostName = socket.gethostbyaddr(ip_address)[0]
            except Exception:
                hostName="N/A"
            if (mac):
                company = get_mac_details(mac)
                queue.put({"ip_address":ip_address,"mac_address":mac,"producer":company,"host_name":hostName})
                
        except PermissionError:
            print("permision Error occured, run this program as root user")
            exception_flag.set()
            exit(1)
        except Exception as e :
            print(e)
            return 

