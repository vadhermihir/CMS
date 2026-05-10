import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import fontTools as font

# Initialize Tkinter window
root = tk.Tk()

# Set the window to full screen
root.attributes("-fullscreen", True)

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Text for the welcome page
welcome_text = "Welcome To Swings"
developed_by_text = "Developed By Harshil Maheta"  # Change this to your name or developer name

# Create the gif_label here to ensure it's in the global scope
gif_label = None

# Function to show the welcome page with animated text
def show_welcome_page():
    # Clear the window (if any previous content is present)
    for widget in root.winfo_children():
        widget.destroy()

    # Create a label for displaying the animated text
    label = tk.Label(root, text="", font=("Copperplate Gothic Bold", 72), fg="Red", bg="black")
    label.pack(fill=tk.BOTH, expand=True)

    # Function to animate the text letter by letter (typing effect)
    def type_text(index=0):
        if index < len(welcome_text):
            label.configure(text=welcome_text[:index+1])  # Update text with next letter
            root.after(100, type_text, index+1)  # Delay between each letter

        # Once the text animation is complete, call the function to show the GIF
        if index == len(welcome_text) - 1:
            root.after(1000, remove_text_and_show_gif)  # Wait 1 second before transitioning to GIF

    # Start animating the text
    type_text()

# Function to remove the text and display the GIF
def remove_text_and_show_gif():
    # Clear the window (removes the welcome text)
    for widget in root.winfo_children():
        widget.destroy()

    # Load the GIF
    file = '111.gif'  # Change this path to your actual GIF file path
    info = Image.open(file)
    frames = info.n_frames
    print(f"Total frames: {frames}")

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

        # Schedule the next frame update
        anim = root.after(25, lambda: animation(count))

    # Start the animation immediately when the window is loaded
    animation(count)

    # After the GIF animation, show the "Developed By" text with animation
    root.after(frames * 50 + 1000, show_developed_by_text)  # Wait for the GIF to finish, then show text

# Function to show "Developed By" text with typing effect
def show_developed_by_text():
    # Clear the window (if any previous content is present)
    for widget in root.winfo_children():
        widget.destroy()

    # Create a label for displaying the "Developed By" text
    label = tk.Label(root, text="", font=("Copperplate Gothic Bold", 48), fg="white", bg="black")
    label.pack(fill=tk.BOTH, expand=True)

    # Function to animate the text letter by letter (typing effect)
    def type_text(index=0):
        if index < len(developed_by_text):
            label.configure(text=developed_by_text[:index+1])  # Update text with next letter
            root.after(150, type_text, index+1)  # Delay between each letter

    # Start animating the text
    type_text()

show_welcome_page()

# Start the Tkinter event loop
root.mainloop()
