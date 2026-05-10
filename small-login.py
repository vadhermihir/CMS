import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import hashlib

# Initialize the main window with customtkinter
root = ctk.CTk()

# Set the window to full screen
root.attributes("-fullscreen", True)

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load background image
bg_image_path = "123.jpg"  # Set the path to your background image
bg_image = Image.open(bg_image_path)
bg_image_resized = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)

# Convert to PhotoImage for Tkinter compatibility
bg_image_tk = ImageTk.PhotoImage(bg_image_resized)

# Login credentials for validation (In a real-world app, this should be done with a secure database)
valid_username = "admin"
valid_password_hash = hashlib.sha256("admin".encode()).hexdigest()  # Store a hashed version of the password


# Function to show the login page
def show_login_page():
    # Clear the window (if any previous content is present)
    for widget in root.winfo_children():
        widget.destroy()

    # Set the window title
    root.title("Login Page")


    # Create a canvas to display the background image
    canvas = ctk.CTkCanvas(root, width=screen_width, height=screen_height)
    canvas.pack(fill=tk.BOTH, expand=True)  # Make the canvas fill the entire window

    # Set the background image
    canvas.create_image(0, 0, image=bg_image_tk, anchor="nw")

    # Create a frame for the login form and place it in the center
    frame = ctk.CTkFrame(root, fg_color="black", width=screen_width//3, height=300)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Add username and password labels and entry fields
    username_label = ctk.CTkLabel(frame, text="Username:", font=("Helvetica", 18), text_color="white")
    username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    username_entry = ctk.CTkEntry(frame, font=("Helvetica", 18))
    username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    password_label = ctk.CTkLabel(frame, text="Password:", font=("Helvetica", 18), text_color="white")
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    password_entry = ctk.CTkEntry(frame, font=("Helvetica", 18), show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    # Function to validate login credentials against the MySQL database

    # Add a password visibility toggle button
    def toggle_password():
        if password_entry.cget('show') == "*":
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    toggle_button = ctk.CTkButton(frame, text="👁", font=("Helvetica", 14), command=toggle_password, width=40, fg_color="black", text_color="white")  # Removed corner_radius
    toggle_button.grid(row=1, column=2, padx=10)

    # Add hover effect for the login button
    def on_enter(e):
        login_button.config(bg_color="#ff5733")

    def on_leave(e):
        login_button.config(bg_color="#333333")

    # Add a login button (without rounded corners)
    def validate_login():
        username = username_entry.get()
        password = password_entry.get()

        # Validate credentials
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if username == valid_username and password_hash == valid_password_hash:
            messagebox.showinfo("Login Success", "Welcome, Admin!")
            # After successful login, perform any next action
        else:
            messagebox.showerror("Login Error", "Invalid Username or Password")
            password_entry.delete(0, tk.END)  # Clear password field after incorrect attempt

    # Create the login button without rounded corners
    login_button = ctk.CTkButton(frame, text="Login", font=("Helvetica", 24), command=validate_login, width=200, height=40, fg_color="black", text_color="white")  # Removed corner_radius
    login_button.grid(row=3, columnspan=2, pady=20)
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

# Show the login page first
show_login_page()

# Start the Tkinter event loop
root.mainloop()
