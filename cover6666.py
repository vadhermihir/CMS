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
bg_image_path = "ecom.jpg"  # Set the path to your background image
bg_image = Image.open(bg_image_path)
bg_image_resized = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # High-quality resizing
bg_image_tk = ImageTk.PhotoImage(bg_image_resized)

# Text for the welcome page
welcome_text = "Welcome To Swings"
developed_by_text = "Developed By Harshil Maheta"  # Change this to your name or developer name

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
    label = tk.Label(root, text="", font=("Copperplate Gothic Bold"
                                          "", 48), fg="black", bg="white")
    label.pack(fill=tk.BOTH, expand=True)

    # Function to animate the text letter by letter (typing effect)
    def type_text(index=0):
        if index < len(developed_by_text):
            label.configure(text=developed_by_text[:index+1])  # Update text with next letter
            root.after(150, type_text, index+1)  # Delay between each letter

    # Start animating the text
    type_text()

    # After the "Developed By" text, show the login page
    root.after(len(developed_by_text) * 150 + 1000, show_login_page)  # Wait for the text to finish, then show the login page

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
    frame = ctk.CTkFrame(root, fg_color="#EF8A18", width=screen_width, height=300)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Add username and password labels and entry fields
    username_label = ctk.CTkLabel(frame, text="Username:", font=("Copperplate Gothic Bold", 18), text_color="black")
    username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    username_entry = ctk.CTkEntry(frame, font=("Helvetica", 18))
    username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    password_label = ctk.CTkLabel(frame, text="Password:", font=("Copperplate Gothic Bold", 18), text_color="black")
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    password_entry = ctk.CTkEntry(frame, font=("Helvetica", 18), show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")


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

    # Add a login button
    login_button = ctk.CTkButton(frame, text="Login", font=("Copperplate Gothic Bold", 20), text_color="black", command=validate_login)
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
    )
    logout_button.place(relx=0.10, rely=0.5, anchor="center")  # Center the button in the middle of the screen

# Function to logout and return to login page
def logout():
    show_login_page()  # Show the login page again

# Show the welcome page first
show_welcome_page()

# Start the Tkinter event loop
root.mainloop()
