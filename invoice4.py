import mysql.connector
from fpdf import FPDF
import datetime
import os
from tkinter import messagebox

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

# Call generate_invoice_pdf function with consignment_no
consignment_no = "68RI9F6UYB"  # Example consignment number
generate_invoice_pdf(consignment_no)
