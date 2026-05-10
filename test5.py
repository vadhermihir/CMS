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
    cursor.execute("SELECT sender_name,sender_address, sender_contact, receiver_name,receiver_address,receiver_contact,package_type,package_size,package_weight,shipment_type, pickup_date, total_amount,payment_status FROM courier_orders WHERE consignment_no = %s", (consignment_no,))
    order = cursor.fetchone()
    cursor.close()
    conn.close()



    if not order:
        messagebox.showerror("Error", "Order not found!")
        return

    sender_name,sender_address,sender_contact, receiver_name,receiver_address, receiver_contact,package_type,package_size,package_weight,shipment_type,pickup_date,total_amount,package_status = order

    # Create a new Toplevel window
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Order Details")
    edit_window.attributes("-fullscreen", True) # Full screen

    bg_image_path = "images/c4.jpg"  # Set the path to your background image
    bg_image = Image.open(bg_image_path)
    bg_image_resized = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # High-quality resizing
    bg_image_tk = ImageTk.PhotoImage(bg_image_resized)

    # Create a canvas to display the background image
    canvas = ctk.CTkCanvas(edit_window, width=screen_width, height=screen_height)
    canvas.place(x=0, y=0)  # Use place() for more precise control

    # Draw the background image on the canvas
    canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)

    # Keep a reference to the image to prevent it from being garbage collected
    canvas.image = bg_image_tk

    frame = ctk.CTkFrame(edit_window, fg_color="#FFC736", width=screen_width * 0.7, height=screen_height * 0.9,
                         corner_radius=0, border_width=0)
    frame.place(relx=0.7, rely=0.5, anchor="center")

    title_label = ctk.CTkLabel(frame, text="", font=("Copperplate Gothic Bold", 32, "bold"), text_color="black")
    title_label.grid(row=0, column=0, columnspan=2, pady=(20, 30))

    # Adjust the font size based on the screen height (you can also use width if preferred)
    font_size = int(screen_height * 0.05)  # Font size is 5% of the screen height

    # Set up the title label with dynamic font size
    welcome_label = ctk.CTkLabel(
        edit_window,
        text="Delivery Updation Page!",
        font=("Copperplate Gothic Bold", font_size, "bold"),
        text_color="white",
        bg_color="black",
        width=screen_width,
        height=50,
    )
    welcome_label.place(x=0, y=10)
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

    # Inserting value into the entry field
    sender_name_entry.insert(0, sender_name)  # sender_name should be a string


    sender_address_label = ctk.CTkLabel(sender_frame, text="Sender Address:", font=("Copperplate Gothic Bold", 18),
                                        text_color="black")
    sender_address_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    sender_address_entry = ctk.CTkEntry(sender_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                        fg_color="white")
    sender_address_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    sender_address_entry.insert(0, sender_address)

    sender_contact_label = ctk.CTkLabel(sender_frame, text="Sender Contact:", font=("Copperplate Gothic Bold", 18),
                                        text_color="black")
    sender_contact_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    sender_contact_entry = ctk.CTkEntry(sender_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                        fg_color="white")
    sender_contact_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    sender_contact_entry.insert(0, sender_contact)

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
    receiver_name_entry.insert(0, receiver_name)

    receiver_address_label = ctk.CTkLabel(receiver_frame, text="Receiver Address:",
                                          font=("Copperplate Gothic Bold", 18), text_color="black")
    receiver_address_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    receiver_address_entry = ctk.CTkEntry(receiver_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                          fg_color="white")
    receiver_address_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    receiver_address_entry.insert(0, receiver_address)

    receiver_contact_label = ctk.CTkLabel(receiver_frame, text="Receiver Contact:",
                                          font=("Copperplate Gothic Bold", 18), text_color="black")
    receiver_contact_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    receiver_contact_entry = ctk.CTkEntry(receiver_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                          fg_color="white")
    receiver_contact_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    receiver_contact_entry.insert(0, receiver_contact)

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
    consignment_no_entry.insert(0, consignment_no)

    # package Type
    package_type_label = ctk.CTkLabel(package_frame, text="Package Type:", font=("Copperplate Gothic Bold", 18),
                                      text_color="black")
    package_type_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    # Package type dropdown menu
    package_types = ["Documents", "Electronics", "Clothing", "Fragile", "Furniture", "Books", "Food Items"]
    package_type_menu = ctk.CTkOptionMenu(package_frame, values=package_types, font=("Copperplate Gothic Bold", 16))
    package_type_menu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    package_type_menu.set(package_type)

    package_size_label = ctk.CTkLabel(package_frame, text="Package Size:", font=("Copperplate Gothic Bold", 18),
                                      text_color="black")
    package_size_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    # Dropdown for Package Size
    package_sizes = ["Small", "Medium", "Large", "Extra Large"]  # Add more sizes as needed
    package_size_dropdown = ctk.CTkOptionMenu(package_frame, values=package_sizes,
                                              font=("Copperplate Gothic Bold", 16))
    package_size_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    package_size_dropdown.set(package_size)


    package_weight_label = ctk.CTkLabel(package_frame, text="Package Weight (kg):",
                                        font=("Copperplate Gothic Bold", 18), text_color="black")
    package_weight_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    package_weight_entry = ctk.CTkEntry(package_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                        fg_color="white")
    package_weight_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
    package_weight_entry.insert(0, package_weight)

    # shipment Type
    shipment_type_label = ctk.CTkLabel(package_frame, text="Types of Shipment:",
                                       font=("Copperplate Gothic Bold", 18), text_color="black")
    shipment_type_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    # Package type dropdown menu
    shipment_types = ["Air", "Road", "Sea", "Train"]
    shipment_type_menu = ctk.CTkOptionMenu(package_frame, values=shipment_types,
                                           font=("Copperplate Gothic Bold", 16))
    shipment_type_menu.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
    shipment_type_menu.set(shipment_type)

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
    pickup_date_entry.insert(0, str(pickup_date))


    total_amount_label = ctk.CTkLabel(date_frame, text="Total Amount:", font=("Copperplate Gothic Bold", 18),
                                      text_color="black")
    total_amount_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    total_amount_entry = ctk.CTkEntry(date_frame, font=("Copperplate Gothic Bold", 16), text_color="black",
                                      fg_color="white")
    total_amount_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    total_amount_entry.insert(0, str(total_amount))

    # payment type
    payment_type_label = ctk.CTkLabel(date_frame, text="Payment Type:", font=("Copperplate Gothic Bold", 18),
                                      text_color="black")
    payment_type_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    payment_types = ["COD", "UPI", "Paytm", "Google Pay", "PhonePe", "Payzap"]
    payment_type_menu = ctk.CTkOptionMenu(date_frame, values=payment_types, font=("Copperplate Gothic Bold", 16))
    payment_type_menu.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    payment_type_menu.set(package_status)

    def back_to_home_page():
        print("back - back")
        #show_home_page()   Go back to the login page when clicked

    back_icon = Image.open("images/undo.png")  # Replace with your icon file path
    back_icon = back_icon.resize((40, 40), Image.Resampling.LANCZOS)
    back_icon_tk = ImageTk.PhotoImage(back_icon)

    back_button2 = ctk.CTkButton(
        edit_window,
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

    def update_order():
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="cms")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE courier_orders 
            SET sender_name=%s, sender_address=%s, sender_contact=%s,
                receiver_name=%s, receiver_address=%s, receiver_contact=%s,
                package_type=%s, package_size=%s, package_weight=%s,
                shipment_type=%s, pickup_date=%s, total_amount=%s, payment_status=%s
            WHERE consignment_no=%s
        """, (
            sender_name_entry.get(), sender_address_entry.get(), sender_contact_entry.get(),
            receiver_name_entry.get(), receiver_address_entry.get(), receiver_contact_entry.get(),
            package_type_menu.get(), package_size_dropdown.get(), package_weight_entry.get(),
            shipment_type_menu.get(), pickup_date_entry.get(), total_amount_entry.get(),
            payment_type_menu.get(), consignment_no
        ))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Order updated successfully!")
        edit_window.destroy()
        fetch_and_display_data()


        # Submit Button
    submit_button = ctk.CTkButton(frame, text="Update Order", font=("Copperplate Gothic Bold", 18),
                                  command=update_order, fg_color="green", hover_color="lightgreen")
    submit_button.grid(row=5, column=0, pady=20, columnspan=2)


def fetch_and_display_data():
    # Load Background Image
    bg_image_path = "images/c88.png"
    bg_image = Image.open(bg_image_path).resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_image_tk = ImageTk.PhotoImage(bg_image)

    # Create Canvas for Background
    canvas = tk.Canvas(root, width=screen_width, height=screen_height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)

    # Welcome Label
    welcome_label = ctk.CTkLabel(root, text="Welcome To Order Manage Page",
                                 font=("Copperplate Gothic Bold", 36, "bold"),
                                 text_color="white", fg_color="#0051AD", width=screen_width, height=100)
    welcome_label.place(x=0, y=10)

    # Main Frame
    frame = ctk.CTkFrame(root, fg_color="white", width=1520, height=730, corner_radius=5, border_width=3,
                         border_color="black")
    frame.place(x=10, y=120)

    # Scrollable Table Frame
    table_frame = ctk.CTkScrollableFrame(frame, width=1480, height=680, fg_color="white")
    table_frame.place(x=10, y=10)
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




fetch_and_display_data()
root.mainloop()
