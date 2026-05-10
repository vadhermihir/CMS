import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
from PIL import Image, ImageTk
import mysql.connector
import random
import string

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

# Function to generate a random consignment number
def generate_random_consignment_no():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Function to submit the order
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
    payment_status = payment_status_menu.get()  # Fetch selected value from dropdown

    # Validate input
    if not sender_name or not sender_address or not sender_contact or not pickup_date:
        messagebox.showerror("Input Error", "Please fill in all required fields.")
        return

    conn = connect_to_db()
    if conn is None:
        return

    cursor = conn.cursor()

    # SQL query to insert data into orders table
    sql_query = """
        INSERT INTO orders (sender_name, sender_address, sender_contact, receiver_name, receiver_address, 
                            receiver_contact, package_type, package_size, package_weight, consignment_no, 
                            shipment_types, pickup_date, total_amount, payment_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (sender_name, sender_address, sender_contact, receiver_name, receiver_address,
              receiver_contact, package_type, package_size, package_weight, consignment_no,
              shipment_types, pickup_date, total_amount, payment_status)

    try:
        cursor.execute(sql_query, values)
        conn.commit()
        messagebox.showinfo("Success", "Order submitted successfully!")
        clear_form()
        # Generate new consignment number after submission
        consignment_no_entry.delete(0, tk.END)
        consignment_no_entry.insert(0, generate_random_consignment_no())
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
    payment_status_menu.set("Select Payment Status")

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

    select_button = ctk.CTkButton(calendar_window, text="Select", command=lambda: set_date(cal.get_date()))
    select_button.pack(pady=10)

# Initialize Tkinter window
root = tk.Tk()
root.attributes("-fullscreen", True)
root.title("Courier Order Management System")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Background Image
bg_image_path = "c3.jpg"
bg_image = Image.open(bg_image_path)
bg_image_resized = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
bg_image_tk = ImageTk.PhotoImage(bg_image_resized)

canvas = ctk.CTkCanvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)
canvas.image = bg_image_tk

frame = ctk.CTkFrame(root, fg_color="#FFC736", width=screen_width * 0.7, height=screen_height * 0.9)
frame.place(relx=0.7, rely=0.5, anchor="center")

# Title Label
welcome_label = ctk.CTkLabel(
    root, text="Courier Order Management Page!", font=("Copperplate Gothic Bold", 36, "bold"),
    text_color="white", bg_color="black", width=screen_width, height=100
)
welcome_label.place(relx=0.5, rely=0.1, anchor="center")

# Sender Details Section
sender_name_entry = ctk.CTkEntry(frame, font=("Copperplate Gothic Bold", 16))
sender_address_entry = ctk.CTkEntry(frame, font=("Copperplate Gothic Bold", 16))
sender_contact_entry = ctk.CTkEntry(frame, font=("Copperplate Gothic Bold", 16))

# Receiver Details Section
receiver_name_entry = ctk.CTkEntry(frame, font=("Copperplate Gothic Bold", 16))
receiver_address_entry = ctk.CTkEntry(frame, font=("Copperplate Gothic Bold", 16))
receiver_contact_entry = ctk.CTkEntry(frame, font=("Copperplate Gothic Bold", 16))

# Package Details Section
consignment_no_entry = ctk.CTkEntry(frame, font=("Copperplate Gothic Bold", 16))
consignment_no_entry.insert(0, generate_random_consignment_no())

package_types = ["Select Package Type", "Documents", "Electronics", "Clothing", "Fragile", "Furniture"]
package_type_menu = ctk.CTkOptionMenu(frame, values=package_types, font=("Copperplate Gothic Bold", 16))

package_sizes = ["Small", "Medium", "Large", "Extra Large"]
package_size_dropdown = ctk.CTkOptionMenu(frame, values=package_sizes, font=("Copperplate Gothic Bold", 16))

package_weight_entry = ctk.CTkEntry(frame, font=("Copperplate Gothic Bold", 16))

shipment_types = ["Select Shipment Type", "Air", "Road", "Sea", "Train"]
shipment_types_menu = ctk.CTkOptionMenu(frame, values=shipment_types, font=("Copperplate Gothic Bold", 16))

# Date and Payment Section
pickup_date_entry = ctk.CTkEntry(frame, font=("Copperplate Gothic Bold", 16))
pickup_date_entry.bind("<Button-1>", lambda e: open_calendar(pickup_date_entry))

total_amount_entry = ctk.CTkEntry(frame, font=("Copperplate Gothic Bold", 16))

# Payment Status Dropdown
payment_status_options = ["Select Payment Status", "Paid", "Unpaid", "Pending"]
payment_status_menu = ctk.CTkOptionMenu(frame, values=payment_status_options, font=("Copperplate Gothic Bold", 16))

# Submit Button
submit_button = ctk.CTkButton(frame, text="Submit Order", font=("Copperplate Gothic Bold", 18), command=submit_order, fg_color="green", hover_color="lightgreen")
submit_button.grid(row=5, column=0, columnspan=2, pady=30)

root.mainloop()
