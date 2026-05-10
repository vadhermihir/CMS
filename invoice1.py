from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import mysql.connector
from datetime import datetime


def generate_invoice_pdf(consignment_no):
    # Connect to MySQL Database
    conn = mysql.connector.connect(host="localhost", user="root", password="",
                                   database="cms")
    cursor = conn.cursor(dictionary=True)

    # Fetch Order Details
    cursor.execute("SELECT * FROM courier_orders WHERE consignment_no = %s", (consignment_no,))
    order = cursor.fetchone()

    if not order:
        print("No order found with consignment number:", consignment_no)
        return

    # File Name for PDF
    pdf_filename = f"Invoice_{order['consignment_no']}.pdf"

    # Create a PDF canvas
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 50, "TAX INVOICE")

    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0, 0.5, 0)  # Green Color
    c.drawCentredString(width / 2, height - 75, "HK Enterprises")

    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0, 0, 0)  # Black Color
    c.drawCentredString(width / 2, height - 95, "M.G.Road, Opp.Garden, Jetpur 360370")

    # Business Details
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, height - 120, "Phone: +91 8733010200")
    c.drawString(40, height - 140, f"Shipment Type: {order['shipment_types']}")
    c.drawCentredString(width / 2, height - 140, "GSTIN: 24AALCR2857A1ZD")
    c.drawRightString(width - 40, height - 120, f"Date: {datetime.now().strftime('%d-%m-%Y')}")
    c.drawRightString(width - 40, height - 140, f"Consignment No: {order['consignment_no']}")

    # Sender & Receiver Details
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, height - 170, "Sender:")
    c.setFont("Helvetica", 10)
    c.drawString(100, height - 170, f"{order['sender_name']}")
    c.drawString(100, height - 185, f"Address: {order['sender_address']}")
    c.drawString(100, height - 200, f"Contact: {order['sender_contact']}")

    c.setFont("Helvetica-Bold", 10)
    c.drawString(350, height - 170, "Receiver:")
    c.setFont("Helvetica", 10)
    c.drawString(420, height - 170, f"{order['receiver_name']}")
    c.drawString(420, height - 185, f"Address: {order['receiver_address']}")
    c.drawString(420, height - 200, f"Contact: {order['receiver_contact']}")

    # Table Headers
    c.setFont("Helvetica-Bold", 10)
    y_start = height - 230
    c.drawString(40, y_start, "Sr. No.")
    c.drawString(120, y_start, "Package Type")
    c.drawString(300, y_start, "Weight")
    c.drawString(450, y_start, "Amount")

    # Table Rows
    c.setFont("Helvetica", 10)
    y_position = y_start - 20
    c.drawString(40, y_position, "1")
    c.drawString(120, y_position, order["package_type"])
    c.drawString(300, y_position, f"{order['package_weight']} kg")
    c.drawString(450, y_position, f"₹{order['total_amount']}")

    # Footer (Subtotal, GST, and Grand Total)
    subtotal = float(order["total_amount"])
    gst = round(subtotal * 0.18, 2)
    grand_total = subtotal + gst

    y_footer = y_position - 50
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(width - 40, y_footer, f"Subtotal: ₹{subtotal}")
    c.drawRightString(width - 40, y_footer - 20, f"GST (18%): ₹{gst}")
    c.drawRightString(width - 40, y_footer - 40, f"Grand Total: ₹{grand_total}")

    # Terms & Conditions
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y_footer - 80, "Terms & Conditions:")
    c.setFont("Helvetica", 10)
    terms = [
        "1. Customer will pay the GST.",
        "2. Customer will pay the delivery charges.",
        "3. Pay the due amount within 15 days."
    ]
    for i, term in enumerate(terms):
        c.drawString(60, y_footer - 100 - (i * 15), term)

    # Authorized Signatory
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(width - 40, y_footer - 160, "Authorized Signatory")
    c.drawRightString(width - 40, y_footer - 180, "HK Enterprises")

    # Save PDF
    c.save()
    print(f"Invoice saved as {pdf_filename}")

    # Close DB Connection
    cursor.close()
    conn.close()


# Example Usage
generate_invoice_pdf("IR7XAZDKL0")
