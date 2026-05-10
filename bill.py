import mysql.connector
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import qrcode
print(dir(qrcode))

# Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "cms"
}


# Fetch data from MySQL
def get_courier_data(courier_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM orders WHERE courier_id = %s"
        cursor.execute(query, (courier_id,))
        data = cursor.fetchone()

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


# Generate Courier Slip PDF
def create_courier_slip(courier_id):
    data = get_courier_data(courier_id)
    if not data:
        print("No data found for this courier ID.")
        return

    pdf_filename = f"courier_slip_{courier_id}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=A4)

    # Add company logo (optional)
    logo_path = "i1.png"  # Change to your logo path
    try:
        logo = ImageReader(logo_path)
        c.drawImage(logo, 40, 770, width=100, height=50)  # Adjust size
    except:
        print("⚠️ Logo not found, skipping.")

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(180, 780, "Courier Service - Delivery Slip")

    # QR Code for Tracking
    qr_path = generate_qr_code(data["consignment_no"])
    c.drawImage(qr_path, 450, 730, width=80, height=80)

    # Draw Border
    c.setStrokeColor(colors.black)
    c.rect(30, 90, 530, 660)  # Main border

    # Sender & Receiver Info
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 710, "Sender Information:")
    c.drawString(300, 710, "Receiver Information:")

    c.setFont("Helvetica", 11)
    sender_details = [
        f"Name: {data['sender_name']}",
        f"Address: {data['sender_address']}",
        f"Contact: {data['sender_contact']}"
    ]

    receiver_details = [
        f"Name: {data['receiver_name']}",
        f"Address: {data['receiver_address']}",
        f"Contact: {data['receiver_contact']}"
    ]

    y_position = 690
    for sender, receiver in zip(sender_details, receiver_details):
        c.drawString(40, y_position, sender)
        c.drawString(300, y_position, receiver)
        y_position -= 20

    # Package Details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 630, "Package Details:")

    c.setFont("Helvetica", 11)
    package_details = [
        ("Consignment No", data["consignment_no"]),
        ("Package Type", data["package_type"]),
        ("Package Size", data["package_size"]),
        ("Package Weight", f"{data['package_weight']} kg"),
        ("Shipment Type", data["shipment_types"]),
        ("Pickup Date", data["pickup_date"]),
        ("Total Amount", f"${data['total_amount']}"),
        ("Delivery Status", data["payment_status"])
    ]

    y_position = 610
    for label, value in package_details:
        c.drawString(40, y_position, f"{label}:")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(200, y_position, str(value))
        c.setFont("Helvetica", 11)
        y_position -= 20

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(40, 100, "Thank you for choosing our courier service. Have a great day!")

    # Save PDF
    c.save()
    print(f"✅ Courier slip generated: {pdf_filename}")


# Example Usage
create_courier_slip(1)  # Replace with actual courier ID
