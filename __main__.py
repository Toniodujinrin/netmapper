import  pyfiglet 
from worker import main, options
import argparse
from gui import root
import os
from colorama import Fore
from gui import root
import sys



print(pyfiglet.Figlet().renderText("Netmapper"))

if(os.name != "nt" and os.getuid() != 0 ):
    print(Fore.RED,"[x] You must have root priveledges to run this application, exiting ...")
    print(Fore.RESET)
    exit()



usage = """

Usage:

-d -discover: perform host discovery

-t<1-3> -timing<1-3> : set timing and decretion( 1-slow but very discrete, 3-fast but not discrete)

-g -gui: open GUI( still in production)

-s -scan: scan host open ports

-r -response: show average response times and TTL

-o -os: perform os detection(still in production)

-m -hard: gather hardware details

Example: python3 netmapper -d -t 3 -s -r -o -h

"""
timing = None
gui = None
discover = None
hardware = None 
scan = None
response = None 
def get_args():
    global timing
    global gui
    global discover
    global hardware
    global scan 
    global response
    arguments = sys.argv[1:]
    if (len(arguments) == 0):
        print(usage)
        exit(0)
    parser = argparse.ArgumentParser()
    parser.add_argument("-g","-gui",help="open gui interface",action="store_true")
    parser.add_argument('-t',"-timing",help="set timing")
    parser.add_argument("-d","-discover", help="commence discovery", action="store_true")
    parser.add_argument("-m","-hard", help="get hardware details", action="store_true")
    parser.add_argument("-s","-scan", help="scan for open ports", action="store_true")
    parser.add_argument("-r","-response", help="get average response time and ttl", action="store_true")
    try:
        args = parser.parse_args(arguments)
        for arg in args._get_kwargs():
            if(arg[0] == "g"):
                gui = arg[1]
            elif(arg[0] == "d"):
                discover = arg[1]
            elif(arg[0]== "t" and arg[1]):
                timing = arg[1]
            elif(arg[0] == "m"):
                hardware = arg[1]
            elif(arg[0]== "s"):
                scan = arg[1]
            elif(arg[0] == "r"):
                response = arg[1]
    except Exception as e:
        print(e)



def commence():
    global timing 
    global gui
    global discover
    global hardware
    global scan 
    global response
    
    options["header"] = ["ip_address","mac_address","host_name"]
    options["scan"] = False
    options["response"] = False
    options["hardware"] = False
    if (timing):
        
        if(timing == "1"):
            options['max_threads'] = 50
        elif(timing == "2"):
            options['max_threads'] = 100
        elif(timing == "3"):
            options['max_threads'] = 200
        else:
            print(Fore.LIGHTYELLOW_EX,"[-] Invalid timing value set, using default timing of 1")
            options['max_threads'] = 50
            print(Fore.RESET)
    else:
        print(Fore.LIGHTYELLOW_EX,"[-] Timing flag not set, using default timing of 1")
        options['max_threads'] = 50
        print(Fore.RESET)
    if(hardware):
        options["header"].append("producer")
        options["hardware"] = True 
    if(response):
          options["header"].append("average_response_time")
          options["header"].append("ttl")
          options["response"]= True 
    if(scan):
        options["header"].append("open_ports")
        options["scan"] = True
    if(gui and discover):
        print(Fore.RED,"[x] You cannot run gui and cli simultaneously, exiting ...")
        print(Fore.RESET)
        exit(1)

    if(gui):
        options['should_log'] = False 
        root.mainloop()
    elif(discover):
        options['should_log'] = True
        main()  
    else:
        print(Fore.RED,"[x] No requests made, exiting ...")
        print(Fore.RESET)
        exit(0)






get_args()
commence()




