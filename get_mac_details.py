import requests 


def get_mac_details(data_lock, viewing_array,exception_flag):
    counter = 0 
    while not exception_flag.is_set():
        if(len(viewing_array) > counter):
            host = viewing_array[counter]
            try:
                mac = host.get("mac_address",0)
                if(mac):
                    res = requests.get(f"https://api.maclookup.app/v2/macs/{mac}?apiKey=01hke6r9qg9kqbgz6kcpcwmk6m01hke6sxtg6jtchas1txx4qe2reqazgkqduxcz")
                    company =  res.json().get("company","N/A")
                    if(len(company) == 0): company = "N/A"
                    host["producer"] = company        
            except Exception as x:
                host["producer"] = "N/A"
            counter += 1 