import random
import string
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from tkcalendar import Calendar

# ---------------- Database Connection ---------------- #
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cms"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# ---------------- Generate Random Consignment No ---------------- #
def generate_random_consignment_no():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# ---------------- Track Order Function ---------------- #
def track_order():
    consignment_no = consignment_no_entry.get().strip()

    if not consignment_no:
        messagebox.showwarning("Input Error", "Please enter a consignment number!")
        return

    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT consignment_no FROM courier_orders WHERE consignment_no = %s", (consignment_no,))
            order = cursor.fetchone()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching data: {err}")
            order = None
        finally:
            cursor.close()
            conn.close()

        if order:
            messagebox.showinfo("Order Found", f"📦 Consignment No: {order[0]}\nYour order exists in our database.")
        else:
            messagebox.showerror("Not Found", "No order found with this consignment number.")

# ---------------- Initialize Tkinter Window ---------------- #
root = tk.Tk()
root.attributes("-fullscreen", True)
root.title("Track Tour Order")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# ---------------- Show Main Form ---------------- #
def show_main_form():
    global consignment_no_entry  # Make the entry field accessible globally

    # Clear the window (removes previous content)
    for widget in root.winfo_children():
        widget.destroy()

    # Load and resize background image to fit the full screen
    bg_image_path = "c8.jpg"  # Ensure this image exists
    try:
        bg_image = Image.open(bg_image_path)
        bg_image_resized = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        bg_image_tk = ImageTk.PhotoImage(bg_image_resized)
    except Exception as e:
        messagebox.showerror("Image Error", f"Could not load background image.\nError: {e}")
        return

    # Create a canvas for the background image
    canvas = ctk.CTkCanvas(root, width=screen_width, height=screen_height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)
    canvas.image = bg_image_tk  # Prevent garbage collection

    # Welcome Label
    welcome_label = ctk.CTkLabel(
        root,
        text="Welcome To Tracking Page",
        font=("Copperplate Gothic Bold", 36, "bold"),
        text_color="white",
        fg_color="black",
        width=screen_width,
        height=100
    )
    welcome_label.place(relx=0.5, rely=0.1, anchor="center")

    # Main Tracking Frame
    frame = ctk.CTkFrame(root, fg_color="#FFC736", width=screen_width * 0.5, height=screen_height * 0.5, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Title Label
    title_label = ctk.CTkLabel(frame, text="Track Tour Order", font=("Copperplate Gothic Bold", 28), text_color="black")
    title_label.pack(pady=(20, 10))

    # Input Field
    consignment_no_label = ctk.CTkLabel(frame, text="Enter Consignment Number:", font=("Copperplate Gothic Bold", 18), text_color="black")
    consignment_no_label.pack(pady=(10, 5))

    consignment_no_entry = ctk.CTkEntry(frame, font=("Copperplate Gothic Bold", 16), text_color="black", fg_color="white", width=300)
    consignment_no_entry.pack(pady=(0, 15))

    # Submit Button
    submit_button = ctk.CTkButton(
        frame, text="Track Order", font=("Copperplate Gothic Bold", 18), text_color="black",
        fg_color="#3B8ED0", hover_color="#D65C07", command=track_order
    )
    submit_button.pack(pady=20)

    # Exit Button
    exit_button = ctk.CTkButton(
        frame, text="Exit", font=("Copperplate Gothic Bold", 18), text_color="white",
        fg_color="red", hover_color="#D65C07", command=root.quit
    )
    exit_button.pack(pady=10)

# Run the main form
show_main_form()
root.mainloop()
