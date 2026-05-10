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

# Initialize Tkinter window
root = tk.Tk()

# Set the window to full screen
root.attributes("-fullscreen", True)
root.title("Track Tour Order")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Text for the welcome page
welcome_text = "Welcome To Swings"
developed_by_text = "Developed By Harshil Maheta"  # Change this to your name or developer name

# Create the gif_label here to ensure it's in the global scope
gif_label = None


def show_gif():
    # Clear the window (removes the welcome text)
    for widget in root.winfo_children():
        widget.destroy()

    # Load the GIF
    file = 'images/111.gif'  # Change this path to your actual GIF file path
    try:
        info = Image.open(file)
        frames = info.n_frames
        print(f"Total frames: {frames}")
    except FileNotFoundError:
        messagebox.showerror("Error", "GIF file not found!")
        return
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return

    # Load and resize each frame to fit the full screen
    im_resized = []
    for i in range(frames):
        info.seek(i)
        frame = info.copy()

        # Resize the frame to exactly match the screen size
        frame_resized = frame.resize((screen_width, screen_height))

        # Convert the resized frame to a Tkinter PhotoImage object
        im_resized.append(ImageTk.PhotoImage(frame_resized))

    # Initialize variables for animation
    anim = None
    count = 0

    # Create a label to display the GIF (only once, persist the label)
    global gif_label
    gif_label = tk.Label(root)
    gif_label.pack(fill=tk.BOTH, expand=True)

    # Function to display the animation
    def animation(count):
        global anim
        if gif_label is not None:  # Ensure gif_label exists before updating
            im2 = im_resized[count]
            gif_label.configure(image=im2)

        # Increment the count and loop back to 0 after the last frame
        count += 1
        if count == frames:
            count = 0

        # Schedule the next frame update with a delay for "line by line" effect
        anim = root.after(100, lambda: animation(count))  # Adjust 100 to control the delay (milliseconds)

    # Start the animation immediately when the window is loaded
    animation(count)

    # After the GIF animation, show the "Developed By" text with animation
    root.after(frames * 100 + 1000, show_gif1())  # Wait for the GIF to finish, then show text


def show_gif1():
    # Clear the window (removes the welcome text)
    for widget in root.winfo_children():
        widget.destroy()

    # Load the GIF
    file = 'images/shop.gif'  # Change this path to your actual GIF file path
    try:
        info = Image.open(file)
        frames = info.n_frames
        print(f"Total frames: {frames}")
    except FileNotFoundError:
        messagebox.showerror("Error", "GIF file not found!")
        return
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return

    # Load and resize each frame to fit the full screen
    im_resized = []
    for i in range(frames):
        info.seek(i)
        frame = info.copy()

        # Resize the frame to exactly match the screen size
        frame_resized = frame.resize((screen_width, screen_height))

        # Convert the resized frame to a Tkinter PhotoImage object
        im_resized.append(ImageTk.PhotoImage(frame_resized))

    # Initialize variables for animation
    anim = None
    count = 0

    # Create a label to display the GIF (only once, persist the label)
    global gif_label
    gif_label = tk.Label(root)
    gif_label.pack(fill=tk.BOTH, expand=True)

    # Function to display the animation
    def animation(count):
        global anim
        if gif_label is not None:  # Ensure gif_label exists before updating
            im2 = im_resized[count]
            gif_label.configure(image=im2)

        # Increment the count and loop back to 0 after the last frame
        count += 1
        if count == frames:
            count = 0

        # Schedule the next frame update with a delay for "line by line" effect
        anim = root.after(100, lambda: animation(count))  # Adjust 100 to control the delay (milliseconds)

    # Start the animation immediately when the window is loaded
    animation(count)

    # After the GIF animation, show the "Developed By" text with animation
    root.after(frames * 100 + 1000)


show_gif()

root.mainloop()
