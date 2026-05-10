from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors


def generate_invoice():
    pdf_file = "Invoice.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)
    width, height = A4

    # Add Header Background
    c.setFillColor(colors.HexColor("#FFC107"))
    c.rect(0, height - 150, width, 100, fill=True, stroke=False)

    # Add Logo/Icon
    logo_path = "h1.png"  # Ensure the file exists
    logo = ImageReader(logo_path)
    c.drawImage(logo, 50, height - 110, 80, 40, mask='auto')

    # Invoice Title
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(150, height - 90, "INVOICE")

    # Company & Contact Details
    c.setFont("Helvetica", 12)
    c.drawString(450, height - 70, "647-444-1234")
    c.drawString(450, height - 85, "your@email.com")
    c.drawString(450, height - 100, "yourwebsite.com")

    # Client & Invoice Details
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 160, "Billed To")
    c.drawString(300, height - 160, "Invoice Number")
    c.drawString(450, height - 160, "Invoice Total")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 175, "Client Name")
    c.drawString(50, height - 190, "1 Client Address")
    c.drawString(50, height - 205, "City, State, Country")
    c.drawString(50, height - 220, "ZIP CODE")

    c.drawString(300, height - 175, "000000")
    c.drawString(300, height - 190, "Date Of Issue")
    c.drawString(300, height - 205, "10/07/14")

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#FFC107"))
    c.drawString(450, height - 175, "$4520.00")

    # Table Headers
    c.setFillColor(colors.HexColor("#FFC107"))
    c.rect(50, height - 260, 500, 25, fill=True, stroke=False)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, height - 250, "Description")
    c.drawString(230, height - 250, "Unit Cost")
    c.drawString(340, height - 250, "Qty / Hr Rate")
    c.drawString(450, height - 250, "Amount")

    # Items
    c.setFont("Helvetica", 12)
    items = [
        ("Your Item Name", "$1000", "1", "$1000"),
        ("Your Item Name", "$1000", "1", "$1000"),
        ("Your Item Name", "$1000", "1", "$1000"),
        ("Your Item Name", "$1000", "1", "$1000"),
    ]
    y = height - 280
    for desc, unit_cost, qty, amount in items:
        c.drawString(60, y, desc)
        c.drawString(230, y, unit_cost)
        c.drawString(340, y, qty)
        c.drawString(450, y, amount)
        y -= 20

    # Totals
    c.setFont("Helvetica-Bold", 12)
    c.drawString(340, y - 30, "Subtotal:")
    c.drawString(450, y - 30, "$4000.00")
    c.drawString(340, y - 50, "Tax:")
    c.drawString(450, y - 50, "$520.00")

    # Save PDF
    c.save()
    print(f"Invoice saved as {pdf_file}")


generate_invoice()
