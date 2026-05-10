import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import mysql.connector  # Import MySQL connector
from PIL import Image, ImageTk

# Initialize Tkinter window
root = tk.Tk()

# Set the window to full screen
root.attributes("-fullscreen", True)

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and resize background image to fit the full screen
bg_image_path = "123.jpg"  # Set the path to your background image
bg_image = Image.open(bg_image_path)
bg_image_resized = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # High-quality resizing
bg_image_tk = ImageTk.PhotoImage(bg_image_resized)

# Function to create and show the login page
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

    # Add a "Welcome Admin" label at the top
    welcome_label = ctk.CTkLabel(
        root,
        text="Welcome To Admin Panel",
        font=("Copperplate Gothic Bold", 36, "bold"),
        text_color="white",
        bg_color="black",
        width=screen_width,
        height=100,
    )
    welcome_label.place(relx=0.5, rely=0.1, anchor="center")  # Position it at the top of the screen

    # Create a frame for the login form and place it in the center
    frame = ctk.CTkFrame(root, fg_color="#2C3E50", width=screen_width * 0.6, height=400, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Add username and password labels and entry fields
    username_label = ctk.CTkLabel(frame, text="Username:", font=("Helvetica", 18), text_color="white")
    username_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
    username_entry = ctk.CTkEntry(frame, font=("Helvetica", 18), placeholder_text="Enter Username", height=40)
    username_entry.grid(row=0, column=1, padx=20, pady=20, sticky="w")

    password_label = ctk.CTkLabel(frame, text="Password:", font=("Helvetica", 18), text_color="white")
    password_label.grid(row=1, column=0, padx=20, pady=20, sticky="w")
    password_entry = ctk.CTkEntry(frame, font=("Helvetica", 18), show="*", placeholder_text="Enter Password", height=40)
    password_entry.grid(row=1, column=1, padx=20, pady=20, sticky="w")

    # Function to validate login credentials against the MySQL database
    def validate_login():
        username = username_entry.get()
        password = password_entry.get()

        # Connect to MySQL database (make sure to replace these with your credentials)
        try:
            conn = mysql.connector.connect(
                host='localhost',  # Replace with your MySQL server host
                user='root',       # Replace with your MySQL username
                password='',  # Replace with your MySQL password
                database='cms'  # Replace with your database name
            )

            cursor = conn.cursor()

            # Query to check if the username and password match
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo("Login Success", f"Welcome, {username}!")
                show_home_page()  # Redirect to home page after successful login
            else:
                messagebox.showerror("Login Error", "Invalid Username or Password")

            # Close the connection
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Connection Error", f"Error connecting to MySQL: {err}")

    # Add a login button with improved design
    login_button = ctk.CTkButton(
        frame,
        text="Login",
        font=("Helvetica", 20, "bold"),
        text_color="white",
        fg_color="#E67E22",  # Orange color
        hover_color="#D35400",  # Darker orange on hover
        command=validate_login,
        height=40,
        width=200,
        corner_radius=10
    )
    login_button.grid(row=2, columnspan=2, pady=20)

# Function to display the home page after successful login
def show_home_page():
    # Clear the window (removes the login page)
    for widget in root.winfo_children():
        widget.destroy()

    # Set the home page title
    root.title("Home Page")

    # Create a canvas for the background (same as login page)
    canvas = ctk.CTkCanvas(root, width=screen_width, height=screen_height)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Set the background image for the home page (you can use a different image or same image as login)
    canvas.create_image(0, 0, image=bg_image_tk, anchor="nw")

    # Add a welcome label
    welcome_label = ctk.CTkLabel(
        root,
        text="Welcome to the Home Page!",
        font=("Copperplate Gothic Bold", 36, "bold"),
        text_color="white",
        bg_color="black",
        width=screen_width,
        height=100,
    )
    welcome_label.place(relx=0.5, rely=0.1, anchor="center")

    # Add a logout button to log out and go back to login page
    logout_button = ctk.CTkButton(
        root,
        text="Logout",
        font=("Helvetica", 24),
        command=logout,
        height=50,
        width=200,
        corner_radius=15
    )
    logout_button.place(relx=0.10, rely=0.5, anchor="center")  # Center the button in the middle of the screen

# Function to logout and return to login page
def logout():
    show_login_page()  # Show the login page again

# Show the login page first
show_login_page()

# Start the Tkinter event loop
root.mainloop()
