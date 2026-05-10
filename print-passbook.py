import os
import tkinter as tk
from tkinter import scrolledtext, filedialog, TOP
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import datetime

def generate_passbook():
    passbook_dashboard = tk.Tk()
    passbook_dashboard.title("Passbook Dashboard")
    passbook_dashboard.attributes('-fullscreen', True)
    passbook_dashboard.configure(background="yellow")

    tk.Label(passbook_dashboard, text="Enter your customer ID", font="times 30 bold", background="#023047",
             foreground="white").place(relx=0.050, rely=0.070, relheight=0.100, width=1300)

    tk.Label(passbook_dashboard, text="Customer Id", font="times 30 bold", background="#023047",
             foreground="white").place(relx=0.270, rely=0.4, relheight=0.070, width=400)

    entry_id = tk.Entry(passbook_dashboard, font="times 50 bold", background="#023047", foreground="white")
    entry_id.place(relx=0.570, rely=0.4, relheight=0.070, width=400)

    def fetch_passbook_data(customer_id):
        # Dummy function for fetching transactions
        # You should replace this with the actual database query
        return [
            {'transaction_date': datetime.datetime.now(), 'transaction_type': 'Deposit', 'amount': 1000},
            {'transaction_date': datetime.datetime.now(), 'transaction_type': 'Withdrawal', 'amount': 500}
        ]

    def Passbook():
        customer_id = int(entry_id.get())
        transactions = fetch_passbook_data(customer_id)
        if transactions:
            passbook_text = f"Passbook for Account ID: {customer_id}\n\n"
            passbook_text += "Date            | Withdrawal        | Deposit          | Amount\n"
            passbook_text += "-----------------------------------\n"
            for txn in transactions:
                account_type = txn['transaction_type']
                if account_type == "Deposit":
                    passbook_text += f"{txn['transaction_date'].strftime('%Y-%m-%d')} |                             | {txn['amount']}\n"
                elif account_type == "Withdrawal":
                    passbook_text += f"{txn['transaction_date'].strftime('%Y-%m-%d')} | {txn['amount']}\n"

            text_area = scrolledtext.ScrolledText(passbook_dashboard, wrap=tk.WORD, font="Times 30 bold", bg="cyan2")
            text_area.insert(tk.INSERT, passbook_text)
            text_area.pack(expand=True, fill='both', side=TOP)

            # Adding Print and Save as PDF buttons
            tk.Button(passbook_dashboard, text="Print", font="times 20 bold", command=lambda: print_passbook(passbook_text)).place(relx=0.3, rely=0.85, relheight=0.100, width=200)
            tk.Button(passbook_dashboard, text="Save as PDF", font="times 20 bold", command=lambda: save_as_pdf(passbook_text)).place(relx=0.5, rely=0.85, relheight=0.100, width=200)

        else:
            tk.Label(passbook_dashboard, text="Transactions History\nNo transactions found for this account ID.",
                     font="times 40 bold", background="#023047", foreground="white").place(relx=0.050, rely=0.75, relheight=0.250, width=1300)

    def print_passbook(passbook_text):
        # Print the passbook using the system's print command
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        temp_file.write(passbook_text.encode())
        temp_file.close()
        if os.name == 'nt':  # Windows
            os.startfile(temp_file.name, 'print')
        elif os.name == 'posix':  # macOS/Linux
            os.system(f'lpr {temp_file.name}')
        os.unlink(temp_file.name)

    def save_as_pdf(passbook_text):
        # Open file dialog to save the PDF
        pdf_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if pdf_filename:
            # Create the PDF
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            width, height = letter
            lines = passbook_text.split('\n')
            y = height - 100  # Starting position for text

            # Loop through each line and add to the PDF
            for line in lines:
                c.drawString(100, y, line)
                y -= 20  # Move down the page
                if y < 40:  # If we run out of space, create a new page
                    c.showPage()
                    y = height - 100

            c.save()

    # Passbook button
    tk.Button(passbook_dashboard, text="Generate Passbook", font="times 30 bold", command=Passbook).place(relx=0.5, rely=0.85, relheight=0.100, width=200)

    passbook_dashboard.mainloop()

