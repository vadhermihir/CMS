import os
import webbrowser
import datetime
from reportlab.pdfgen import canvas


def generateInvoice(s_name, s_add, s_pno, r_name, r_add, r_pno, orders):
    company_name = "HK Enterprise"
    address = "123, Sindhubhavan Road"
    city = "Ahmedabad"
    gstNo = "GSTIN123456"
    auSign = "Authorized Signature"
    logo_path = "h2.jpg"  # Ensure this file exists

    today_date = datetime.date.today().strftime("%d-%m-%Y")

    # Create PDF Canvas
    inv_canvas = canvas.Canvas("Invoice_Generated.pdf", pagesize=(220, 280), bottomup=0)

    # Draw lines and boxes for layout
    inv_canvas.line(5, 50, 215, 50)
    inv_canvas.line(15, 130, 205, 130)
    inv_canvas.line(40, 118, 40, 250)
    inv_canvas.line(130, 118, 130, 250)
    inv_canvas.line(160, 118, 160, 250)
    inv_canvas.line(185, 118, 185, 250)
    inv_canvas.line(15, 250, 205, 250)

    # Add company logo
    try:
        inv_canvas.drawImage(logo_path, 15, 5, width=40, height=40)
    except Exception as e:
        print(f"Error loading logo: {e}")

    # Company Details
    inv_canvas.setFont("Times-Bold", 10)
    inv_canvas.drawCentredString(130, 20, company_name)
    inv_canvas.setFont("Times-Roman", 6)
    inv_canvas.drawCentredString(130, 30, address)
    inv_canvas.drawCentredString(130, 35, city + ", India")
    inv_canvas.drawCentredString(130, 42, "GST No: " + gstNo)

    # Sender & Receiver Details
    inv_canvas.setFont("Times-Bold", 6)
    inv_canvas.drawRightString(50, 60, "Sender:")
    inv_canvas.drawRightString(100, 60, s_name)
    inv_canvas.drawRightString(50, 70, "Address:")
    inv_canvas.drawRightString(100, 70, s_add)
    inv_canvas.drawRightString(50, 80, "Phone:")
    inv_canvas.drawRightString(100, 80, s_pno)

    inv_canvas.drawRightString(150, 60, "Receiver:")
    inv_canvas.drawRightString(200, 60, r_name)
    inv_canvas.drawRightString(150, 70, "Address:")
    inv_canvas.drawRightString(200, 70, r_add)
    inv_canvas.drawRightString(150, 80, "Phone:")
    inv_canvas.drawRightString(200, 80, r_pno)

    # Date
    inv_canvas.drawRightString(200, 90, f"Date: {today_date}")

    # Table Headers
    inv_canvas.setFont("Times-Bold", 7)
    inv_canvas.drawCentredString(25, 128, "S.No.")
    inv_canvas.drawCentredString(85, 128, "Orders")
    inv_canvas.drawCentredString(145, 128, "Price")
    inv_canvas.drawCentredString(172, 128, "Weight.")
    inv_canvas.drawCentredString(195, 128, "Total")

    # Table Data
    y_position = 140
    total_amount = 0

    for index, order in enumerate(orders, start=1):
        item_name, price, qty = order
        total_price = price * qty
        total_amount += total_price

        inv_canvas.drawCentredString(25, y_position, str(index))
        inv_canvas.drawCentredString(85, y_position, item_name)
        inv_canvas.drawCentredString(145, y_position, f"{price:.2f}")
        inv_canvas.drawCentredString(172, y_position, str(qty))
        inv_canvas.drawCentredString(195, y_position, f"{total_price:.2f}")

        y_position += 10

    # Total Amount
    inv_canvas.drawRightString(195, y_position + 10, f"Total: ₹{total_amount:.2f}")

    # Authorized Signature
    inv_canvas.drawRightString(200, 270, auSign)
    inv_canvas.drawRightString(200, 275, "HKmaheta")

    inv_canvas.showPage()
    inv_canvas.save()

    print("Invoice generated successfully as 'Invoice_Generated.pdf'")

    # Open the generated PDF on Windows
    pdf_path = os.path.abspath("Invoice_Generated.pdf")
    if os.name == "nt":  # Check if running on Windows
        os.startfile(pdf_path)  # Opens the PDF in default viewer
    else:
        webbrowser.open(f"file://{pdf_path}")  # Fallback for non-Windows OS


if __name__ == "__main__":
    # Example order list: [(Item name, Price, Quantity)]
    orders = [("Laptop", 450, 1), ("Mouse", 500, 2), ("Keyboard", 120, 1)]
    generateInvoice("John Doe", "Jetpur", "9876543210", "Marry", "Rajkot", "9876543210", orders)
