import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk             
from PIL import ImageTk, Image
import pymysql
import os
import shutil
# import db_config

mywindow = tk.Tk() #Change the name for every window you make
mywindow.title("Password Manager") #This will be the window title
mywindow.geometry("540x280") #This will be the window size (str)
mywindow.minsize(540, 280) #This will be set a limit for the window's minimum size (int)
mywindow.configure(bg="grey") #This will be the background color

# tabs

tab_parent = ttk.Notebook(mywindow)
tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)
tab4 = ttk.Frame(tab_parent)
tab_parent.add(tab1, text="All Accounts")
tab_parent.add(tab2, text="Add New Account")
tab_parent.add(tab3, text="Update Old Account")
tab_parent.add(tab4, text="Delete Old Account")
tab_parent.pack(expand=1, fill='both')

# widgets

addAppLabel = tk.Label(tab2, text="Website/Application:")
addUserLabel = tk.Label(tab2, text="Username:")
addPasswordLabel = tk.Label(tab2, text="Password:")

addWebEntry = tk.Entry(tab2)
addUserEntry = tk.Entry(tab2)
addPasswordEntry = tk.Entry(tab2)

buttonGenerate = tk.Button(tab2, text="Generate")
buttonAdd = tk.Button(tab2, text="Add")

# add widgets
addAppLabel.grid(row=0, column=0, padx=5, pady=15)
addWebEntry.grid(row=0, column=1, padx=5, pady=15)

addUserLabel.grid(row=1, column=0, padx=5, pady=15)
addUserEntry.grid(row=1, column=1, padx=5, pady=15)

addPasswordLabel.grid(row=2, column=0, padx=5, pady=15)
addPasswordEntry.grid(row=2, column=1, padx=5, pady=15)

buttonGenerate.grid(row=2, column=2, padx=5, pady=15)
buttonAdd.grid(row=3, column=2, padx=5, pady=15)

mywindow.mainloop() #You must add this at the end to show the window