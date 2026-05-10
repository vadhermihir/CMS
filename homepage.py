import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
from PIL import Image, ImageTk
import mysql.connector
import random
import string
import subprocess
import os



# Path to your scripts
PROJECT_PATH = r"D:\2Courier Management System Project In Python Source Code"

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
root.title("Courier Management")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Main frame with a subtle shadow effect and padding (no border)
frame = ctk.CTkFrame(root, fg_color="#ECBA7F", width=screen_width * 0.7, height=screen_height * 0.9,corner_radius=0,border_width=0)
frame.place(relx=0.7, rely=0.5, anchor="center")

# Load the background image
bg_image_path = "images/c4.jpg"  # Replace with your image file path

try:
    bg_image = Image.open(bg_image_path)
except Exception as e:
    print(f"Error loading image: {e}")
    root.quit()  # Close the application if the image fails to load

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
    package_types = ["Select Package Type", "Documents", "Electronics", "Clothing", "Fragile", "Furniture"]
    package_type_menu = ctk.CTkOptionMenu(package_frame, values=package_types, font=("Copperplate Gothic Bold", 16),
                                          text_color="black", fg_color="white")
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

    # package Type
    types_of_shipment_label = ctk.CTkLabel(package_frame, text="Types of Shipment:",
                                           font=("Copperplate Gothic Bold", 18), text_color="black")
    types_of_shipment_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    # Package type dropdown menu
    shipment_types = ["Select Package Type", "Air", "Road", "Sea", "Train"]
    shipment_types_menu = ctk.CTkOptionMenu(package_frame, values=shipment_types,
                                            font=("Copperplate Gothic Bold", 16))
    shipment_types_menu.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

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

    # package Type
    package_type_label = ctk.CTkLabel(package_frame, text="Package Type:", font=("Copperplate Gothic Bold", 18),
                                      text_color="black")
    package_type_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    # Package type dropdown menu
    package_types = ["Select Package Type", "Documents", "Electronics", "Clothing", "Fragile", "Furniture"]
    package_type_menu = ctk.CTkOptionMenu(package_frame, values=package_types, font=("Copperplate Gothic Bold", 16))
    package_type_menu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    payment_type_label = ctk.CTkLabel(date_frame, text="Payment Type:", font=("Copperplate Gothic Bold", 18),
                                      text_color="black")
    payment_type_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    payment_types = ["COD", "UPI", "Paytm", "Google Pay", "PhonePe", "Payzap"]
    payment_type_menu = ctk.CTkOptionMenu(date_frame, values=payment_types, font=("Copperplate Gothic Bold", 16))
    payment_type_menu.grid(row=2, column=1, padx=10, pady=5, sticky="ew")


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
        shipment_types = shipment_types_menu.get()
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
        sql_query = """
                    INSERT INTO courier_orders (sender_name, sender_address, sender_contact, receiver_name, receiver_address, 
                                        receiver_contact, package_type, package_size, package_weight, consignment_no, 
                                        shipment_types,pickup_date, total_amount, payment_status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)
                """
        values = (sender_name, sender_address, sender_contact, receiver_name, receiver_address,
                  receiver_contact, package_type, package_size, package_weight, consignment_no,
                  shipment_types, pickup_date, total_amount, payment_type)

        try:
            cursor.execute(sql_query, values)
            conn.commit()
            messagebox.showinfo("Success", "Order submitted successfully!")
            clear_form()
            # Generate new consignment number after submission
            new_consignment_no = generate_random_consignment_no()
            consignment_no_entry.delete(0, tk.END)
            consignment_no_entry.insert(0, new_consignment_no)  # Set the new consignment number
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

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
    submit_button.grid(row=5, column=0, columnspan=2, pady=30)


def customer_support():
    print("Accessing Customer Support...")

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

about_button=ctk.CTkButton(
    root,
    text="About Us",
    font=("Copperplate Gothic Bold",16),
    width=button_width,
    height=button_height,
    image=about_us_icon_tk,
    compound="left",
)
about_button.place(relx=0.7, rely=0.7, anchor="center")

# Start the Tkinter event loop
root.mainloop()
