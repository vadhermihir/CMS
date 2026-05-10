import random
import string
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from tkcalendar import Calendar
from fpdf import FPDF
import os
import datetime
import subprocess


# Initialize Tkinter window
root = tk.Tk()

# Set the window to full screen
root.attributes("-fullscreen", True)
root.title("Track Tour Order")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

def show_main_form():
    # Clear the window (removes any previous content)
    for widget in root.winfo_children():
        widget.destroy()

    # Load and resize background image to fit the full screen
    bg_image_path = "images/c8.jpg"  # Set the path to your background image
    bg_image = Image.open(bg_image_path)
    bg_image_resized = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # High-quality resizing
    bg_image_tk = ImageTk.PhotoImage(bg_image_resized)

    # Create a canvas to display the background image
    canvas = ctk.CTkCanvas(root, width=screen_width, height=screen_height)
    canvas.pack(fill="both", expand=True)

    # Draw the background image on the canvas
    canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)

    # Keep a reference to the image to prevent it from being garbage collected
    canvas.image = bg_image_tk

    welcome_label = ctk.CTkLabel(
        root,
        text="Welcome To Tracking Page",
        font=("Copperplate Gothic Bold", 36, "bold"),
        text_color="white",
        bg_color="black",
        width=screen_width,
        height=100,
    )
    welcome_label.place(relx=0.5, rely=0.1, anchor="center")  # Position it at the top of the screen

    # Main frame with a subtle shadow effect and padding (no border)
    frame = ctk.CTkFrame(root, fg_color="#FFC736", width=screen_width * 0.8, height=screen_height * 0.9,
                         corner_radius=0,border_width=0)
    frame.place(relx=0.7, rely=0.5, anchor="center")

    # Title Label
    title_label = ctk.CTkLabel(frame, text="Track Tour Order", font=("Copperplate Gothic Bold", 32, "bold"), text_color="black")
    title_label.grid(row=0, column=0, columnspan=2, pady=(20, 30))

    # Sender Details Section
    sender_frame = ctk.CTkFrame(frame, width=screen_width * 0.6, corner_radius=0, fg_color="#3B8ED0", height=300,
                                border_width=0)
    sender_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

    consignment_no_label = ctk.CTkLabel(sender_frame, text="Enter Consignment number:", font=("Copperplate Gothic Bold", 18),
                                        fg_color="#3B8ED0",text_color="white")
    consignment_no_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    consignment_no_entry = ctk.CTkEntry(sender_frame, font=("Copperplate Gothic Bold", 16), text_color="black", fg_color="white")
    consignment_no_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")


    # Submit Button
    submit_button = ctk.CTkButton(frame, text="Track Order", font=("Copperplate Gothic Bold", 18), text_color="black",
                                  fg_color="#3B8ED0", hover_color="#D65C07",command="")
    submit_button.grid(row=5, column=0, columnspan=2, pady=30)

    # Load Help Icon Image
    help_icon_path = "images/44.png"  # Replace this with your actual help icon image file path
    help_icon = Image.open(help_icon_path)
    help_icon_resized = help_icon.resize((40, 40), Image.Resampling.LANCZOS)  # Resize to an appropriate size
    help_icon_tk = ImageTk.PhotoImage(help_icon_resized)

    help_button = ctk.CTkButton(frame, image=help_icon_tk, text="Admin", font=("Copperplate Gothic Bold", 16),
                                text_color="black",
                                fg_color="#3B8ED0", hover_color="#1F8C46", command="")
    help_button.grid(row=6, column=0, columnspan=2, pady=20)  # Place after submit button

    help_button1 = ctk.CTkButton(frame, image=help_icon_tk, text="Customer Support", font=("Copperplate Gothic Bold", 16),
                                text_color="black",
                                fg_color="#3B8ED0", hover_color="#1F8C46", command="")
    help_button1.grid(row=7, column=0, columnspan=2, pady=20)  # Place after submit button

show_main_form()
root.mainloop()