import tkinter as tk
from tkinter import DISABLED, StringVar, messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter.font import NORMAL             
from PIL import ImageTk, Image
import pymysql
import os
import shutil
import password_db_config
from encrypt_pass import *
from generate_pass import *

# functions
def connect():
    con = pymysql.connect(host=password_db_config.DB_SERVER,
                                user=password_db_config.DB_USER,
                                password=password_db_config.DB_PASS,
                                database=password_db_config.DB,
                                port=password_db_config.DB_PORT)
    return con

def on_tab_selected(event):
    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")
    if tab_text == "All Accounts":
        print("All Accounts tab selected")
    if tab_text == "Add New Account":
        print("Add New Account tab selected")
    if tab_text == "Update Old Account":
        print("Update Old Account tab selected")
    if tab_text == "Delete Old Account":
        print("Delete Old Account tab selected")
    clear()

# may be deleted start
def load_database_results():
    global rows
    global num_of_rows

    try:
        con = connect()
        sql = "SELECT * FROM accounts"
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        num_of_rows = cur.rowcount
        cur.close()
        con.close()
        has_loaded_successfully = True
        # messagebox.showinfo("Connected to Database", "Connected OK")
    except pymysql.InternalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.OperationalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.ProgrammingError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DataError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.IntegrityError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.NotSupportedError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DatabaseError as e:
        has_loaded_successfully = database_error(e)

    return has_loaded_successfully
# may be deleted end

def database_error(err):
    messagebox.showinfo("Error", err)
    return False

def clear():
    tab = tab_parent.select()
    print(tab)
    if tab == ".!notebook.!frame":
        search_website.set("")
        search_username.set("")
    if tab == ".!notebook.!frame2":
        add_website.set("")
        add_username.set("")
        add_password.set("")
        addWebEntry.focus()
    if tab == ".!notebook.!frame3":
        update_website.set("")
        update_username.set("")
        update_old_password.set("")
        update_new_password.set("")       
        updateWebEntry.focus()
    if tab == ".!notebook.!frame4":
        delete_website.set("")
        delete_username.set("")
        delWebEntry.focus()

def generate_password():
    password = randomPass(characters)
    tab = tab_parent.select()
    if tab == ".!notebook.!frame2":
        add_password.set(password)
    if tab == ".!notebook.!frame3":
        update_new_password.set(password)

def add_new_account():
    if add_website.get() == "" or add_username.get() == "" or add_password.get() == "":
        messagebox.showerror("Error", "Please fill in all fields")
        
    else:
        messagebox.showinfo("Success","New Account Added to Database")
        encryptMe = encrypt(add_password.get(), shift)
        try:
            con = connect()
            cur = con.cursor()
            sql = """insert into `accounts` (website, username, password) values (%s, %s, %s)"""
            cur.execute(sql,(add_website.get(), add_username.get(), encryptMe))
            con.commit()
            cur.close()
            con.close()
        except pymysql.InternalError as e:
            has_loaded_successfully = database_error(e)
        except pymysql.OperationalError as e:
            has_loaded_successfully = database_error(e)
        except pymysql.ProgrammingError as e:
            has_loaded_successfully = database_error(e)
        except pymysql.DataError as e:
            has_loaded_successfully = database_error(e)
        except pymysql.IntegrityError as e:
            has_loaded_successfully = database_error(e)
        except pymysql.NotSupportedError as e:
            has_loaded_successfully = database_error(e)
        except pymysql.DatabaseError as e:
            has_loaded_successfully = database_error(e)
        clear()
    return

def delete_account():
    try:
        con = connect()
        cur = con.cursor()
        sql = "select * from accounts where website = %s and username = %s"
        cur.execute(sql, (delete_website.get(), delete_username.get()))
        if cur.fetchone():
            deleteChoice = messagebox.askyesno("Warning","Are You Sure You Want to Delete this Account?")
            if deleteChoice > 0:
                sql = """Delete from `accounts` where website = %s and username = %s"""
                cur.execute(sql, (delete_website.get(), delete_username.get())) 
                messagebox.showinfo("Success","Account Deleted from Database")
        else :
            messagebox.showerror("Error","Account Does Not Exist in Database")
        con.commit()
        cur.close()
        con.close()
    except pymysql.InternalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.OperationalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.ProgrammingError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DataError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.IntegrityError as e:
       has_loaded_successfully = database_error(e)
    except pymysql.NotSupportedError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DatabaseError as e:
       has_loaded_successfully = database_error(e)
    return

    
def update_account():
    try:
        con = connect()
        cur = con.cursor()
        sql = "select * from accounts where website = %s and username = %s"
        cur.execute(sql, (update_website.get(), update_username.get()))
        if cur.fetchone():
            sql = """Select password from `accounts` where website = %s and username = %s"""
            cur.execute(sql, (update_website.get(), update_username.get()))
            old_password = cur.fetchone()
            if decrypt(old_password[0], shift) == update_new_password.get():
                messagebox.showerror("Error","New Password Cannot be the Same as Old Password")
                return
            if update_new_password.get() == "":
                messagebox.showerror("Error","Please Enter a New Password")
                return
            updateChoice = messagebox.askyesno("Warning","Are You Sure You Want to Change the Password for this Account?")
            if updateChoice > 0:
                encryptMe = encrypt(update_new_password.get(), shift)
                sql = """Update `accounts` set password = %s where website = %s and username = %s"""
                cur.execute(sql, (encryptMe, update_website.get(), update_username.get()))
                messagebox.showinfo("Success","Account Updated in Database")
        else :
            messagebox.showerror("Error","Account Does Not Exist in Database")
        con.commit()
        cur.close()
        con.close()
    except pymysql.InternalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.OperationalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.ProgrammingError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DataError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.IntegrityError as e:
       has_loaded_successfully = database_error(e)
    except pymysql.NotSupportedError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DatabaseError as e:
       has_loaded_successfully = database_error(e)
    return

def call_pass(event):
    try:
        con = connect()
        cur = con.cursor()
        sql = """Select password from `accounts` where website = %s and username = %s"""
        cur.execute(sql, (update_website.get(), update_username.get()))
        old_password = cur.fetchone() 
        update_old_password.set(decrypt(old_password[0], shift))
        con.commit()
    except TypeError as e:
        messagebox.showerror("Error","Please Fill Out All Fields")
    except pymysql.InternalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.OperationalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.ProgrammingError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DataError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.IntegrityError as e:
       has_loaded_successfully = database_error(e)
    except pymysql.NotSupportedError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DatabaseError as e:
       has_loaded_successfully = database_error(e)

def conditional_search():
    clear_treeview()
    if search_website.get() != "" and search_username.get() == "":
        website_search()
    elif search_website.get() == "" and search_username.get() != "":
        username_search()
    elif search_website.get() != "" and search_username.get() != "":
        website_username_search()
    else:
        messagebox.showerror("Error","Please Enter a Search Term")  
    return

def website_search():
    try:
        con = connect()
        cur = con.cursor()
        sql = """Select * from `accounts` where website = %s"""
        cur.execute(sql, (search_website.get()))
        if cur.fetchone():
            sql = """Select * from `accounts` where website = %s"""
            cur.execute(sql, (search_website.get()))
            for i in cur.fetchall():
                tree.insert("", 0, values=(i[0],i[1],decrypt(i[2], shift)))
            clear()
        else :
            messagebox.showerror("Error","Account Does Not Exist in Database")
        con.commit()
        cur.close()
        con.close()
    except pymysql.InternalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.OperationalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.ProgrammingError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DataError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.IntegrityError as e:
       has_loaded_successfully = database_error(e)
    except pymysql.NotSupportedError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DatabaseError as e:
       has_loaded_successfully = database_error(e)
    return

def username_search():
    try:
        con = connect()
        cur = con.cursor()
        sql = """Select * from `accounts` where username = %s"""
        cur.execute(sql, (search_username.get()))
        if cur.fetchone():
            sql = """Select * from `accounts` where username = %s"""
            cur.execute(sql, (search_username.get()))
            for i in cur.fetchall():
                tree.insert("", 0, values=(i[0],i[1],decrypt(i[2], shift)))
            clear()
        else :
            messagebox.showerror("Error","Account Does Not Exist in Database")
        con.commit()
        cur.close()
        con.close()
    except pymysql.InternalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.OperationalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.ProgrammingError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DataError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.IntegrityError as e:
       has_loaded_successfully = database_error(e)
    except pymysql.NotSupportedError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DatabaseError as e:
       has_loaded_successfully = database_error(e)
    return

def website_username_search():
    try:
        con = connect()
        cur = con.cursor()
        sql = """Select * from `accounts` where website = %s and username = %s"""
        cur.execute(sql, (search_website.get(), search_username.get()))
        if cur.fetchone():
            sql = """Select * from `accounts` where website = %s and username = %s"""
            cur.execute(sql, (search_website.get(), search_username.get()))
            for i in cur.fetchall():
                tree.insert("", 0, values=(i[0],i[1],decrypt(i[2], shift)))
            clear()
        else :
            messagebox.showerror("Error","Account Does Not Exist in Database")
        con.commit()
        cur.close()
        con.close()
    except pymysql.InternalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.OperationalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.ProgrammingError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DataError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.IntegrityError as e:
       has_loaded_successfully = database_error(e)
    except pymysql.NotSupportedError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DatabaseError as e:
       has_loaded_successfully = database_error(e)
    return

# function to check if account already exists
def check_account():
    try:
        con = connect()
        cur = con.cursor()
        sql = """Select * from `accounts` where website = %s and username = %s"""
        cur.execute(sql, (add_website.get(), add_username.get()))
        if cur.fetchone():
            messagebox.showerror("Error","Account Already Exists")
            return False
        else:
            add_new_account()
            return True
    except pymysql.InternalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.OperationalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.ProgrammingError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DataError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.IntegrityError as e:
       has_loaded_successfully = database_error(e)
    except pymysql.NotSupportedError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DatabaseError as e:
       has_loaded_successfully = database_error(e)
    return

# function to clear treeview
def clear_treeview():
    tree.delete(*tree.get_children())
    return

# variables

file_name = "default.png"
path = password_db_config.PHOTO_DIRECTORY + file_name
rows = None # may be removed
num_of_rows = None # may be removed
shift = 5

# main window

mywindow = tk.Tk() #Change the name for every window you make
mywindow.title("Password Manager") #This will be the window title
mywindow.geometry("430x280") #This will be the window size (str)
mywindow.minsize(430, 280) #This will be set a limit for the window's minimum size (int)
mywindow.configure(bg="grey") #This will be the background color

# ===TABS===

tab_parent = ttk.Notebook(mywindow)
tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)
tab4 = ttk.Frame(tab_parent)
tab_parent.bind("<<NotebookTabChanged>>", on_tab_selected)
tab_parent.add(tab1, text="All Accounts")
tab_parent.add(tab2, text="Add New Account")
tab_parent.add(tab3, text="Update Old Account")
tab_parent.add(tab4, text="Delete Old Account")
tab_parent.pack(expand=1, fill='both')

# ===WIDGETS===
search_website = StringVar()
search_username = StringVar()
search_website.set("")
search_username.set("")
add_website = StringVar()
add_username = StringVar()
add_password = StringVar()
add_website.set("")
add_username.set("")
add_password.set("")
update_website = StringVar()
update_username = StringVar()
update_old_password = StringVar()
update_new_password = StringVar()
update_website.set("")
update_username.set("")
update_old_password.set("")
update_new_password.set("")
delete_website = StringVar()
delete_username = StringVar()
delete_website.set("")
delete_username.set("")


# ===TAB 1===
# create a frame for the tab 1 with a fixed height and color and anchored at top
tab1_frame = tk.Frame(tab1, height=100, width=400, borderwidth=1)
tab1_frame.pack(expand=1, fill='x', anchor='n')

scrollbar = ttk.Scrollbar(tab1_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(tab1_frame, height=8, columns=("Website", "Username", "Password"), show="headings", yscrollcommand=scrollbar.set)
tree.column("Website", width=100, anchor="center")
tree.column("Username", width=100, anchor="center")
tree.column("Password", width=100, anchor="center")
tree.heading("Website", text="Website")
tree.heading("Username", text="Username")
tree.heading("Password", text="Password")
tree.pack(expand=1, fill='x')

scrollbar.config(command=tree.yview)


tab1_frame2 = tk.Frame(tab1, height=100, width=400, borderwidth=1)
tab1_frame2.pack(expand=1, fill='x', anchor='n')
# create entry boxes for the tab1_frame2
searchWebLabel = tk.Label(tab1_frame2, text="Website:")
searchUsernameLabel = tk.Label(tab1_frame2, text="Username:")

searchWebEntry = tk.Entry(tab1_frame2, textvariable=search_website, width=17)
searchUsernameEntry = tk.Entry(tab1_frame2, textvariable=search_username, width=17)
searchWebLabel.grid(row=0, column=0, sticky="n", padx=5, pady=5)
searchUsernameLabel.grid(row=0, column=2, sticky="n", padx=5, pady=5)
searchWebEntry.grid(row=0, column=1, sticky="n", padx=5, pady=5)
searchUsernameEntry.grid(row=0, column=3, sticky="n", padx=5, pady=5)

# create a button for the tab1_frame2 below the entry boxes
searchButton = tk.Button(tab1_frame2, text="Search", command=conditional_search)
searchButton.grid(row=0, column=4, sticky="n", padx=5, pady=5)


# tab2
addAppLabel = tk.Label(tab2, text="Website/Application:")
addUserLabel = tk.Label(tab2, text="Username:")
addPasswordLabel = tk.Label(tab2, text="Password:")

addWebEntry = tk.Entry(tab2, textvariable=add_website, state=NORMAL)
addUserEntry = tk.Entry(tab2, textvariable=add_username, state=NORMAL)
addPasswordEntry = tk.Entry(tab2, textvariable=add_password, state=NORMAL)

buttonGenerate = tk.Button(tab2, text="Generate", command=generate_password)
buttonAdd = tk.Button(tab2, text="Add", command=check_account)

# tab3
updateAppLabel = tk.Label(tab3, text="Website/Application:")
updateUserLabel = tk.Label(tab3, text="Username:")
updateOldPasswordLabel = tk.Label(tab3, text="Old Password:")
updateNewPasswordLabel = tk.Label(tab3, text="New Password:")

updateWebEntry = tk.Entry(tab3, textvariable=update_website, state=NORMAL)
updateUserEntry = tk.Entry(tab3, textvariable=update_username, state=NORMAL)
updateOldPasswordEntry = tk.Entry(tab3, textvariable=update_old_password, state=DISABLED)
updateNewPasswordEntry = tk.Entry(tab3, textvariable=update_new_password, state=NORMAL)
updateNewPasswordEntry.bind("<1>",call_pass)


buttonGenerate2 = tk.Button(tab3, text="Generate", command=generate_password)
buttonUpdate = tk.Button(tab3, text="Update", command=update_account)

# tab4
delAppLabel = tk.Label(tab4, text="Website/Application:")
delUserLabel = tk.Label(tab4, text="Username:")

delWebEntry = tk.Entry(tab4, textvariable=delete_website, state=NORMAL)
delUserEntry = tk.Entry(tab4, textvariable=delete_username, state=NORMAL)

buttonDel = tk.Button(tab4, text="Delete", command=delete_account)

# ===ADD WIDGETS TO TABS===

# tab1


# tab2
addAppLabel.grid(row=0, column=0, padx=15, pady=15)
addWebEntry.grid(row=0, column=1, padx=15, pady=15)

addUserLabel.grid(row=1, column=0, padx=15, pady=15)
addUserEntry.grid(row=1, column=1, padx=15, pady=15)

addPasswordLabel.grid(row=2, column=0, padx=15, pady=15)
addPasswordEntry.grid(row=2, column=1, padx=15, pady=15)

buttonGenerate.grid(row=3, column=1, padx=15, pady=15)
buttonAdd.grid(row=3, column=2, padx=15, pady=15)

# tab3
updateAppLabel.grid(row=0, column=0, padx=15, pady=15)
updateWebEntry.grid(row=0, column=1, padx=15, pady=15)

updateUserLabel.grid(row=1, column=0, padx=15, pady=15)
updateUserEntry.grid(row=1, column=1, padx=15, pady=15)

updateOldPasswordLabel.grid(row=2, column=0, padx=15, pady=15)
updateOldPasswordEntry.grid(row=2, column=1, padx=15, pady=15)

updateNewPasswordLabel.grid(row=3, column=0, padx=15, pady=15)
updateNewPasswordEntry.grid(row=3, column=1, padx=15, pady=15)

buttonGenerate2.grid(row=4, column=1, padx=15, pady=15)
buttonUpdate.grid(row=4, column=2, padx=15, pady=15)

# tab4
delAppLabel.grid(row=0, column=0, padx=15, pady=15)
delWebEntry.grid(row=0, column=1, padx=15, pady=15)

delUserLabel.grid(row=1, column=0, padx=15, pady=15)
delUserEntry.grid(row=1, column=1, padx=15, pady=15)

buttonDel.grid(row=3, column=2, padx=15, pady=15)



success = load_database_results() #may be removed
mywindow.mainloop() #You must add this at the end to show the window