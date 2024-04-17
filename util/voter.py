import tkinter as tk
from tkinter import messagebox
import customtkinter
from PIL import Image, ImageTk
import util.database_voter_operations as db

def create_voting_ui(voter_name):
    customtkinter.set_appearance_mode("light")
    main_font = ('Arial', 15, 'bold')
    head_font = ('Arial', 18, 'bold')

    # Define the available candidates and their image paths
    candidate_data = db.get_candidates()

    # Create a dictionary to store the PhotoImage objects
    photo_images = {}

    # Create the main window
    root = customtkinter.CTk()
    root.title("Voting System")
    root.geometry('960x480')
    root.resizable(True,True)

    # Create a frame for the name input
    name_frame = customtkinter.CTkFrame(root)
    name_frame.pack(pady=20)

    # Create a label and entry for the name input
    name_label = customtkinter.CTkLabel(name_frame, text="Voter Name:")
    name_label.pack(side=tk.LEFT)
    name_entry = customtkinter.CTkEntry(name_frame, textvariable=tk.StringVar(value=voter_name), state='readonly')
    name_entry.pack(side=tk.LEFT)

    # Create a frame for the voting buttons
    voting_frame = customtkinter.CTkFrame(root, width=300, height=200)
    voting_frame.pack(pady=20)

    # Create a variable to store the selected candidate
    selected_candidate = customtkinter.StringVar()

    # Create the voting buttons with candidate images
    for candidate, image_path in candidate_data.items():
        # Load the candidate image
        image = Image.open(image_path)
        image = image.resize((150, 150))
        photo_image = ImageTk.PhotoImage(image)

        # Store the PhotoImage object in the dictionary
        photo_images[candidate] = photo_image

        # Create a frame for the candidate button
        candidate_frame = customtkinter.CTkFrame(voting_frame)
        candidate_frame.pack(side=tk.LEFT, padx=10)

        # Create the candidate image label
        image_label = customtkinter.CTkLabel(candidate_frame,text = "", image=photo_image)
        image_label.pack()

        # Create the candidate name label
        name_label = customtkinter.CTkLabel(candidate_frame, text=candidate)
        name_label.pack()

        # Create the radio button
        button = tk.Radiobutton(candidate_frame, variable=selected_candidate, value=candidate)
        button.pack()

    # Create a function to handle the voting
    def vote():
        name = name_entry.get()
        candidate = selected_candidate.get()
        has_voted = db.check_if_voted(name)

        if has_voted == None:
            messagebox.showerror('Error', 'User not found in DB')
        elif has_voted[0] == True:
            messagebox.showerror('Error', 'Vote already submitted')
        else:
            candidateID = db.get_candidate_id(candidate)
            db.add_vote(has_voted[1], candidateID)
            messagebox.showinfo('Submitted', 'Vote successfully submitted!')

    # Create a button to submit the vote
    submit_button = customtkinter.CTkButton(root, text="Submit Vote", command=vote)
    submit_button.pack(pady=20)

    # Start the main event loop
    root.mainloop()