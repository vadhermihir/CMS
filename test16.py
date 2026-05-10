import os
import webbrowser
import datetime
import mysql.connector
from reportlab.pdfgen import canvas


def fetch_order_data(consignment_no):
    """Fetches order details from the 'courier_orders' table based on consignment_no."""
    # Replace with your MySQL connection details
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cms"
    )

    cursor = connection.cursor()

    # Fetch all required columns
    cursor.execute("""
        SELECT sender_name, sender_address, sender_contact, receiver_name, receiver_address, 
               receiver_contact, package_type, package_size, package_weight, consignment_no, 
               shipment_types, pickup_date, total_amount, payment_status
        FROM courier_orders WHERE consignment_no = %s
    """, (consignment_no,))

    order_data = cursor.fetchone()
    connection.close()

    if order_data:
        return order_data  # Returns all fetched columns as a tuple
    else:
        print("No order data found!")
        return None


def generateInvoice(order_data):
    """Generates an invoice PDF using the fetched order data."""

    # Unpacking database data
    (s_name, s_add, s_pno, r_name, r_add, r_pno, package_type, package_size, package_weight,
     consignment_no, shipment_types, pickup_date, total_amount, payment_status) = order_data

    company_name = "HK Enterprise"
    address = "123, Sindhubhavan Road"
    city = "Ahmedabad"
    gstNo = "GSTIN123456"
    auSign = "Authorized Signature"
    logo_path = "h1.png"  # Ensure this file exists

    today_date = datetime.date.today().strftime("%d-%m-%Y")

    # Create PDF Canvas
    inv_canvas = canvas.Canvas("Invoice_Generated.pdf", pagesize=(250, 300), bottomup=0)

    # Draw lines and boxes for layout
    inv_canvas.line(5, 50, 245, 50)
    inv_canvas.line(15, 130, 235, 130)
    inv_canvas.line(40, 118, 40, 250)
    inv_canvas.line(140, 118, 140, 250)
    inv_canvas.line(190, 118, 190, 250)
    inv_canvas.line(15, 250, 235, 250)

    # Add company logo
    try:
        inv_canvas.drawImage(logo_path, 15, 5, width=40, height=40)
    except Exception as e:
        print(f"Error loading logo: {e}")

    # Company details
    inv_canvas.setFont("Times-Bold", 10)
    inv_canvas.drawCentredString(140, 20, company_name)
    inv_canvas.setFont("Times-Bold", 5)
    inv_canvas.drawCentredString(140, 30, address)
    inv_canvas.drawCentredString(140, 35, city + ", India")
    inv_canvas.setFont("Times-Bold", 6)
    inv_canvas.drawCentredString(140, 42, "GST No:" + gstNo)
    inv_canvas.setFont("Times-Bold", 8)

    # Sender & Receiver Details
    inv_canvas.setFont("Times-Bold", 6)
    inv_canvas.drawRightString(50, 60, "Sender Name:")
    inv_canvas.drawRightString(70, 60, s_name)
    inv_canvas.drawRightString(50, 70, "Sender Address:")
    inv_canvas.drawRightString(70, 70, s_add)
    inv_canvas.drawRightString(50, 80, "Sender Phone:")
    inv_canvas.drawRightString(82, 80, s_pno)

    inv_canvas.drawRightString(200, 60, "Receiver Name:")
    inv_canvas.drawRightString(215, 60, r_name)
    inv_canvas.drawRightString(200, 70, "Receiver Address:")
    inv_canvas.drawRightString(218, 70, r_add)
    inv_canvas.drawRightString(200, 80, "Receiver Phone:")
    inv_canvas.drawRightString(230, 80, r_pno)

    inv_canvas.drawRightString(52, 100, "Consignment No:")
    inv_canvas.drawRightString(88, 100, consignment_no)

    inv_canvas.drawRightString(50, 90, "Shipment Type:")
    inv_canvas.drawRightString(60, 90, shipment_types)
    inv_canvas.drawRightString(200, 100, "Pickup Date:")
    inv_canvas.drawRightString(230, 100, str(pickup_date))

    # Date
    inv_canvas.drawRightString(230, 90, f"Invoice Date: {today_date}")

    # Table Headers
    inv_canvas.setFont("Times-Bold", 7)
    inv_canvas.drawCentredString(25, 128, "S.No.")
    inv_canvas.drawCentredString(100, 128, "Package Type")
    inv_canvas.drawCentredString(165, 128, "Weight")
    inv_canvas.drawCentredString(215, 128, "Total Amount")

    # Table Data
    y_position = 140

    inv_canvas.drawCentredString(25, y_position, "1")  # Only one row since it's a single order
    inv_canvas.drawCentredString(100, y_position, package_type)
    inv_canvas.drawCentredString(165, y_position, package_weight)
    inv_canvas.drawCentredString(215, y_position, f"{float(total_amount):.2f}")

    # Grand Total
    inv_canvas.drawRightString(232, y_position + 105, f"Total: {float(total_amount):.2f}")

    # Authorized Signature
    inv_canvas.drawRightString(230, 270, auSign)
    inv_canvas.drawRightString(216, 280, "HKmaheta")

    inv_canvas.showPage()
    inv_canvas.save()

    print("Invoice generated successfully as 'Invoice_Generated.pdf'")

    # Open the generated PDF on Windows
    pdf_path = os.path.abspath("Invoice_Generated.pdf")
    if os.name == "nt":  # Check if running on Windows
        os.startfile(pdf_path)  # Opens the PDF in default viewer
    else:
        webbrowser.open(f"file://{pdf_path}")  # Fallback for non-Windows OS


# Directly calling the functions without `if __name__ == "__main__"`
consignment_no = "I417A7SZ4W"  # Replace with actual consignment number
order_data = fetch_order_data(consignment_no)

if order_data:
    generateInvoice(order_data)
