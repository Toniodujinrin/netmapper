import  pyfiglet 
from worker import main
import argparse
from gui import root
import os
from colorama import Fore
import time
from gui import root
import sys



print(pyfiglet.Figlet().renderText("Netmapper"))

if(not os.getuid() ==0 ):
    print(Fore.RED,"[x] You must have root priveledges to run this application, exiting ...")
    print(Fore.RESET)
    exit()

usage = """

Usage:
-g : open graphical interface 
-d : commence discovery 
-t : set speed <1-3>



"""
timing = 1
gui = None
discover = None
def get_args():
    global timing
    global gui
    global discover
    arguments = sys.argv[1:]
    if (len(arguments) == 0):
        print(usage)
    parser = argparse.ArgumentParser()
    parser.add_argument("-g","-gui",help="open gui interface",action="store_true")
    parser.add_argument('-t',"-timing",help="set timing")
    parser.add_argument("-d","-discover", help="commence discovery", action="store_true")
    args = parser.parse_args(arguments)
    for arg in args._get_kwargs():
        if(arg[0] == "g"):
            gui = arg[1]
        elif(arg[0] == "d"):
            discover = arg[1]
        elif(arg[0]== "t" and arg[1]):
            timing = arg[1]

def commence():
    global timing 
    global gui
    global discover

    if(gui and discover):
        print(Fore.RED,"[x] You cannot run gui and cli simultaneously, exiting ...")
        print(Fore.RESET)
        exit(1)
    if(gui):
        root.mainloop()
    elif(discover):
        main()
        
    else:
        print(Fore.RED,"[x] No requests made, exiting ...")
        print(Fore.RESET)
        exit(0)






get_args()
commence()




