from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_courier_invoice():
    pdf_file = "Courier_Invoice.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "COURIER MANAGEMENT INVOICE")
    c.setFont("Helvetica", 12)
    c.drawString(400, height - 50, "Invoice #: 001")
    c.drawString(400, height - 70, "Date: 10/07/14")

    # Sender & Receiver Info
    c.drawString(50, height - 100, "Sender:")
    c.drawString(50, height - 120, "John Doe")
    c.drawString(50, height - 140, "123 Street, City, Country")
    c.drawString(50, height - 160, "ZIP CODE")

    c.drawString(300, height - 100, "Receiver:")
    c.drawString(300, height - 120, "Jane Smith")
    c.drawString(300, height - 140, "456 Avenue, City, Country")
    c.drawString(300, height - 160, "ZIP CODE")

    # Table Headers
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 200, "Description")
    c.drawString(300, height - 200, "Weight (kg)")
    c.drawString(400, height - 200, "Distance (km)")
    c.drawString(500, height - 200, "Amount")
    c.line(50, height - 205, 550, height - 205)

    # Items
    c.setFont("Helvetica", 12)
    items = [("Parcel 1", 5, 100, 50.00), ("Parcel 2", 10, 200, 100.00)]
    y = height - 230
    subtotal = 0
    for desc, weight, distance, amount in items:
        subtotal += amount
        c.drawString(50, y, desc)
        c.drawString(300, y, str(weight))
        c.drawString(400, y, str(distance))
        c.drawString(500, y, f"${amount:.2f}")
        y -= 20

    # Totals
    tax = subtotal * 0.10  # 10% tax
    total = subtotal + tax
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, y - 20, "Subtotal:")
    c.drawString(500, y - 20, f"${subtotal:.2f}")
    c.drawString(400, y - 40, "Tax (10%):")
    c.drawString(500, y - 40, f"${tax:.2f}")
    c.drawString(400, y - 60, "Total:")
    c.drawString(500, y - 60, f"${total:.2f}")

    c.save()
    print(f"Courier Invoice saved as {pdf_file}")


generate_courier_invoice()
