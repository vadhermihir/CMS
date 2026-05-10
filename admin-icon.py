import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector


# Initialize Tkinter window
root = tk.Tk()

# Set the window to full screen
root.attributes("-fullscreen", True)
root.title("Track Tour Order")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and resize background image to fit the full screen
bg_image_path = "ecom.jpg"  # Set the path to your background image
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

# Main frame with a subtle shadow effect and padding (no border)
frame = ctk.CTkFrame(root, fg_color="#ECBA7F", width=screen_width * 0.7, height=screen_height * 0.9, corner_radius=0,
                     border_width=0)
frame.place(relx=0.7, rely=0.5, anchor="center")

# Title Label
title_label = ctk.CTkLabel(frame, text="Track Tour Order", font=("Arial", 32, "bold"), text_color="black")
title_label.grid(row=0, column=0, columnspan=2, pady=(20, 30))

# Sender Details Section
sender_frame = ctk.CTkFrame(frame, width=screen_width * 0.6, corner_radius=10, fg_color="lightblue", height=300, border_width=0)
sender_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

sender_name_label = ctk.CTkLabel(sender_frame, text="Enter Consignment number:", font=("Arial", 18), text_color="black")
sender_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
sender_name_entry = ctk.CTkEntry(sender_frame, font=("Arial", 16))
sender_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")


# Receiver Details Section
receiver_frame = ctk.CTkFrame(frame, width=screen_width * 0.6, corner_radius=10, fg_color="lightgreen", height=300, border_width=0)
receiver_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

receiver_name_label = ctk.CTkLabel(receiver_frame, text="Enter Your Phone number", font=("Arial", 18), text_color="black")
receiver_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
receiver_name_entry = ctk.CTkEntry(receiver_frame, font=("Arial", 16))
receiver_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

# Submit Button
submit_button = ctk.CTkButton(frame, text="Submit Order", font=("Arial", 18), text_color="black", fg_color="#F08D18", hover_color="#D65C07")
submit_button.grid(row=5, column=0, columnspan=2, pady=30)

# Load Help Icon Image
help_icon_path = "44.png"  # Replace this with your actual help icon image file path
help_icon = Image.open(help_icon_path)
help_icon_resized = help_icon.resize((40, 40), Image.Resampling.LANCZOS)  # Resize to an appropriate size
help_icon_tk = ImageTk.PhotoImage(help_icon_resized)

# Help Icon Button
def show_help():
    messagebox.showinfo("Help", "Enter your consignment number and phone number to track your order.")

help_button = ctk.CTkButton(frame, image=help_icon_tk, text="Admin", font=("Arial", 16), text_color="black", fg_color="#58D68D", hover_color="#1F8C46", command=show_help)
help_button.grid(row=6, column=0, columnspan=2, pady=20)  # Place after submit button

# Function to handle window closing
def on_closing():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Keep a reference to the help icon to prevent garbage collection
help_button.image = help_icon_tk

root.mainloop()
