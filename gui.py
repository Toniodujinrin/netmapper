from tkinter import * 
from worker import main,gloabl_queue

root = Tk()

root.geometry("600x600")
root.title("Netmapper")
root.configure(background="black")
root.resizable(False, False)

start = Button(text="Start", command=lambda: main(),  width=10, height=3, background="green", borderwidth=0, highlightcolor="green" ).grid(row=1,column=1)


root.mainloop()