import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
from PIL import Image, ImageTk
import mysql.connector
import random
import string
from reportlab.pdfgen import canvas
import datetime
import os
import webbrowser

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

# Initialize Tkinter window
root = tk.Tk()

# Set the window to full screen
root.attributes("-fullscreen", True)
root.title("Courier Management")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()



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
    submit_button = ctk.CTkButton(frame, text="Update Order", font=("Copperplate Gothic Bold", 18),
                                  command="", fg_color="green", hover_color="lightgreen")
    submit_button.grid(row=5, column=0, columnspan=2, pady=30)


manage_deliveries()

# Start the Tkinter event loop
root.mainloop()
