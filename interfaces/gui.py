from tkinter import * 
from worker import main,exception_flag
from interfaces.tkinterTools import makeButton


root = Tk()

root.geometry("600x600")
root.title("Netmapper")
root.configure(background="black")
root.resizable(False, False)

def checkForException():
    if(exception_flag.is_set()):
        Label(root,text="an Error occured", foreground="red", background="black").grid(row=2, column=2)

    root.after(1000,checkForException)


checkForException()

button = makeButton(root,"black",main,"Start",60,100,"green","white").grid(row=1,column=1)






