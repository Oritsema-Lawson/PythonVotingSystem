def setup_app():  
    import subprocess
    import os
    # Install required packages
    subprocess.run(["pip", "install", "-r", "requirements.txt"])

    import customtkinter
    from tkinter import messagebox
    import util.database_operations as db
    import re

    customtkinter.set_appearance_mode("Dark")  # Set appearance mode to dark

    root = customtkinter.CTk()  # Create the Tk window
    root.geometry("400x400")
    root.title("Initialization")

    db_dir = "databases"
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Function to validate that the entered name is a full name with first and last name separated by a space
    def check_full_name(name):
        pattern = r'^[a-zA-Z]+\s[a-zA-Z]+$' # Regular expression to match first and last name separated by a space
        if re.match(pattern, name):
            return True
        else:
            return False

    # Function to handle button click
    def setup_admin():
        username = username_entry.get()
        password = password_entry.get()
        if username != '' and password != '':
            if check_full_name(username):
                db.create_db()
                if not db.check_if_user_exists(username):
                    # Add user to the database with admin authorization and open voter UI
                    db.add_user(username, password, "ADMIN")
                    messagebox.showinfo('Success', 'Setup Complete.')
                    root.destroy()
                else:
                    messagebox.showerror('Error', 'Already Registered')
            else:
                messagebox.showerror('Error', 'Please enter your first and last name into the name field')
        else:
            messagebox.showerror('Error',"Please fill in all the fields")

    # Create username label and entry
    username_label = customtkinter.CTkLabel(master=root, text="Admin Name")
    username_label.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)
    username_entry = customtkinter.CTkEntry(master=root, width=200, height=30)
    username_entry.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

    # Create password label and entry
    password_label = customtkinter.CTkLabel(master=root, text="Admin Password")
    password_label.place(relx=0.5, rely=0.4, anchor=customtkinter.CENTER)
    password_entry = customtkinter.CTkEntry(master=root, width=200, height=30)
    password_entry.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    # Create submit button
    submit_button = customtkinter.CTkButton(master=root, text="Setup", command=setup_admin)
    submit_button.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER)

    root.mainloop()