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

# Path to your scripts
PROJECT_PATH = r"D:\project\2Courier Management System Project In Python Source Code"

def open_page(script_name):
    script_path = os.path.join(PROJECT_PATH, script_name)
    subprocess.Popen(["python", script_path], shell=True)

# MySQL database connection setup
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cms"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

def generate_random_consignment_no():
    consignment_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return consignment_no


# Initialize Tkinter window
root = tk.Tk()

# Set the window to full screen
root.attributes("-fullscreen", True)
root.title("Track Tour Order")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Text for the welcome page
welcome_text = "Welcome To Hk Enterprise"
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
    file = file = r"D:\project\2Courier Management System Project In Python Source Code\images\111.gif"   # Change this path to your actual GIF file path
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

def serch_consign(consignment_no):
    conn = connect_to_db()
    if conn is None:
        return

    cursor = conn.cursor()

    # Fetch order details from the database using consignment number
    cursor.execute("SELECT * FROM courier_orders WHERE consignment_no = %s", (consignment_no,))
    order = cursor.fetchone()

    if not order:
        messagebox.showerror("Error", "No order found for the given consignment number!")
        return

    root = tk.Toplevel()  # Open a new invoice window
    root.title("Tax Invoice")
    root.attributes("-fullscreen", True)
    root.state("zoomed")

    canvas = tk.Canvas(root, width=794, height=900, bg="white")
    canvas.pack()

    # Draw Invoice Details
    canvas.create_rectangle(10, 10, 784, 1113, outline="black", width=2)
    canvas.create_text(397, 30, text="TAX INVOICE", font=("Arial", 12, "bold"), anchor="center")
    canvas.create_text(397, 60, text="HK Enterprises", font=("Arial", 18, "bold"), fill="green",
                       anchor="center")
    canvas.create_text(397, 85, text="M.G.Road, Opp.Garden, Jetpur 360370", font=("Arial", 10), anchor="center")

    # Business Details
    canvas.create_text(50, 90, text="Phone: +91 8733010200", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(50, 110, text=f"Shipment type: {order[11]}", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(397, 110, text="GSTIN: 24AALCR2857A1ZD", font=("Arial", 9, "bold"), anchor="center")
    canvas.create_text(730, 90, text=f"Date: {order[12]}", font=("Arial", 9, "bold"), anchor="e")
    canvas.create_text(744, 110, text=f"Consignment No: {order[10]}", font=("Arial", 9, "bold"), anchor="e")

    # Sender and Receiver Details
    canvas.create_rectangle(20, 130, 774, 200, outline="black", width=2)
    canvas.create_text(50, 145, text=f"Sender Name: {order[1]}", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(50, 165, text=f"Sender Address: {order[2]}", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(50, 185, text=f"Sender Number: {order[3]}", font=("Arial", 9, "bold"), anchor="w")

    canvas.create_text(500, 145, text=f"Receiver Name: {order[4]}", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(500, 165, text=f"Receiver Address: {order[5]}", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(500, 185, text=f"Receiver Number: {order[6]}", font=("Arial", 9, "bold"), anchor="w")

    # Table Header Section
    canvas.create_rectangle(20, 220, 774, 250, fill="green", outline="black", width=2)
    headers = ["    No.", "                   Package Type", "                 Weight",
               "                     Amount"]
    x_positions = [20, 80, 350, 550]  # Adjusted for proper spacing

    for i, header in enumerate(headers):
        canvas.create_text(x_positions[i], 235, text=header, font=("Arial", 10, "bold"), fill="white",
                           anchor="w")

    # Table Rows with Proper Borders
    row_start = 250
    row_height = 30
    for i in range(8):  # 5 Rows for better visibility
        y = row_start + (i * row_height)
        canvas.create_rectangle(20, y, 774, y + row_height, outline="black", width=2)

    # Column Dividers (Ensuring Proper Alignment)
    for x in x_positions:
        canvas.create_line(x, 250, x, 490, fill="black", width=1)  # adjust line

    # Populate First Row (Example Data from DB)
    canvas.create_text(40, 265, text="1", font=("Arial", 9), anchor="w")
    canvas.create_text(170, 265, text=f"{order[7]}", font=("Arial", 9), anchor="w")
    canvas.create_text(420, 265, text=f"{order[9]}", font=("Arial", 9), anchor="w")
    canvas.create_text(650, 265, text=f"₹{order[13]}", font=("Arial", 9), anchor="w")

    # Footer (Amount Details)
    canvas.create_rectangle(20, 500, 774, 580, outline="black", width=2)
    # Calculate Amounts
    total_amount = float(order[13])  # Convert string to float
    gst = 50  # Fixed GST
    subtotal = total_amount - gst

    # Pricing Details
    canvas.create_text(600, 515, text="Subtotal:" f"₹{order[13]}", font=("Arial", 10, "bold"), anchor="w")
    gst_amount = round(float(order[13]) * 0.18, 2)  # Calculate 18% GST
    total_price = round(float(order[13]) + gst_amount, 2)

    canvas.create_text(600, 535, text="GST (18%):"f"₹{gst_amount}", font=("Arial", 10, "bold"), anchor="w")
    canvas.create_text(600, 555, text="Grand Total:"f"₹{total_price}", font=("Arial", 10, "bold"), anchor="w")

    # Terms & Conditions Section
    canvas.create_rectangle(20, 670, 774, 760, outline="black", width=2)
    canvas.create_text(50, 685, text="Notes", font=("Arial", 10, "bold"), anchor="w")
    canvas.create_text(50, 705, text="1. No return deal", font=("Arial", 10), anchor="w")

    canvas.create_text(397, 685, text="Terms & Conditions", font=("Arial", 10, "bold"), anchor="center")
    terms = ["1. Customer will pay the GST", "2. Customer will pay the Delivery charges",
             "3. Pay due amount within 15 days"]
    for i, term in enumerate(terms):
        canvas.create_text(397, 705 + (i * 20), text=term, font=("Arial", 10), anchor="center")

    # Authorized Signatory
    canvas.create_text(750, 720, text="Authorized Signatory", font=("Arial", 10, "bold"), anchor="e")
    canvas.create_text(730, 740, text="HK Enterprises", font=("Arial", 10), anchor="e")

    root.mainloop()
    root.quit()


# Function to display the main form for tracking tour orders
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
    submit_button = ctk.CTkButton(frame, text="Track Order", font=("Copperplate Gothic Bold", 18), text_color="white",
                                  fg_color="#3B8ED0", hover_color="#D65C07",command=lambda: serch_consign(consignment_no_entry.get()))
    submit_button.grid(row=5, column=0, columnspan=2, pady=30)

    # Load Help Icon Image
    help_icon_path = "images/44.png"  # Replace this with your actual help icon image file path
    help_icon = Image.open(help_icon_path)
    help_icon_resized = help_icon.resize((40, 40), Image.Resampling.LANCZOS)  # Resize to an appropriate size
    help_icon_tk = ImageTk.PhotoImage(help_icon_resized)

    help_button = ctk.CTkButton(frame, image=help_icon_tk, text="Admin", font=("Copperplate Gothic Bold", 16),
                                text_color="black",
                                fg_color="#3B8ED0", hover_color="#1F8C46", command=lambda: show_login_page())
    help_button.grid(row=6, column=0, columnspan=2, pady=20)  # Place after submit button






# Function to display the login page for the admin
def show_login_page():
    # Clear the window (removes any previous content)
    for widget in root.winfo_children():
        widget.destroy()

    # Load and resize background image to fit the full screen
    bg_image_path = "images/c6.jpg"  # Set the path to your background image
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
    username_entry = ctk.CTkEntry(frame, font=("Helvetica", 18,),text_color="black", fg_color="white")
    username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    password_label = ctk.CTkLabel(frame, text="Password:", font=("Copperplate Gothic Bold", 18), text_color="black")
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    password_entry = ctk.CTkEntry(frame, font=("Helvetica", 18),text_color="black", fg_color="white", show="*")
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
            cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
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
    bg_image_path = "images/c4.jpg"  # Set the path to your background image
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

    def back_to_login():
        show_login_page()  # Go back to the login page when clicked

    # Placeholder functions for the buttons
    def track_shipment():
        # Load and resize background image to fit the full screen
        bg_image_path = "images/c8.jpg"  # Set the path to your background image
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
        title_label = ctk.CTkLabel(frame, text="Track Tour Order", font=("Copperplate Gothic Bold", 32, "bold"),
                                   text_color="black")
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 30))

        # Sender Details Section
        sender_frame = ctk.CTkFrame(frame, width=screen_width * 0.6, corner_radius=10, fg_color="#3B8ED0", height=300,
                                    border_width=0)
        sender_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

        consignment_no_label = ctk.CTkLabel(sender_frame, text="Enter Consignment number:",
                                            font=("Copperplate Gothic Bold", 18),
                                            fg_color="#3B8ED0", text_color="white")
        consignment_no_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        consignment_no_entry = ctk.CTkEntry(sender_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                            fg_color="white")
        consignment_no_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Submit Button
        submit_button = ctk.CTkButton(frame, text="Track Order", font=("Copperplate Gothic Bold", 18),
                                      text_color="black",
                                      fg_color="#3B8ED0", hover_color="#D65C07",
                                      command=lambda: serch_consign(consignment_no_entry.get()))
        submit_button.grid(row=5, column=0, columnspan=2, pady=30)

        def back_to_home_page():
            show_home_page()  # Go back to the login page when clicked

        back_icon = Image.open("images/undo.png")  # Replace with your icon file path
        back_icon = back_icon.resize((40, 40), Image.Resampling.LANCZOS)
        back_icon_tk = ImageTk.PhotoImage(back_icon)

        back_button2 = ctk.CTkButton(
            root,
            text="Back To Home",
            font=("Copperplate Gothic Bold", 16),
            width=200,
            height=50,
            image=back_icon_tk,
            fg_color="#3B8ED0",  # Customize as you prefer
            hover_color="#D65C07",
            command=back_to_home_page
        )
        back_button2.place(relx=0.1, rely=0.9, anchor="center")

        print("Tracking Shipment...")


    def manage_deliveries():
        bg_image_path = "images/c4.jpg"
        bg_image = Image.open(bg_image_path)
        bg_image_resized = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        bg_image_tk = ImageTk.PhotoImage(bg_image_resized)

        canvas = ctk.CTkCanvas(root, width=screen_width, height=screen_height)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)
        canvas.image = bg_image_tk

        frame = ctk.CTkFrame(root, fg_color="#FFC736", width=screen_width * 0.7, height=screen_height * 0.9,
                             corner_radius=0, border_width=0)
        frame.place(relx=0.7, rely=0.5, anchor="center")

        title_label = ctk.CTkLabel(frame, text="", font=("Copperplate Gothic Bold", 32, "bold"), text_color="black")
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 30))

        # Adjust the font size based on the screen height (you can also use width if preferred)
        font_size = int(screen_height * 0.05)  # Font size is 5% of the screen height

        # Set up the title label with dynamic font size
        welcome_label = ctk.CTkLabel(
            root,
            text="Courier Delivery Page!",
            font=("Copperplate Gothic Bold", font_size, "bold"),
            text_color="white",
            bg_color="black",
            width=screen_width,
            height=50,
        )
        welcome_label.place(relx=0.5, rely=0.1, anchor="center")
        # Sender Details Section
        sender_frame = ctk.CTkFrame(frame, width=screen_width * 0.6, corner_radius=10, fg_color="lightblue", height=300,
                                    border_width=0)
        sender_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

        sender_info_heading = ctk.CTkLabel(sender_frame, text="Sender Information",
                                           font=("Copperplate Gothic Bold", 20, "bold"), text_color="black")
        sender_info_heading.grid(row=0, column=2, columnspan=1, pady=(5, 10))

        sender_name_label = ctk.CTkLabel(sender_frame, text="Sender Name:", font=("Copperplate Gothic Bold", 18),
                                         text_color="black")
        sender_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        sender_name_entry = ctk.CTkEntry(sender_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                         fg_color="white")
        sender_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        sender_address_label = ctk.CTkLabel(sender_frame, text="Sender Address:", font=("Copperplate Gothic Bold", 18),
                                            text_color="black")
        sender_address_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        sender_address_entry = ctk.CTkEntry(sender_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                            fg_color="white")
        sender_address_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        sender_contact_label = ctk.CTkLabel(sender_frame, text="Sender Contact:", font=("Copperplate Gothic Bold", 18),
                                            text_color="black")
        sender_contact_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        sender_contact_entry = ctk.CTkEntry(sender_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                            fg_color="white")
        sender_contact_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Receiver Details Section
        receiver_frame = ctk.CTkFrame(frame, width=screen_width * 0.6, corner_radius=10, fg_color="light green",
                                      height=300, border_width=0)
        receiver_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

        receiver_info_heading = ctk.CTkLabel(receiver_frame, text="Receiver Information",
                                             font=("Copperplate Gothic Bold", 20, "bold"), text_color="black")
        receiver_info_heading.grid(row=0, column=2, columnspan=2, pady=(5, 15))

        receiver_name_label = ctk.CTkLabel(receiver_frame, text="Receiver Name:", font=("Copperplate Gothic Bold", 18),
                                           text_color="black")
        receiver_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        receiver_name_entry = ctk.CTkEntry(receiver_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                           fg_color="white")
        receiver_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        receiver_address_label = ctk.CTkLabel(receiver_frame, text="Receiver Address:",
                                              font=("Copperplate Gothic Bold", 18), text_color="black")
        receiver_address_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        receiver_address_entry = ctk.CTkEntry(receiver_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                              fg_color="white")
        receiver_address_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        receiver_contact_label = ctk.CTkLabel(receiver_frame, text="Receiver Contact:",
                                              font=("Copperplate Gothic Bold", 18), text_color="black")
        receiver_contact_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        receiver_contact_entry = ctk.CTkEntry(receiver_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                              fg_color="white")
        receiver_contact_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Package Details Section (similar to the sender section)
        package_frame = ctk.CTkFrame(frame, width=screen_width * 0.6, corner_radius=10, fg_color="light yellow",
                                     height=300, border_width=0)
        package_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

        consignment_no_label = ctk.CTkLabel(package_frame, text="Consignment No:", font=("Copperplate Gothic Bold", 18),
                                            text_color="black")
        consignment_no_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        consignment_no_entry = ctk.CTkEntry(package_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                            fg_color="white")
        consignment_no_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        # Automatically generate consignment no when the form is loaded
        consignment_no_entry.insert(0, generate_random_consignment_no())

        # package Type
        package_type_label = ctk.CTkLabel(package_frame, text="Package Type:", font=("Copperplate Gothic Bold", 18),
                                          text_color="black")
        package_type_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        # Package type dropdown menu
        package_types = ["Documents", "Electronics", "Clothing", "Fragile", "Furniture","Books","Food Items"]
        package_type_menu = ctk.CTkOptionMenu(package_frame, values=package_types, font=("Copperplate Gothic Bold", 16))
        package_type_menu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        package_size_label = ctk.CTkLabel(package_frame, text="Package Size:", font=("Copperplate Gothic Bold", 18),
                                          text_color="black")
        package_size_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        # Dropdown for Package Size
        package_sizes = ["Small", "Medium", "Large", "Extra Large"]  # Add more sizes as needed
        package_size_dropdown = ctk.CTkOptionMenu(package_frame, values=package_sizes,
                                                  font=("Copperplate Gothic Bold", 16))
        package_size_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        package_weight_label = ctk.CTkLabel(package_frame, text="Package Weight (kg):",
                                            font=("Copperplate Gothic Bold", 18), text_color="black")
        package_weight_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        package_weight_entry = ctk.CTkEntry(package_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                            fg_color="white")
        package_weight_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # shipment Type
        shipment_type_label = ctk.CTkLabel(package_frame, text="Types of Shipment:",
                                           font=("Copperplate Gothic Bold", 18), text_color="black")
        shipment_type_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        # Package type dropdown menu
        shipment_types = ["Air", "Road", "Sea", "Train"]
        shipment_type_menu = ctk.CTkOptionMenu(package_frame, values=shipment_types,
                                               font=("Copperplate Gothic Bold", 16))
        shipment_type_menu.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # Date and Payment Section
        date_frame = ctk.CTkFrame(frame, width=screen_width * 0.6, corner_radius=10, fg_color="light coral", height=200,
                                  border_width=0)
        date_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

        pickup_date_label = ctk.CTkLabel(date_frame, text="Pickup Date:", font=("Copperplate Gothic Bold", 18),
                                         text_color="black")
        pickup_date_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        pickup_date_entry = ctk.CTkEntry(date_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                         fg_color="white")
        pickup_date_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        pickup_date_entry.bind("<Button-1>", lambda e: open_calendar(pickup_date_entry))

        total_amount_label = ctk.CTkLabel(date_frame, text="Total Amount:", font=("Copperplate Gothic Bold", 18),
                                          text_color="black")
        total_amount_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        total_amount_entry = ctk.CTkEntry(date_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                          fg_color="white")
        total_amount_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # payment type
        payment_type_label = ctk.CTkLabel(date_frame, text="Payment Type:", font=("Copperplate Gothic Bold", 18),
                                          text_color="black")
        payment_type_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        payment_types = ["COD", "UPI", "Paytm", "Google Pay", "PhonePe", "Payzap"]
        payment_type_menu = ctk.CTkOptionMenu(date_frame, values=payment_types, font=("Copperplate Gothic Bold", 16))
        payment_type_menu.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        def back_to_home_page():
            show_home_page()  # Go back to the login page when clicked

        back_icon = Image.open("images/undo.png")  # Replace with your icon file path
        back_icon = back_icon.resize((40, 40), Image.Resampling.LANCZOS)
        back_icon_tk = ImageTk.PhotoImage(back_icon)

        back_button2 = ctk.CTkButton(
            root,
            text="Back To Home",
            font=("Copperplate Gothic Bold", 16),
            width=200,
            height=50,
            image=back_icon_tk,
            fg_color="#3B8ED0",  # Customize as you prefer
            hover_color="#D65C07",
            command=back_to_home_page
        )
        back_button2.place(relx=0.1, rely=0.9, anchor="center")

        def submit_order():
            sender_name = sender_name_entry.get()
            sender_address = sender_address_entry.get()
            sender_contact = sender_contact_entry.get()
            receiver_name = receiver_name_entry.get()
            receiver_address = receiver_address_entry.get()
            receiver_contact = receiver_contact_entry.get()
            package_type = package_type_menu.get()
            package_size = package_size_dropdown.get()
            package_weight = package_weight_entry.get()
            consignment_no = consignment_no_entry.get()
            shipment_type = shipment_type_menu.get()
            pickup_date = pickup_date_entry.get()
            total_amount = total_amount_entry.get()
            payment_type = payment_type_menu.get()

            # Validate input
            if not sender_name or not sender_address or not sender_contact or not pickup_date:
                messagebox.showerror("Input Error", "Please fill in all the required fields.")
                return

            conn = connect_to_db()
            if conn is None:
                return

            cursor = conn.cursor()

            # SQL query to insert data into orders table
            sql_query = """INSERT INTO courier_orders (sender_name, sender_address, sender_contact, receiver_name, receiver_address, 
                                            receiver_contact, package_type, package_size, package_weight, consignment_no, 
                                            shipment_type,pickup_date, total_amount, payment_status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)
                    """
            values = (sender_name, sender_address, sender_contact, receiver_name, receiver_address,
                      receiver_contact, package_type, package_size, package_weight, consignment_no,
                      shipment_type, pickup_date, total_amount, payment_type)
            try:
                cursor.execute(sql_query, values)
                conn.commit()
                messagebox.showinfo("Success", "Order submitted successfully!")
                clear_form()
                # Generate new consignment number after submission
                new_consignment_no = generate_random_consignment_no()
                consignment_no_entry.delete(0, tk.END)
                consignment_no_entry.insert(0, new_consignment_no)
                generate_invoice_pdf(consignment_no)
                generate_invoice(consignment_no)  # Set the new consignment number
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

        def generate_invoice(consignment_no):
            conn = connect_to_db()
            if conn is None:
                return

            cursor = conn.cursor()

            # Fetch order details from the database using consignment number
            cursor.execute("SELECT * FROM courier_orders WHERE consignment_no = %s", (consignment_no,))
            order = cursor.fetchone()

            if not order:
                messagebox.showerror("Error", "No order found for the given consignment number!")
                return

            root = tk.Toplevel()  # Open a new invoice window
            root.title("Tax Invoice")
            root.attributes("-fullscreen", True)
            root.state("zoomed")

            canvas = tk.Canvas(root, width=794, height=900, bg="white")
            canvas.pack()

            # Draw Invoice Details
            canvas.create_rectangle(10, 10, 784, 1113, outline="black", width=2)
            canvas.create_text(397, 30, text="TAX INVOICE", font=("Arial", 12, "bold"), anchor="center")
            canvas.create_text(397, 60, text="HK Enterprises", font=("Arial", 18, "bold"), fill="green",
                               anchor="center")
            canvas.create_text(397, 85, text="M.G.Road, Opp.Garden, Jetpur 360370", font=("Arial", 10), anchor="center")

            # Business Details
            canvas.create_text(50, 90, text="Phone: +91 8733010200", font=("Arial", 9, "bold"), anchor="w")
            canvas.create_text(50, 110, text=f"Shipment type: {order[11]}", font=("Arial", 9, "bold"), anchor="w")
            canvas.create_text(397, 110, text="GSTIN: 24AALCR2857A1ZD", font=("Arial", 9, "bold"), anchor="center")
            canvas.create_text(730, 90, text=f"Date: {order[12]}", font=("Arial", 9, "bold"), anchor="e")
            canvas.create_text(744, 110, text=f"Consignment No: {order[10]}", font=("Arial", 9, "bold"), anchor="e")

            # Sender and Receiver Details
            canvas.create_rectangle(20, 130, 774, 200, outline="black", width=2)
            canvas.create_text(50, 145, text=f"Sender Name: {order[1]}", font=("Arial", 9, "bold"), anchor="w")
            canvas.create_text(50, 165, text=f"Sender Address: {order[2]}", font=("Arial", 9, "bold"), anchor="w")
            canvas.create_text(50, 185, text=f"Sender Number: {order[3]}", font=("Arial", 9, "bold"), anchor="w")

            canvas.create_text(500, 145, text=f"Receiver Name: {order[4]}", font=("Arial", 9, "bold"), anchor="w")
            canvas.create_text(500, 165, text=f"Receiver Address: {order[5]}", font=("Arial", 9, "bold"), anchor="w")
            canvas.create_text(500, 185, text=f"Receiver Number: {order[6]}", font=("Arial", 9, "bold"), anchor="w")

            # Table Header Section
            canvas.create_rectangle(20, 220, 774, 250, fill="green", outline="black", width=2)
            headers = ["    No.", "                   Package Type", "                 Weight",
                       "                     Amount"]
            x_positions = [20, 80, 350, 550]  # Adjusted for proper spacing

            for i, header in enumerate(headers):
                canvas.create_text(x_positions[i], 235, text=header, font=("Arial", 10, "bold"), fill="white",
                                   anchor="w")

            # Table Rows with Proper Borders
            row_start = 250
            row_height = 30
            for i in range(8):  # 5 Rows for better visibility
                y = row_start + (i * row_height)
                canvas.create_rectangle(20, y, 774, y + row_height, outline="black", width=2)

            # Column Dividers (Ensuring Proper Alignment)
            for x in x_positions:
                canvas.create_line(x, 250, x, 490, fill="black", width=1)  # adjust line

            # Populate First Row (Example Data from DB)
            canvas.create_text(40, 265, text="1", font=("Arial", 9), anchor="w")
            canvas.create_text(170, 265, text=f"{order[7]}", font=("Arial", 9), anchor="w")
            canvas.create_text(420, 265, text=f"{order[9]}", font=("Arial", 9), anchor="w")
            canvas.create_text(650, 265, text=f"₹{order[13]}", font=("Arial", 9), anchor="w")

            # Footer (Amount Details)
            canvas.create_rectangle(20, 500, 774, 580, outline="black", width=2)
            # Calculate Amounts
            total_amount = float(order[13])  # Convert string to float
            gst = 50  # Fixed GST
            subtotal = total_amount - gst

            # Pricing Details
            canvas.create_text(600, 515, text="Subtotal:" f"₹{order[13]}", font=("Arial", 10, "bold"), anchor="w")
            gst_amount = round(float(order[13]) * 0.18, 2)  # Calculate 18% GST
            total_price = round(float(order[13]) + gst_amount, 2)

            canvas.create_text(600, 535, text="GST (18%):"f"₹{gst_amount}", font=("Arial", 10, "bold"), anchor="w")
            canvas.create_text(600, 555, text="Grand Total:"f"₹{total_price}", font=("Arial", 10, "bold"), anchor="w")

            # Terms & Conditions Section
            canvas.create_rectangle(20, 670, 774, 760, outline="black", width=2)
            canvas.create_text(50, 685, text="Notes", font=("Arial", 10, "bold"), anchor="w")
            canvas.create_text(50, 705, text="1. No return deal", font=("Arial", 10), anchor="w")

            canvas.create_text(397, 685, text="Terms & Conditions", font=("Arial", 10, "bold"), anchor="center")
            terms = ["1. Customer will pay the GST", "2. Customer will pay the Delivery charges",
                     "3. Pay due amount within 15 days"]
            for i, term in enumerate(terms):
                canvas.create_text(397, 705 + (i * 20), text=term, font=("Arial", 10), anchor="center")

            # Authorized Signatory
            canvas.create_text(750, 720, text="Authorized Signatory", font=("Arial", 10, "bold"), anchor="e")
            canvas.create_text(730, 740, text="HK Enterprises", font=("Arial", 10), anchor="e")

            root.mainloop()
            root.quit()

        def generate_invoice_pdf(consignment_no):
            try:
                # Establish connection to MySQL Database
                connection = mysql.connector.connect(
                    host="localhost",  # MySQL host
                    user="root",  # MySQL username
                    password="",  # MySQL password (empty in this case)
                    database="cms"  # Database name
                )

                cursor = connection.cursor(dictionary=True)  # Fetch results as dictionaries

                # Fetch the invoice data for the given consignment number using a JOIN query
                query = """
                SELECT co.*, pi.package_type, pi.package_weight, pi.total_amount
                FROM courier_orders co
                LEFT JOIN courier_orders pi ON co.consignment_no = pi.consignment_no
                WHERE co.consignment_no = %s
                """
                cursor.execute(query, (consignment_no,))
                invoice_data = cursor.fetchall()  # Fetch all rows (including multiple items)

                cursor.close()
                connection.close()

                if not invoice_data:
                    messagebox.showerror("Error", "Could not fetch data from database")
                    return

                class PDF(FPDF):
                    def header(self):
                        self.set_fill_color(200, 200, 200)
                        self.rect(5, 5, 200, 30, 'F')
                        try:
                            self.image("images/ailogo.png", 10, 4, 33)
                        except Exception:
                            self.set_font("Arial", "I", 12)
                            self.cell(0, 10, "Logo not found", 0, 1, "L")

                        self.set_font("Arial", "B", 16)
                        self.cell(80)
                        self.cell(30, 10, "HK Enterprise", border=False, ln=True, align="C")
                        self.set_font("Arial", "", 10)
                        self.cell(0, 6, "M.g.road, opp.Garden, nr.civil hospital Jetpur-360370", ln=True, align="C")
                        self.cell(0, 6, "Contact: 8733010200 | GST NO: 24AAAAA12345ZZF", ln=True, align="C")
                        self.ln(5)

                    def footer(self):
                        self.set_fill_color(200, 200, 200)
                        self.rect(5, self.h - 20, 190, 15, 'F')
                        self.set_y(-15)
                        self.set_font("Arial", "I", 8)
                        self.set_text_color(0, 0, 0)
                        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

                def draw_uniform_border(pdf, x, y, width, height):
                    pdf.rect(x, y, width, height)

                pdf = PDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()

                # Invoice Details Section
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 8, "Invoice Details", ln=True, align="C")
                pdf.cell(0, 8, f"Invoice Date: {datetime.date.today().strftime('%d-%m-%Y')}", ln=True)
                pdf.ln(2)

                border_x = 10
                border_y = pdf.get_y()
                border_width = 190
                border_height = 25
                draw_uniform_border(pdf, border_x, border_y, border_width, border_height)

                # Get first row from invoice_data for general information
                first_row = invoice_data[0]

                # Add Invoice Details Content
                pdf.set_font("Arial", "", 10)
                pdf.cell(95, 6, f"Sender Name: {first_row['sender_name']}", ln=False)
                pdf.cell(100, 6, f"Receiver Name: {first_row['receiver_name']}", ln=True)

                pdf.cell(95, 6, f"Sender Contact: {first_row['sender_contact']}", ln=False)
                pdf.cell(100, 6, f"Receiver Contact: {first_row['receiver_contact']}", ln=True)

                pdf.cell(95, 6, f"Shipment Type: {first_row['shipment_type']}", ln=False)
                pdf.cell(100, 6, f"Receiver Address: {first_row['receiver_address']}", ln=True)

                pdf.cell(95, 6, f"Pickup Date: {first_row['pickup_date']}", ln=False)
                pdf.cell(100, 6, f"Consignment Number: {first_row['consignment_no']}", ln=True)

                pdf.ln(10)

                # Table Header
                pdf.set_font("Arial", "B", 10)
                columns = ["Nos.", "Package Type", "Weight", "Total Price"]
                column_widths = [10, 100, 40, 40]
                for col_name, col_width in zip(columns, column_widths):
                    pdf.cell(col_width, 8, col_name, 1, 0, "C")
                pdf.ln()

                # Table Rows - Now iterate through invoice_data
                pdf.set_font("Arial", "", 10)
                subtotal = 0
                for row_index, item in enumerate(invoice_data, start=1):
                    pdf.cell(column_widths[0], 8, str(row_index), 1, 0, "C")
                    pdf.cell(column_widths[1], 8, f"{item['package_type']}", 1, 0, "L")
                    pdf.cell(column_widths[2], 8, f"{item['package_weight']}", 1, 0, "R")
                    pdf.cell(column_widths[3], 8, f"{float(item['total_amount']):.2f}", 1, 0, "R")
                    pdf.ln()
                    subtotal += float(item['total_amount'])

                # Summary Section
                border_x = 10
                border_y = pdf.get_y()
                border_width = 190
                border_height = 25
                draw_uniform_border(pdf, border_x, border_y, border_width, border_height)

                pdf.ln(5)
                pdf.set_font("Arial", "B", 10)
                pdf.cell(0, 6, f"Subtotal: {subtotal:.2f}", ln=True, align="R")
                pdf.cell(0, 6, f"GST (18%): {subtotal * 0.18:.2f}", ln=True, align="R")
                pdf.cell(0, 6, f"Grand Total: {subtotal * 1.18:.2f}", ln=True, align="R")

                # Terms and Conditions Section
                border_x = 10
                border_y = pdf.get_y()
                border_width = 190
                border_height = 40
                draw_uniform_border(pdf, border_x, border_y, border_width, border_height)
                pdf.ln(10)
                pdf.set_font("Arial", "B", 10)

                # Left Column: Terms and Conditions
                pdf.cell(95, 6, "Terms and Conditions:", border=0, ln=0, align="L")
                pdf.cell(95, 6, "HK Enterprise", border=0, ln=1, align="R")

                # Additional Details
                pdf.set_font("Arial", "", 8)
                pdf.cell(95, 6, "1. Customer will pay the GST.", border=0, ln=0, align="L")
                pdf.cell(95, 6, "Authorized", border=0, ln=1, align="R")
                pdf.cell(95, 6, "2. Customer will pay the delivery charges.", border=0, ln=1, align="L")
                pdf.cell(95, 6, "3. Prices are subject to change without notice.", border=0, ln=1, align="L")
                pdf.cell(95, 6, "4. Pay the due amount within 15 days.", border=0, ln=1, align="L")

                # Create folder if it doesn't exist
                folder_name = "invoice"
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                # Save PDF
                file_name = f"Invoice_{first_row['consignment_no']}.pdf"
                file_path = os.path.join(folder_name, file_name)
                pdf.output(file_path)
                messagebox.showinfo("Success", f"PDF generated: {file_path}")

            except mysql.connector.Error as err:
                print(f"Error: {err}")
                messagebox.showerror("Error", "An error occurred while generating the invoice.")

        # Function to clear the form fields
        def clear_form():
            sender_name_entry.delete(0, tk.END)
            sender_address_entry.delete(0, tk.END)
            sender_contact_entry.delete(0, tk.END)
            receiver_name_entry.delete(0, tk.END)
            receiver_address_entry.delete(0, tk.END)
            receiver_contact_entry.delete(0, tk.END)
            package_type_menu.set("Select Package Type")
            package_size_dropdown.set("Select Package Size")
            package_weight_entry.delete(0, tk.END)
            consignment_no_entry.delete(0, tk.END)
            pickup_date_entry.delete(0, tk.END)
            total_amount_entry.delete(0, tk.END)
            payment_type_menu.set("Select Payment Type")

        # Function to open the calendar popup for picking a date
        def open_calendar(entry_field):
            def set_date(selected_date):
                entry_field.delete(0, tk.END)
                entry_field.insert(0, selected_date)
                calendar_window.destroy()

            calendar_window = tk.Toplevel(root)
            calendar_window.title("Select Date")

            cal = Calendar(calendar_window, selectmode="day", date_pattern="yyyy-mm-dd")
            cal.pack(padx=10, pady=10)

            # Button to confirm the date selection
            select_button = ctk.CTkButton(calendar_window, text="Select", command=lambda: set_date(cal.get_date()))
            select_button.pack(pady=10)

        # Submit Button
        submit_button = ctk.CTkButton(frame, text="Submit Order", font=("Copperplate Gothic Bold", 18),
                                      command=submit_order, fg_color="green", hover_color="lightgreen")
        submit_button.grid(row=5, column=0, pady=20, columnspan=2)



    def about_us():
        global bg_image_tk  # Ensure persistence

        bg_image_path = "images/c4.jpg"
        bg_image = Image.open(bg_image_path)
        bg_image_resized = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        bg_image_tk = ImageTk.PhotoImage(bg_image_resized)

        canvas = ctk.CTkCanvas(root, width=screen_width, height=screen_height)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)
        canvas.image = bg_image_tk

        frame = ctk.CTkFrame(root, fg_color="#ffffff", width=350, height=1100,
                             corner_radius=10, border_width=4,border_color="black")
        frame.place(x=700, y=180)

        # Adjust the font size based on the screen height
        font_size = int(screen_height * 0.05)  # Font size is 5% of screen height

        # Title label inside the frame
        title_label = ctk.CTkLabel(frame, text="About Us", font=("Copperplate Gothic Bold", 32, "bold"),
                                   text_color="black")
        title_label.grid(row=0, column=0, pady=(20, 10), padx=20)

        description = """
        🚀 Welcome to HK Enterprise!

        At HK ENTERPRISE, we are committed to providing fast, reliable, and secure courier services.
        With years of experience in the logistics industry, we ensure that every package is handled 
        with utmost care and efficiency.

        🌟 Why Choose Us?
        ✅ Fast & Reliable Delivery
        ✅ Secure Handling
        ✅ Affordable Rates
        ✅ Real-Time Tracking
        ✅ 24/7 Customer Support

        📌 Our Mission:
        We aim to bridge distances by delivering not just parcels but trust and reliability.
        Whether it’s a business shipment, personal gift, or urgent document, we ensure 
        it reaches its destination safely and on time.

        📌 Our Vision:
        To become a leading courier service provider, known for innovation, efficiency, and customer satisfaction.

        📦 Your Package, Our Priority!
        """

        desc_label = ctk.CTkLabel(frame, text=description, font=("Copperplate Gothic Bold", 16), text_color="black",
                                  wraplength=screen_width * 0.6)
        desc_label.grid(row=1, column=0, padx=20, pady=10)

        # Welcome Banner
        welcome_label12 = ctk.CTkLabel(
            root,
            text="About Us Page!",
            font=("Copperplate Gothic Bold", font_size, "bold"),
            text_color="white",
            fg_color="black",  # Proper background color for CTkLabel
            width=screen_width,
            height=100,
        )
        welcome_label12.place(relx=0.5, rely=0.1, anchor="center")

        def back_to_home_page():
            show_home_page()  # Go back to the login page when clicked

        back_icon = Image.open("images/undo.png")  # Replace with your icon file path
        back_icon = back_icon.resize((40, 40), Image.Resampling.LANCZOS)
        back_icon_tk = ImageTk.PhotoImage(back_icon)

        back_button2 = ctk.CTkButton(
            root,
            text="Back To Home",
            font=("Copperplate Gothic Bold", 16),
            width=200,
            height=50,
            image=back_icon_tk,
            fg_color="#3B8ED0",  # Customize as you prefer
            hover_color="#D65C07",
            command=back_to_home_page
        )
        back_button2.place(relx=0.1, rely=0.9, anchor="center")

        print("Show_About_us_page")


    # Load icons for each option
    track_icon = Image.open("images/b2.png")  # Replace with your icon file path
    track_icon = track_icon.resize((40, 40), Image.Resampling.LANCZOS)
    track_icon_tk = ImageTk.PhotoImage(track_icon)

    pickup_icon = Image.open("images/b5.png")  # Replace with your icon file path
    pickup_icon = pickup_icon.resize((40, 40), Image.Resampling.LANCZOS)
    pickup_icon_tk = ImageTk.PhotoImage(pickup_icon)

    deliveries_icon = Image.open("images/b3.png")  # Replace with your icon file path
    deliveries_icon = deliveries_icon.resize((40, 40), Image.Resampling.LANCZOS)
    deliveries_icon_tk = ImageTk.PhotoImage(deliveries_icon)

    support_icon = Image.open("images/b4.png")  # Replace with your icon file path
    support_icon = support_icon.resize((40, 40), Image.Resampling.LANCZOS)
    support_icon_tk = ImageTk.PhotoImage(support_icon)

    about_us_icon = Image.open("images/b7.png")  # Replace with your icon file path
    about_us_icon = about_us_icon.resize((40, 40), Image.Resampling.LANCZOS)
    about_us_icon_tk = ImageTk.PhotoImage(about_us_icon)

    logout_icon = Image.open("images/power.png")  # Replace with your icon file path
    logout_icon = logout_icon.resize((40, 40), Image.Resampling.LANCZOS)
    logout_icon_tk = ImageTk.PhotoImage(logout_icon)


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

    def create_button(text, icon, command):
        button = ctk.CTkButton(
            master=root,
            text=text,
            width=button_width,
            height=button_height,
            font=("Copperplate Gothic Bold", 16),
            image=icon,
            compound="left",
            command=command
        )
        button.place(relx=0.7, rely=0.4, anchor="center")  # Fix rely to be in range (0.0 - 1.0)

    # Example usage (ensure `pickup_icon_tk` is defined)
    create_button("Manage order", pickup_icon_tk, lambda: open_page("manage_order.py"))


    # Manage Deliveries button
    deliveries_button = ctk.CTkButton(
        root,
        text="Send Deliveries",
        font=("Copperplate Gothic Bold", 16),
        width=button_width,
        height=button_height,
        image=deliveries_icon_tk,
        compound="left",  # Places the icon to the left of the text
        command=manage_deliveries
    )
    deliveries_button.place(relx=0.7, rely=0.5, anchor="center")

    def create_button(text, icon, command):
        button_cs = ctk.CTkButton(
            master=root,
            text=text,
            width=button_width,
            height=button_height,
            font=("Copperplate Gothic Bold", 16),
            image=icon,
            compound="left",
            command=command
        )
        button_cs.place(relx=0.7, rely=0.6, anchor="center")  # Fix rely to be in range (0.0 - 1.0)

    # Example usage (ensure `pickup_icon_tk` is defined)
    create_button("Customer Support", pickup_icon_tk, lambda: open_page("customer_support.py"))

    about_button = ctk.CTkButton(
        root,
        text="About Us",
        font=("Copperplate Gothic Bold", 16),
        width=button_width,
        height=button_height,
        image=about_us_icon_tk,
        compound="left",
        command=about_us
    )
    about_button.place(relx=0.7, rely=0.7, anchor="center")

    logout_button = ctk.CTkButton(
        root,
        text="Logout",
        font=("Copperplate Gothic Bold", 16),
        width=button_width,
        height=button_height,
        image=logout_icon_tk,
        compound="left",
        command=back_to_login
    )
    logout_button.place(relx=0.7, rely=0.8, anchor="center")






# Start the welcome page
show_welcome_page()

# Start the Tkinter event loop
root.mainloop()
