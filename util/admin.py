import customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import sqlite3
import shutil
import os
from PIL import Image, ImageTk
import util.database_operations as database_operations
from tkinter import filedialog

def show_admin_ui():
    db_path = os.path.join("databases", "voting.db")

    customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
    main_font = ('Arial', 15, 'bold')
    head_font = ('Arial', 18, 'bold')

    images_path = "candidateimages"
    if not os.path.exists(images_path):
        os.makedirs(images_path)


    plot_path = "plots"
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)


    # Create the main window
    root = customtkinter.CTk()
    root.geometry('960x540')
    root.title('Voting System')
    root.resizable(True,True)

    # Create a notebook widget to hold the tabs
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    # Create the first tab for user login
    user_tab = customtkinter.CTkFrame(notebook)
    notebook.add(user_tab, text='User Management')

    # Create the entry fields for username and password
    head_label = customtkinter.CTkLabel(user_tab,font=head_font, text='User Management')
    head_label.grid(column=0, row=0, padx=10, pady=10)

    username_label = customtkinter.CTkLabel(user_tab, text='Username:',font=main_font)
    username_label.grid(column=0, row=2, padx=10, pady=10)
    username_entry = customtkinter.CTkEntry(user_tab)
    username_entry.grid(column=1, row=2, padx=10, pady=10)

    password_label = customtkinter.CTkLabel(user_tab, text='Password:',font=main_font)
    password_label.grid(column=0, row=3, padx=10, pady=10)
    password_entry = customtkinter.CTkEntry(user_tab, show='*')
    password_entry.grid(column=1, row=3, padx=10, pady=10)

    id_label = customtkinter.CTkLabel(user_tab, text='ID:',font=main_font)
    id_label.grid(column=0, row=4, padx=10, pady=10)
    id_entry = customtkinter.CTkEntry(user_tab)
    id_entry.grid(column=1, row=4, padx=10, pady=10)

    auth_label = customtkinter.CTkLabel(user_tab, text='Authorization:',font=main_font)
    auth_label.grid(column=0, row=5, padx=10, pady=10)
    auth_box = customtkinter.CTkComboBox(user_tab, values=['','ADMIN','VOTER'],state='readonly')
    auth_box.grid(column=1, row=5, padx=10, pady=10)

    def commit_user():
        username = username_entry.get()
        password = password_entry.get()
        auth = auth_box.get()
        if username == '' or password == '' or auth == '':
                messagebox.showerror('Error', 'Please fill in all fields')
        else:
            database_operations.add_user(username,password,auth)
            messagebox.showinfo("Success","User Added Successfully!")
            fill_user_tree()
            
    save_button = customtkinter.CTkButton(user_tab,width=180, text='Add User',command=commit_user)
    save_button.grid(column=0, row=6, padx=10, pady=5)

    def del_user():
        ID = id_entry.get()
        if ID == '' or ID.isnumeric == False:
            messagebox.showerror('Error',"Enter A Valid ID")
        else:
            database_operations.delete_user(ID)
            messagebox.showinfo("Success","User Deleted Successfully!")
            fill_user_tree()

    del_button = customtkinter.CTkButton(user_tab,width=180, text='Delete User',command=del_user)
    del_button.grid(column=0, row=7, padx=10, pady=5)

    #-------------------------------------------------------#

    #CANDIDATE GUI#

    # Create the second tab for candidate registration
    candidate_tab = customtkinter.CTkFrame(notebook)
    notebook.add(candidate_tab, text='Candidate Registration')


    head2_label = customtkinter.CTkLabel(candidate_tab,font=head_font, text='Candidate Registration')
    head2_label.grid(column=0, row=0, padx=10, pady=10)

    # Create the entry fields for candidate name and image path
    candidate_name_label = customtkinter.CTkLabel(candidate_tab, text='Candidate Name:',font=main_font)
    candidate_name_label.grid(column=0, row=1, padx=10, pady=10)
    candidate_name_entry = customtkinter.CTkEntry(candidate_tab)
    candidate_name_entry.grid(column=1, row=1, padx=10, pady=10)

    image_path_label = customtkinter.CTkLabel(candidate_tab, text='Image Path:',font=main_font)
    image_path_label.grid(column=0, row=2, padx=10, pady=10)

    image_path_entry = customtkinter.CTkEntry(candidate_tab)
    image_path_entry.grid(column=1, row=2, padx=10, pady=10)

    id2_label = customtkinter.CTkLabel(candidate_tab, text='ID:',font=main_font)
    id2_label.grid(column=0, row=3, padx=10, pady=10)

    id2_entry = customtkinter.CTkEntry(candidate_tab)
    id2_entry.grid(column=1, row=3, padx=10, pady=10)

    def commit_candidate():
        name = candidate_name_entry.get()
        image = image_path_entry.get()
        if name == '' or image == '':
                messagebox.showerror('Error', 'Please fill in all fields')
        else:
            new_path = os.path.join(images_path, name + "_image.png")
            shutil.copy2(image, new_path)
            database_operations.add_candidate(name,new_path)

            image_path_entry.setvar(new_path)
            display_image()

            messagebox.showinfo("Success","Candidate Added Successfully!")
            fill_candidate_tree()

    commit_button = customtkinter.CTkButton(candidate_tab, text='Add Candidate', command=commit_candidate)
    commit_button.grid(column=0, row=7, padx=10, pady=5)

    # Create a function to display the image

    def display_image():
        global label
        im1 = image_path_entry.get()
        if im1 == "":
            messagebox.showerror('Error',"Select an Image")
        else:
            try:
                image = Image.open(im1)
                photo = customtkinter.CTkImage(light_image=image,size=(247,247))
                label = customtkinter.CTkLabel(candidate_tab,text = "", image=photo)
                label.place(x=580,y=5)
            except Exception as e:
                messagebox.showerror('Error', f"Error opening image file: {e}")


    def find_image():
        image_path_entry.delete(0,999)
        filename = (filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes =[('image files', '.png')])).strip("'")
        image_path_entry.insert(0,filename)
        display_image()

    def close_image():
                label.destroy()
        
    iamge_path_button = customtkinter.CTkButton(candidate_tab, text='Select Image', command=find_image)
    iamge_path_button.grid(column=0, row=4, padx=10, pady=3)


    # Create a button to display the image
    close_button = customtkinter.CTkButton(candidate_tab, text='Close Image', command=close_image)
    close_button.grid(column=0, row=6, padx=10, pady=(3,70))

    display_button = customtkinter.CTkButton(candidate_tab, text='Display Image', command=display_image)
    display_button.grid(column=0, row=5, padx=10, pady=3)

    def del_candidate():
        ID = id2_entry.get()
        if ID == '' or ID.isnumeric == False:
            messagebox.showerror('Error',"Enter A Valid ID")
        else:
            database_operations.delete_candidate(ID)
            messagebox.showinfo("Success","User Deleted Successfully!")
            fill_candidate_tree()

    del2_button = customtkinter.CTkButton(candidate_tab, text='Delete Candidate',command=del_candidate)
    del2_button.grid(column=0, row=8, padx=10, pady=5)


    # Create a treeview widget
    usertree = ttk.Treeview(user_tab, columns=('ID', 'Username', 'Password', 'Authorization'), height=31)
    # Set the headings for each column
    usertree.heading('#1', text='ID')
    usertree.heading('#2', text='Username')
    usertree.heading('#3', text='Password')
    usertree.heading('#4', text='Authorization')

    # Set the column widths and alignment
    usertree.column('#0', width=0, stretch=tk.NO)
    usertree.column('#1', anchor=tk.CENTER, width=100)
    usertree.column('#2', anchor=tk.CENTER, width=155)
    usertree.column('#3', anchor=tk.CENTER, width=155)
    usertree.column('#4', anchor=tk.CENTER, width=155)

    #Placing treeview widget into the tab
    usertree.place(relx=0.525,rely=0.005)

    #Collecting data from database and inputing into treeview
    def fill_user_tree():
        usertree.delete(*usertree.get_children())
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("Select * FROM users") 
        rows = cursor.fetchall()
        for i, row in enumerate(rows):
                usertree.insert('', 'end', values=row)

    fill_user_tree()
    # Candidate treeview
    candidatetree = ttk.Treeview(candidate_tab, columns=('ID', 'Name', 'Image Path'), height=15)

    candidatetree.heading('#1', text='ID')
    candidatetree.heading('#2', text='Username')
    candidatetree.heading('#3', text='Image Path')

    # Set the column widths and alignment
    candidatetree.column('#0', width=0, stretch=tk.NO)
    candidatetree.column('#1', anchor=tk.CENTER, width=100)
    candidatetree.column('#2', anchor=tk.CENTER, width=230)
    candidatetree.column('#3', anchor=tk.CENTER, width=230)

    #Placing treeview widget into the tab
    candidatetree.place(relx=0.525,rely=0.49)

    def fill_candidate_tree():
        candidatetree.delete(*candidatetree.get_children())
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("Select * FROM candidates") 
        rows = cursor.fetchall()
        for i, row in enumerate(rows):
                candidatetree.insert('', 'end', values=row)

    fill_candidate_tree()

    def generate_vote_graph():
        candidate_dict = database_operations.get_votes()

        candidates = list(candidate_dict.keys())
        votes = list(candidate_dict.values())

        fig1, ax1 = plt.subplots()
        ax1.pie(votes, labels=candidates, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.savefig('plots/results.png')
        plt.show()
        messagebox.showinfo('Success', 'Plot saved at plot/results.png')
    
    gen_plot = customtkinter.CTkButton(candidate_tab, text='Generate Results',command=generate_vote_graph)
    gen_plot.grid(column=0, row=10, padx=10, pady=5)
    
    # Run the main loop
    root.mainloop()
