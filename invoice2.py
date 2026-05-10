import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
from PIL import Image, ImageTk
import mysql.connector
import random
import string
from fpdf import FPDF
import os
import datetime


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



def manage_deliveries():
    bg_image_path = "c4.jpg"
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
    package_types = ["Documents","Electronics","Clothing", "Fragile", "Furniture"]
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

    # package Type
    types_of_shipment_label = ctk.CTkLabel(package_frame, text="Types of Shipment:",
                                           font=("Copperplate Gothic Bold", 18), text_color="black")
    types_of_shipment_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    # Package type dropdown menu
    shipment_types = ["Air", "Road", "Sea", "Train"]
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

    # payment type
    payment_type_label = ctk.CTkLabel(date_frame, text="Payment Type:", font=("Copperplate Gothic Bold", 18),
                                      text_color="black")
    payment_type_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    payment_types = ["COD", "UPI", "Paytm", "Google Pay", "PhonePe", "Payzap"]
    payment_type_menu = ctk.CTkOptionMenu(date_frame, values=payment_types, font=("Copperplate Gothic Bold", 16))
    payment_type_menu.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    def back_to_home_page():
        show_home_page()  # Go back to the login page when clicked

    back_button2 = ctk.CTkButton(
        root,
        text="Back To Home",
        font=("Copperplate Gothic Bold", 16),
        width=200,
        height=50,
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
        shipment_types = shipment_types_menu.get()
        pickup_date = pickup_date_entry.get()
        total_amount = total_amount_entry.get()
        payment_type = payment_type_menu.get()

        # Validate input
        #if not sender_name or not sender_address or not sender_contact or not pickup_date:
            #messagebox.showerror("Input Error", "Please fill in all the required fields.")
            #return

        conn = connect_to_db()
        if conn is None:
            return

        cursor = conn.cursor()

        # SQL query to insert data into orders table
        sql_query = """INSERT INTO courier_orders (sender_name, sender_address, sender_contact, receiver_name, receiver_address, 
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
            consignment_no_entry.insert(0, new_consignment_no)
            generate_invoice_pdf(consignment_no)
            generate_invoice(consignment_no) # Set the new consignment number
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
        canvas.create_text(397, 60, text="HK Enterprises", font=("Arial", 18, "bold"), fill="green", anchor="center")
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
        headers = ["    No.", "                   Package Type", "                 Weight", "                     Amount"]
        x_positions = [20, 80, 350, 550]  # Adjusted for proper spacing

        for i, header in enumerate(headers):
            canvas.create_text(x_positions[i], 235, text=header, font=("Arial", 10, "bold"), fill="white", anchor="w")

        # Table Rows with Proper Borders
        row_start = 250
        row_height = 30
        for i in range(8):  # 5 Rows for better visibility
            y = row_start + (i * row_height)
            canvas.create_rectangle(20, y, 774, y + row_height, outline="black", width=2)

        # Column Dividers (Ensuring Proper Alignment)
        for x in x_positions:
            canvas.create_line(x, 250, x, 490, fill="black", width=1) #adjust line

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
                        self.image("h1.png", 10, 8, 33)
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

            pdf.cell(95, 6, f"Shipment Type: {first_row['shipment_types']}", ln=False)
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


manage_deliveries()

# Start the Tkinter event loop
root.mainloop()
