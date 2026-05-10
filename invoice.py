import tkinter as tk

def generate_invoice():
    root = tk.Tk()
    root.title("Tax Invoice")
    root.state("zoomed")  # Maximize the window to fit the screen

    canvas = tk.Canvas(root, width=794, height=1123, bg="white")
    canvas.pack()

    # Draw Border
    canvas.create_rectangle(10, 10, 784, 1113, outline="black", width=2)

    # Header
    canvas.create_text(397, 30, text="TAX INVOICE", font=("Arial", 12, "bold"), anchor="center")
    canvas.create_text(397, 60, text="HK Enterprises", font=("Arial", 18, "bold"), fill="green", anchor="center")
    canvas.create_text(397, 85, text="M.G.Road, Opp.Garden, Jetpur 360370", font=("Arial", 10), anchor="center")

    # Business Details
    canvas.create_text(50, 90, text="Phone: +91 8733010200", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(50, 110, text="Shipment type: Air", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(397, 110, text="GSTIN: 24AALCR2857A1ZD", font=("Arial", 9, "bold"), anchor="center")
    canvas.create_text(730, 90, text="Date: 09-07-2005", font=("Arial", 9, "bold"), anchor="e")
    canvas.create_text(744, 110, text="Consignment No: AVHPC9999A", font=("Arial", 9, "bold"), anchor="e")

    # Bill To & Invoice Details
    canvas.create_rectangle(20, 130, 774, 200, outline="black", width=2)
    canvas.create_text(50, 145, text="Sender Name : -", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(145, 145, text="Prit Gohel", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(50, 165, text="Sender Address : -", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(160, 165, text="Jetpur", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(50, 185, text="Sender Number : -", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(155, 185, text="9925544663", font=("Arial", 9, "bold"), anchor="w")

    canvas.create_text(500, 145, text="Receiver Name : -", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(600, 145, text="Harshil Maheta", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(500, 165, text="Receiver Address : -", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(618, 165, text="Ahmadavad", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(500, 185, text="Receiver Number : -", font=("Arial", 9, "bold"), anchor="w")
    canvas.create_text(615, 185, text="9265010050", font=("Arial", 9, "bold"), anchor="w")

    # Table Headers
    canvas.create_rectangle(20, 200, 774, 230, fill="green", outline="black", width=2)
    headers = ["Sr. No.", "Package Type", "Weight", "Amount"]
    x_positions = [45, 220, 470, 670]  # Adjusted for better spacing

    for i, header in enumerate(headers):
        canvas.create_text(x_positions[i], 215, text=header, font=("Arial", 10, "bold"), fill="white", anchor="center")

    # Sample Data for Invoice Rows
    invoice_data = [
        (1, "Electronics", "2 kg", "₹1500"),
        (2, "Clothing", "1.5 kg", "₹800"),
        (3, "Documents", "0.5 kg", "₹300"),
        (4, "Furniture", "10 kg", "₹2500"),
        (5, "Fragile Items", "3 kg", "₹1800"),
        (6, "Books", "4 kg", "₹1200"),
        (7, "Toys", "2.5 kg", "₹900"),
        (8, "Food Items", "3.5 kg", "₹1100"),
    ]

    # Table Rows
    y_start = 230
    row_height = 30

    for i, (sr_no, package, weight, amount) in enumerate(invoice_data):
        y = y_start + (i * row_height)

        # Row Borders
        canvas.create_rectangle(20, y, 774, y + row_height, outline="black", width=1)

        # Column Borders
        canvas.create_line(70, y, 70, y + row_height, fill="black", width=1)  # Sr. No.
        canvas.create_line(370, y, 370, y + row_height, fill="black", width=1)  # Package Type
        canvas.create_line(570, y, 570, y + row_height, fill="black", width=1)  # Weight

        # Fill in the data (center-aligned)
        canvas.create_text(45, y + 15, text=str(sr_no), font=("Arial", 9), anchor="center")
        canvas.create_text(220, y + 15, text=package, font=("Arial", 9), anchor="center")
        canvas.create_text(470, y + 15, text=weight, font=("Arial", 9), anchor="center")
        canvas.create_text(670, y + 15, text=amount, font=("Arial", 9), anchor="center")

    # Footer (Amount Details)
    canvas.create_rectangle(20, 500, 774, 580, outline="black", width=2)
    canvas.create_text(600, 515, text="Subtotal:", font=("Arial", 10, "bold"), anchor="w")
    canvas.create_text(705, 515, text="₹10100", font=("Arial", 10, "bold"), anchor="e")
    canvas.create_text(600, 535, text="GST (18%):", font=("Arial", 10, "bold"), anchor="w")
    canvas.create_text(707, 535, text="₹1818", font=("Arial", 10, "bold"), anchor="e")
    canvas.create_text(600, 555, text="Grand Total:", font=("Arial", 10, "bold"), anchor="w")
    canvas.create_text(725, 555, text="₹11918", font=("Arial", 10, "bold"), anchor="e")

    # Terms & Conditions
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

generate_invoice()
