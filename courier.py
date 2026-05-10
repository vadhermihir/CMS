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

# Text for the welcome page
welcome_text = "Welcome To Swings"
developed_by_text = "Developed By Mihir Vadher"  # Change this to your name or developer name

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
            label.configure(text=welcome_text[:index + 1])  # Update text with next letter
            root.after(100, type_text, index + 1)  # Delay between each letter

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
            label.configure(text=developed_by_text[:index + 1])  # Update text with next letter
            root.after(150, type_text, index + 1)  # Delay between each letter

    # Start animating the text
    type_text()

    # After the text finishes, display the main form
    root.after(len(developed_by_text) * 150 + 1000, show_main_form)


# Function to display the main form for tracking tour orders
def show_main_form():
    # Clear the window (removes any previous content)
    for widget in root.winfo_children():
        widget.destroy()

    # Load and resize background image to fit the full screen
    bg_image_path = "c13.jpg"  # Set the path to your background image
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
    frame = ctk.CTkFrame(root, fg_color="#FFC736", width=screen_width * 0.7, height=screen_height * 0.9,
                         corner_radius=0,
                         border_width=0)
    frame.place(relx=0.7, rely=0.5, anchor="center")

    # Title Label
    title_label = ctk.CTkLabel(frame, text="Track Tour Order", font=("Copperplate Gothic Bold", 32, "bold"), text_color="black")
    title_label.grid(row=0, column=0, columnspan=2, pady=(20, 30))

    # Sender Details Section
    sender_frame = ctk.CTkFrame(frame, width=screen_width * 0.6, corner_radius=10, fg_color="#3B8ED0", height=300,
                                border_width=0)
    sender_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

    consignment_no_label = ctk.CTkLabel(sender_frame, text="Enter Consignment number:", font=("Copperplate Gothic Bold", 18),
                                        fg_color="#3B8ED0",text_color="white")
    consignment_no_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    consignment_no_entry = ctk.CTkEntry(sender_frame, font=("Copperplate Gothic Bold", 16))
    consignment_no_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")


    # Submit Button
    submit_button = ctk.CTkButton(frame, text="Track Order", font=("Copperplate Gothic Bold", 18), text_color="black",
                                  fg_color="#3B8ED0", hover_color="#D65C07")
    submit_button.grid(row=5, column=0, columnspan=2, pady=30)

    # Load Help Icon Image
    help_icon_path = "44.png"  # Replace this with your actual help icon image file path
    help_icon = Image.open(help_icon_path)
    help_icon_resized = help_icon.resize((40, 40), Image.Resampling.LANCZOS)  # Resize to an appropriate size
    help_icon_tk = ImageTk.PhotoImage(help_icon_resized)

    help_button = ctk.CTkButton(frame, image=help_icon_tk, text="Admin", font=("Copperplate Gothic Bold", 16), text_color="black",
                                fg_color="#3B8ED0", hover_color="#1F8C46", command=lambda: show_login_page())
    help_button.grid(row=6, column=0, columnspan=2, pady=20)  # Place after submit button


# Function to display the login page for the admin
def show_login_page():
    # Clear the window (removes any previous content)
    for widget in root.winfo_children():
        widget.destroy()

    # Load and resize background image to fit the full screen
    bg_image_path = "c6.jpg"  # Set the path to your background image
    bg_image = Image.open(bg_image_path)
    bg_image_resized = bg_image.resize((screen_width, screen_height),
                                       Image.Resampling.LANCZOS)  # High-quality resizing
    bg_image_tk = ImageTk.PhotoImage(bg_image_resized)

    # Create a canvas to display the background image
    canvas = ctk.CTkCanvas(root, width=screen_width, height=screen_height)
    canvas.pack(fill="both", expand=True)

    # Draw the background image on the canvas
    canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)

    # Keep a reference to the image to prevent it from being garbage collected
    canvas.image = bg_image_tk

    # Add a "Welcome Admin" label at the top
    welcome_label = ctk.CTkLabel(
        root,
        text="Welcome To Login Page",
        font=("Copperplate Gothic Bold", 36, "bold"),
        text_color="white",
        bg_color="black",
        width=screen_width,
        height=100,
    )
    welcome_label.place(relx=0.5, rely=0.1, anchor="center")  # Position it at the top of the screen


    # Create a frame for the login form and place it in the center
    frame = ctk.CTkFrame(root, fg_color="#FFC736", width=screen_width, height=300)
    frame.place(relx=0.7, rely=0.4, anchor="center")

    def back_to_main():
        show_main_form()  # Go back to the login page when clicked

    back_button1 = ctk.CTkButton(
        root,
        text="Back to Home",
        font=("Copperplate Gothic Bold", 16),
        width=200,
        height=50,
        fg_color="#3B8ED0",  # Customize as you prefer
        hover_color="#D65C07",
        command=back_to_main)
    back_button1.place(relx=0.1, rely=0.9, anchor="center")  # Position at the bottom-left corner

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
                user='root',  # Replace with your MySQL username
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
    login_button = ctk.CTkButton(frame, text="Login", font=("Copperplate Gothic Bold", 20), text_color="black",
                                 command=validate_login)
    login_button.grid(row=2, columnspan=2, pady=20)





# Function to display the home page after successful login
def show_home_page():
    # Clear the window (removes any previous content)
    for widget in root.winfo_children():
        widget.destroy()

    # Load and resize background image to fit the full screen
    bg_image_path = "c4.jpg"  # Set the path to your background image
    bg_image = Image.open(bg_image_path)
    bg_image_resized = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # High-quality resizing
    bg_image_tk = ImageTk.PhotoImage(bg_image_resized)

    # Create a canvas to display the background image
    canvas = ctk.CTkCanvas(root, width=screen_width, height=screen_height)
    canvas.place(x=0, y=0)  # Use place() for more precise control

    # Draw the background image on the canvas
    canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)

    # Keep a reference to the image to prevent it from being garbage collected
    canvas.image = bg_image_tk

    # Add a welcome label
    welcome_label = ctk.CTkLabel(
        root,
        text="Welcome to the Courier Management System!",
        font=("Copperplate Gothic Bold", 36, "bold"),
        text_color="white",
        bg_color="black",
        width=screen_width,
        height=100,
    )
    welcome_label.place(relx=0.5, rely=0.1, anchor="center")

    # Placeholder functions for the buttons
    def track_shipment():
        print("Tracking Shipment...")

    def schedule_pickup():
        print("Scheduling Pickup...")

    def manage_deliveries():
        print("Manage Deleveries")

    def customer_support():
        print("Accessing Customer Support...")

    def back_to_login():
        show_login_page()  # Go back to the login page when clicked

    back_button = ctk.CTkButton(
        root,
        text="Logout",
        font=("Copperplate Gothic Bold", 16),
        width=200,
        height=50,
        fg_color="#3B8ED0",  # Customize as you prefer
        hover_color="#D65C07",
        command=back_to_login
    )
    back_button.place(relx=0.1, rely=0.9, anchor="center")  # Position at the bottom-left corner

    # Load icons for each option
    track_icon = Image.open("b2.png")  # Replace with your icon file path
    track_icon = track_icon.resize((40, 40), Image.Resampling.LANCZOS)
    track_icon_tk = ImageTk.PhotoImage(track_icon)

    pickup_icon = Image.open("b5.png")  # Replace with your icon file path
    pickup_icon = pickup_icon.resize((40, 40), Image.Resampling.LANCZOS)
    pickup_icon_tk = ImageTk.PhotoImage(pickup_icon)

    deliveries_icon = Image.open("b3.png")  # Replace with your icon file path
    deliveries_icon = deliveries_icon.resize((40, 40), Image.Resampling.LANCZOS)
    deliveries_icon_tk = ImageTk.PhotoImage(deliveries_icon)

    support_icon = Image.open("b4.png")  # Replace with your icon file path
    support_icon = support_icon.resize((40, 40), Image.Resampling.LANCZOS)
    support_icon_tk = ImageTk.PhotoImage(support_icon)

    about_us_icon = Image.open("b7.png")  # Replace with your icon file path
    about_us_icon = about_us_icon.resize((40, 40), Image.Resampling.LANCZOS)
    about_us_icon_tk = ImageTk.PhotoImage(about_us_icon)

    # Add 4 buttons for courier management options with icons
    button_width = 350  # Button width
    button_height = 70  # Button height

    # Track Shipment button
    track_button = ctk.CTkButton(
        root,
        text="Track Shipment",
        font=("Copperplate Gothic Bold", 16),
        width=button_width,
        height=button_height,
        image=track_icon_tk,
        compound="left",  # Places the icon to the left of the text
        command=track_shipment
    )
    track_button.place(relx=0.7, rely=0.3, anchor="center")

    # Schedule Pickup button
    pickup_button = ctk.CTkButton(
        root,
        text="Schedule Pickup",
        font=("Copperplate Gothic Bold", 16),
        width=button_width,
        height=button_height,
        image=pickup_icon_tk,
        compound="left",  # Places the icon to the left of the text
        command=schedule_pickup
    )
    pickup_button.place(relx=0.7, rely=0.4, anchor="center")

    # Manage Deliveries button
    deliveries_button = ctk.CTkButton(
        root,
        text="Manage Deliveries",
        font=("Copperplate Gothic Bold", 16),
        width=button_width,
        height=button_height,
        image=deliveries_icon_tk,
        compound="left",  # Places the icon to the left of the text
        command=manage_deliveries
    )
    deliveries_button.place(relx=0.7, rely=0.5, anchor="center")

    # Customer Support button
    support_button = ctk.CTkButton(
        root,
        text="Customer Support",
        font=("Copperplate Gothic Bold", 16),
        width=button_width,
        height=button_height,
        image=support_icon_tk,
        compound="left",  # Places the icon to the left of the text
        command=customer_support
    )
    support_button.place(relx=0.7, rely=0.6, anchor="center")

    about_button = ctk.CTkButton(
        root,
        text="About Us",
        font=("Copperplate Gothic Bold", 16),
        width=button_width,
        height=button_height,
        image=about_us_icon_tk,
        compound="left",
    )
    about_button.place(relx=0.7, rely=0.7, anchor="center")


# Start the welcome page
show_welcome_page()

# Start the Tkinter event loop
root.mainloop()
