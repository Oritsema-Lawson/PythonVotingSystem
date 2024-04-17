import os
import util.setup as setup

if not os.path.exists("database/voting.db"):
    setup.setup_app()
    if not os.path.exists("database/voting.db"):
        exit()

import sqlite3
import customtkinter
from CTkMessagebox import CTkMessagebox
from tkinter import messagebox
from tkinter import ttk
import util.database_operations as db
import re

import util.voter as voter
import util.admin as admin

# Create the main GUI window and database
root = customtkinter.CTk()

# Function to validate that the entered name is a full name with first and last name separated by a space
def check_full_name(name):
    pattern = r'^[a-zA-Z]+\s[a-zA-Z]+$' # Regular expression to match first and last name separated by a space
    if re.match(pattern, name):
        return True
    else:
        return False

# Function to destroy the login window and create the voter UI, passing the username  
def create_voter_ui(name):
    root.destroy()
    voter.create_voting_ui(name)

# Function to destroy the login window and create the admin UI
def create_admin_ui():
    root.destroy()
    admin.show_admin_ui()

# Function to handle sign up button
def sign_up():
    username = name2_entry.get()
    password = pass2_entry.get()
    confirm = confirm_entry.get()
    if username != '' and password != '' and confirm != '':
        if check_full_name(username):
            if not db.check_if_user_exists(username):
                if password == confirm :
                    # Add user to the database with voter authorization and open voter UI
                    db.add_user(username, password, "VOTER")
                    create_voter_ui(username)
                else:
                    messagebox.showerror('Error',"Passwords do not match")
            else:
                messagebox.showerror('Error', 'User already registered, please contact your admin if you forgot your password')
        else:
            messagebox.showerror('Error', 'Please enter your first and last name into the name field')
    else:
        messagebox.showerror('Error',"Please fill in all the fields")

# Function to handle sign in button
def sign_in():
    name = name_entry.get()
    password = pass_entry.get()

    result = db.check_login(name, password)

    if result[0] == "NOT_EXIST":
        CTkMessagebox(title="Login Failed", message="Invalid username")
    elif result[0] == "INCORRECT_PASS":
        CTkMessagebox(title="Login Failed", message="Incorrect password")
    else:
        if result[1] == "VOTER":
            create_voter_ui(result[0]) # Create voter UI for successful voter login
        elif result[1] == "ADMIN":
            create_admin_ui()  # Create admin UI for successful admin login

main_font = ('Arial', 15, 'bold')
head_font = ('Arial', 18, 'bold')

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
root.geometry('960x540')
root.title('Login')
root.resizable(False,False)

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

#LOGIN
log_tab = customtkinter.CTkFrame(notebook)
notebook.add(log_tab, text='Login')

head_label = customtkinter.CTkLabel(log_tab,font=head_font, text='Login')
head_label.grid(column=0, row=0, padx=10, pady=10,)

name_label=customtkinter.CTkLabel(master=log_tab, text="Login:",font=head_font)
name_label.place(relx=0.34, rely=0.3,)

name_entry=customtkinter.CTkEntry(master=log_tab, width=220, placeholder_text='Username')
name_entry.place(relx=0.4,rely=0.3)

pass_label=customtkinter.CTkLabel(master=log_tab, text="Password:",font=head_font)
pass_label.place(relx=0.3, rely=0.4,)

pass_entry=customtkinter.CTkEntry(master=log_tab, width=220, placeholder_text='Password', show="*")
pass_entry.place(relx=0.4,rely=0.4)

#SIGN UP
signup_tab = customtkinter.CTkFrame(notebook)
notebook.add(signup_tab, text='Sign Up')

head2_label = customtkinter.CTkLabel(signup_tab,font=head_font, text='Sign Up')
head2_label.grid(column=0, row=0, padx=10, pady=10,)

name2_label=customtkinter.CTkLabel(master=signup_tab, text="Name:",font=head_font)
name2_label.place(relx=0.34, rely=0.3,)

name2_entry=customtkinter.CTkEntry(master=signup_tab, width=220, placeholder_text='Username')
name2_entry.place(relx=0.4,rely=0.3)

pass2_label=customtkinter.CTkLabel(master=signup_tab, text="Password:",font=head_font)
pass2_label.place(relx=0.3, rely=0.4,)

pass2_entry=customtkinter.CTkEntry(master=signup_tab, width=220, placeholder_text='Password', show="*")
pass2_entry.place(relx=0.4,rely=0.4)

confirm_label=customtkinter.CTkLabel(master=signup_tab, text="Confirm:",font=head_font)
confirm_label.place(relx=0.322, rely=0.5,)

confirm_entry=customtkinter.CTkEntry(master=signup_tab, width=220, placeholder_text='Confirm Password', show="*")
confirm_entry.place(relx=0.4,rely=0.5)

#LOGIN AND SIGN UP BUTTONS
log_button = customtkinter.CTkButton(master=log_tab, width=180, text="Login", corner_radius=6, command=sign_in)
log_button.place(relx=0.418,rely=0.5)

sign_button = customtkinter.CTkButton(master=signup_tab, width=180, text="Login", corner_radius=6, command=sign_up)
sign_button.place(relx=0.418,rely=0.6)

root.mainloop()