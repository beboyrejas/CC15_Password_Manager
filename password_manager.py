from tkinter import *

mywindow = Tk() #Change the name for every window you make
mywindow.title("Password Manager") #This will be the window title
mywindow.geometry("540x420") #This will be the window size (str)
mywindow.minsize(540, 420) #This will be set a limit for the window's minimum size (int)
mywindow.configure(bg="grey") #This will be the background color

mywindow.mainloop() #You must add this at the end to show the window