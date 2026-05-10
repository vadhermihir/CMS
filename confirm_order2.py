import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime
from tkinter import messagebox

from click import command


# MySQL Connection Function
def fetch_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cms"
    )
    cursor = conn.cursor()

    # Query to fetch relevant data
    cursor.execute("""
        SELECT consignment_no, sender_name, sender_contact, 
               receiver_name, receiver_contact, pickup_date 
        FROM courier_orders
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Get today's date
    today_date = datetime.today().date()

    # Modify data to include "Order Status"
    updated_data = []
    for row in rows:
        consignment_no, sender_name, sender_contact, receiver_name, receiver_contact, pickup_date = row

        # Check if pickup_date is valid
        if pickup_date:
            pickup_date = datetime.strptime(str(pickup_date), "%Y-%m-%d").date()

            # Compare with today
            if pickup_date <= today_date:  # Past or today → Delivered
                order_status = "Order Delivered"
            else:  # Future date → Pending
                order_status = "Pending Orders"
        else:
            order_status = "Pending Orders"

        updated_data.append(
            (consignment_no, sender_name, sender_contact, receiver_name, receiver_contact, order_status))

    return updated_data


# Function to delete an order from MySQL
def delete_order(consignment_no):
    confirm = messagebox.askyesno("Delete Order", f"Are you sure you want to delete Order {consignment_no}?")
    if confirm:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cms"
        )
        cursor = conn.cursor()

        # Delete query
        cursor.execute("DELETE FROM courier_orders WHERE consignment_no = %s", (consignment_no,))
        conn.commit()
        cursor.close()
        conn.close()

        # Refresh the table UI after deletion
        fetch_and_display_data()


# Function to fetch data and update the UI
def fetch_and_display_data():
    # Clear existing widgets in table_frame
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Table Column Headers
    columns = ["Sr No", "Consignment No", "Sender Name", "Sender Contact", "Receiver Name", "Receiver Contact",
               "Order Status", "Edit", "Delete"]

    header_bg = "#FDC029"
    font_header = ("Copperplate Gothic Bold", 16, "bold")

    for col_index, col_name in enumerate(columns):
        header = ctk.CTkLabel(table_frame, text=col_name, font=font_header, text_color="black", fg_color=header_bg,
                              corner_radius=5)
        header.grid(row=0, column=col_index, padx=10, pady=10, sticky="ew")

    # Fetch Data from MySQL
    data = fetch_data()
    row_colors = ["#0052B0", "#003E7D"]
    font_cell = ("Copperplate Gothic Bold", 14)

    for row_index, row_data in enumerate(data, start=1):
        row_bg = row_colors[row_index % 2]

        sr_no = row_index
        full_row = [sr_no] + list(row_data)

        for col_index, cell_data in enumerate(full_row):
            cell = ctk.CTkLabel(table_frame, text=cell_data, font=font_cell, text_color="white", fg_color=row_bg,
                                corner_radius=5)
            cell.grid(row=row_index, column=col_index, padx=10, pady=5, sticky="ew")

        consignment_no = row_data[0]

        # Edit Button
        edit_button = ctk.CTkButton(
            table_frame, text="Edit", font=("Copperplate Gothic Bold", 12), fg_color="#3498DB", text_color="white",
            corner_radius=5, width=100, height=25)
        edit_button.grid(row=row_index, column=len(columns) - 2, padx=5, pady=3)

        # Delete Button
        delete_button = ctk.CTkButton(
            table_frame, text="Delete", font=("Copperplate Gothic Bold", 12), fg_color="#E74C3C", text_color="white",
            corner_radius=5, width=100, height=25, command=lambda cn=consignment_no: delete_order(cn)
        )
        delete_button.grid(row=row_index, column=len(columns) - 1, padx=5, pady=3)


# Initialize Tkinter Window
root = tk.Tk()
root.attributes("-fullscreen", True)
root.title("Track Tour Order")

# Get Screen Size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load Background Image
bg_image_path = "images/c88.png"
bg_image = Image.open(bg_image_path).resize((screen_width, screen_height), Image.Resampling.LANCZOS)
bg_image_tk = ImageTk.PhotoImage(bg_image)

# Create Canvas for Background
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)

# Welcome Label
welcome_label = ctk.CTkLabel(root, text="Welcome To Order Manage Page", font=("Copperplate Gothic Bold", 36, "bold"),
                             text_color="white", fg_color="#0051AD", width=screen_width, height=100)
welcome_label.place(x=0, y=10)

# Main Frame
frame = ctk.CTkFrame(root, fg_color="white", width=1520, height=730, corner_radius=5, border_width=3,
                     border_color="black")
frame.place(x=10, y=120)

# Scrollable Table Frame
table_frame = ctk.CTkScrollableFrame(frame, width=1480, height=680, fg_color="white")
table_frame.place(x=10, y=10)

# Load initial data
fetch_and_display_data()

# Run Tkinter Main Loop
root.mainloop()
