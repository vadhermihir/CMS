import mysql.connector
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import qrcode

# Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "cms"
}

# Fetch all courier transactions for a courier_id
def get_all_courier_data(courier_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Query updated to fetch relevant details for the courier based on courier_id
        query = "SELECT * FROM orders WHERE courier_id = %s"
        cursor.execute(query, (courier_id,))
        data = cursor.fetchall()

        cursor.close()
        conn.close()
        return data
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return None

# Generate QR Code for tracking
def generate_qr_code(consignment_number):
    qr = qrcode.QRCode(box_size=5, border=2)
    qr.add_data(f"Tracking Number: {consignment_number}")
    qr.make(fit=True)

    qr_img = qr.make_image(fill="black", back_color="white")
    qr_img_path = f"h1{consignment_number}.png"
    qr_img.save(qr_img_path)
    return qr_img_path

# Generate Courier Passbook PDF
def create_courier_passbook(courier_id):
    data = get_all_courier_data(courier_id)
    if not data:
        print("No shipments found for this courier ID.")
        return

    pdf_filename = f"courier_passbook_{courier_id}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=A4)

    # Add company logo (optional)
    logo_path = "i1.png"  # Change to your logo path
    try:
        logo = ImageReader(logo_path)
        c.drawImage(logo, 40, 770, width=100, height=50)
    except:
        print("⚠️ Logo not found, skipping.")

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(180, 780, f"Courier Passbook - Courier ID: {courier_id}")

    # Draw Border
    c.setStrokeColor(colors.black)
    c.rect(30, 80, 530, 690)  # Main border

    # Table Header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 730, "Pickup Date")
    c.drawString(180, 730, "Consignment No")
    c.drawString(320, 730, "Package Type")
    c.drawString(460, 730, "Amount")

    c.line(30, 720, 560, 720)  # Line separator

    # Table Content
    c.setFont("Helvetica", 11)
    y_position = 700

    for order in data:
        if y_position < 100:
            c.showPage()
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, 730, "Pickup Date")
            c.drawString(180, 730, "Consignment No")
            c.drawString(320, 730, "Package Type")
            c.drawString(460, 730, "Amount")
            c.line(30, 720, 560, 720)
            y_position = 700

        c.setFont("Helvetica", 11)
        c.drawString(40, y_position, str(order["pickup_date"]))  # Convert date to string
        c.drawString(180, y_position, order["consignment_no"])
        c.drawString(320, y_position, order["package_type"])
        c.drawString(460, y_position, f"${order['total_amount']}")

        y_position -= 20

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(40, 90, "Thank you for choosing our courier service!")

    # Save PDF
    c.save()
    print(f"✅ Courier passbook generated: {pdf_filename}")

# Example Usage
courier_id = 1  # Replace with actual courier ID
create_courier_passbook(courier_id)
