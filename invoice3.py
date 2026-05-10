import os
import datetime
from fpdf import FPDF
from tkinter import messagebox

# pdf
def save_as_pdf():
    class PDF(FPDF):
        def header(self):
            # Set background color for header
            self.set_fill_color(200, 200, 200)  # Light gray background
            self.rect(5, 5, 200, 30, 'F')  # Header rectangle (x, y, width, height, style 'F' for fill)

            # Set logo
            try:
                self.image("h1.png", 10, 8, 33)  # Logo position (x, y) and width
            except Exception:
                self.set_font("Arial", "I", 12)
                self.cell(0, 10, "Logo not found", 0, 1, "L")

            # Title
            self.set_font("Arial", "B", 16)
            self.set_text_color(0, 0, 0)  # Black text color
            self.cell(80)  # Center alignment
            self.cell(30, 10, "HK Enterprise", border=False, ln=True, align="C")

            # Address and Contact
            self.set_font("Arial", "", 10)
            self.cell(0, 6, "M.g.road, opp.Garden, nr.civil hospital Jetpur-360370", ln=True, align="C")
            self.cell(0, 6, "Contact: 8733010200 | GST NO: 24AAAAA12345ZZF", ln=True, align="C")
            self.ln(5)  # Add spacing

        def footer(self):
            # Footer background
            self.set_fill_color(200, 200, 200)  # Light gray
            self.rect(5, self.h - 20, 190, 15, 'F')  # Footer rectangle (x, y, width, height, style 'F')

            # Page number
            self.set_y(-15)  # Position 1.5 cm from bottom
            self.set_font("Arial", "I", 8)
            self.set_text_color(0, 0, 0)  # Black text color
            self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def draw_uniform_border(pdf, x, y, width, height):
        """Draw a uniform border with fixed height and width."""
        pdf.rect(x, y, width, height)

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Invoice Details Section
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Invoice Details", ln=True, align="C")  # Title centered
    pdf.cell(0, 8, f"Invoice Date: {datetime.date.today().strftime('%d-%m-%Y')}", ln=True)
    pdf.ln(2)

    # Uniform Border for Invoice Details
    border_x = 10
    border_y = pdf.get_y()
    border_width = 190
    border_height = 25
    draw_uniform_border(pdf, border_x, border_y, border_width, border_height)

    # Add Invoice Details Content
    pdf.set_font("Arial", "", 10)

    # Row 1: Customer Name and Invoice Number
    pdf.cell(95, 6, f"Customer Name: Harshil Maheta", ln=False)  # Left column
    pdf.cell(100, 6, f"Receiver Name:Prit gohel", ln=True)  # Right column

    # Row 2: Address and Invoice Date
    pdf.cell(95, 6, f"Customer Contact: 8733010200", ln=False)  # Left column
    pdf.cell(100, 6, f"Receiver contact:9924455641", ln=True)

    # Row 3: City and State
    pdf.cell(95,6,f"Shipment Type: Air ",ln=False)
    pdf.cell(100, 6, f"Reciever Address: Surat", ln=True)  # Full row

    # Row 4: Contact Information
    pdf.cell(95, 6, f"Pickup Date:09-07-2005", ln=False)
    pdf.cell(100, 6, f"Consignment Number: xxxxxxxx", ln=True)

    # Add spacing after the rows
    pdf.ln(10)

    # Table Header
    pdf.set_font("Arial", "B", 10)
    columns = ["Nos.", "Package Type", "Weight", "Total Price"]
    column_widths = [10, 100, 40, 40]
    for col_name, col_width in zip(columns, column_widths):
        pdf.cell(col_width, 8, col_name, 1, 0, "C")
    pdf.ln()

    # Example product data
    items = [
        ("Apple","20gram", 40.0),
        ("Banana","15gram", 15.0),
        ("Orange","30gram", 30.0)
    ]

    # Table Rows
    pdf.set_font("Arial", "", 10)
    subtotal = 0
    for row_index, item in enumerate(items, start=1):
        pdf.cell(column_widths[0], 8, str(row_index), 1, 0, "C")
        pdf.cell(column_widths[1], 8, item[0], 1, 0, "L")  # Product name
        pdf.cell(column_widths[2], 8, f"{item[1]}", 1, 0, "R")  # Price per item
        pdf.cell(column_widths[3], 8, f"{item[2]:.2f}", 1, 0, "R")  # Total price
        pdf.ln()
        subtotal += item[2]

    # Summary Section
    border_x = 10
    border_y = pdf.get_y()
    border_width = 190
    border_height = 25
    draw_uniform_border(pdf, border_x, border_y, border_width, border_height)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, f"Subtotal: {subtotal:.2f}", ln=True, align="R")  # Subtotal
    pdf.cell(0, 6, f"GST (18%): {subtotal * 0.18:.2f}", ln=True, align="R")  # GST
    pdf.cell(0, 6, f"Grand Total: {subtotal * 1.18:.2f}", ln=True, align="R")  # Grand Total

    # Terms and Conditions Section
    border_x = 10
    border_y = pdf.get_y()
    border_width = 190
    border_height = 40
    draw_uniform_border(pdf, border_x, border_y, border_width, border_height)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 10)

    # Left Column: Terms and Conditions
    pdf.cell(95, 6, "Terms and Conditions:", border=0, ln=0, align="L")  # Half the page width
    pdf.cell(95, 6, "HK Enterprise          ", border=0, ln=1, align="R")  # Second half (right column)

    # Additional Details
    pdf.set_font("Arial", "", 8)
    pdf.cell(95, 6, "1. Customer will pay the GST.", border=0, ln=0, align="L")
    pdf.cell(95, 6, "Authorized", border=0, ln=1, align="R")  # Align right for "Authorized"
    pdf.cell(95, 6, "2. Customer will pay the delivery charges.", border=0, ln=1, align="L")

    # Add more terms as needed below
    pdf.cell(95, 6, "3. Prices are subject to change without notice.", border=0, ln=1, align="L")
    pdf.cell(95, 6, "4. Pay the due amount within 15 days.", border=0, ln=1, align="L")

    folder_name = "invoice"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Save PDF
    file_name = f"Invoice_number.pdf"
    file_path = os.path.join(folder_name, file_name)
    pdf.output(file_path)
    messagebox.showinfo("Success", f"PDF generated: {file_path}")

# Call save_as_pdf function to generate the invoice
save_as_pdf()
