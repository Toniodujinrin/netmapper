import  pyfiglet 
from worker import main
import argparse
from gui import root
import os
from colorama import Fore
import time
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

print("use -h for help")
arguments = sys.argv[1:]

if (len(arguments) == 0):
    print(usage)
parser = argparse.ArgumentParser()
parser.add_argument("-g","-gui",help="open gui interface",action="store_true")
args = parser.parse_args(arguments)
print(args)


