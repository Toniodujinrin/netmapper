from scapy.all import *
import requests

conf.verb = 0 

# def get_mac_details(mac):
#     try:
#         res = requests.get(f"https://api.maclookup.app/v2/macs/{mac}?apiKey=01hke6r9qg9kqbgz6kcpcwmk6m01hke6sxtg6jtchas1txx4qe2reqazgkqduxcz")
#         company =  res.json().get("company","N/A")
#         if(company and len(company)> 1):
#             return company
#         return "N/A"
#     except Exception as x:
#         return "N/A"
    



def discover(ip_address,viewing_array, exception_flag):
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
                viewing_array.append({"ip_address":ip_address,"mac_address":mac,"host_name":hostName})
                
        except PermissionError:
            print("permision Error occured, run this program as root user")
            exception_flag.set()
            exit(1)
        except Exception as e :
            print(e)
            return 

