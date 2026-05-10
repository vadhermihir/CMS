import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime
from tkinter import messagebox

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

# Function to open the Edit Order window
def open_edit_window(consignment_no):
    # Fetch order details
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="cms")
    cursor = conn.cursor()
    cursor.execute("SELECT sender_name, sender_contact, receiver_name, receiver_contact, pickup_date FROM courier_orders WHERE consignment_no = %s", (consignment_no,))
    order = cursor.fetchone()
    cursor.close()
    conn.close()

    if not order:
        messagebox.showerror("Error", "Order not found!")
        return

    sender_name, sender_contact, receiver_name, receiver_contact, pickup_date = order

    # Create a new window
    edit_window = tk.Toplevel(root)
    edit_window.title(f"Edit Order {consignment_no}")
    edit_window.geometry("400x400")

    # Labels & Entry Fields
    tk.Label(edit_window, text="Sender Name:").pack()
    sender_entry = tk.Entry(edit_window)
    sender_entry.insert(0, sender_name)
    sender_entry.pack()

    tk.Label(edit_window, text="Sender Contact:").pack()
    sender_contact_entry = tk.Entry(edit_window)
    sender_contact_entry.insert(0, sender_contact)
    sender_contact_entry.pack()

    tk.Label(edit_window, text="Receiver Name:").pack()
    receiver_entry = tk.Entry(edit_window)
    receiver_entry.insert(0, receiver_name)
    receiver_entry.pack()

    tk.Label(edit_window, text="Receiver Contact:").pack()
    receiver_contact_entry = tk.Entry(edit_window)
    receiver_contact_entry.insert(0, receiver_contact)
    receiver_contact_entry.pack()

    tk.Label(edit_window, text="Pickup Date (YYYY-MM-DD):").pack()
    pickup_entry = tk.Entry(edit_window)
    pickup_entry.insert(0, str(pickup_date))
    pickup_entry.pack()

    # Function to save changes
    def save_changes():
        new_sender = sender_entry.get()
        new_sender_contact = sender_contact_entry.get()
        new_receiver = receiver_entry.get()
        new_receiver_contact = receiver_contact_entry.get()
        new_pickup_date = pickup_entry.get()

        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="cms")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE courier_orders 
                SET sender_name = %s, sender_contact = %s, receiver_name = %s, receiver_contact = %s, pickup_date = %s 
                WHERE consignment_no = %s
            """, (new_sender, new_sender_contact, new_receiver, new_receiver_contact, new_pickup_date, consignment_no))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Order updated successfully!")
            edit_window.destroy()
            fetch_and_display_data()  # Refresh table
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}")

    # Save Button
    tk.Button(edit_window, text="Save Changes", command=save_changes, bg="green", fg="white").pack(pady=10)

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
        row_bg = row_colors[(row_index - 1) % 2]

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
            corner_radius=5, width=100, height=25, command=lambda cn=consignment_no: open_edit_window(cn)
        )
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


fetch_and_display_data()
root.mainloop()
