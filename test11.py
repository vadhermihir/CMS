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
    global consignment_no_entry  # Make it accessible in track_order()

    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Load and resize background image
    bg_image_path = "c8.jpg"
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
        root, text="Welcome To Tracking Page", font=("Copperplate Gothic Bold", 36, "bold"),
        text_color="white", bg_color="black", width=screen_width, height=100
    )
    welcome_label.place(relx=0.5, rely=0.1, anchor="center")

    # Main Frame
    frame = ctk.CTkFrame(root, fg_color="#FFC736", width=screen_width * 0.7, height=screen_height * 0.9, corner_radius=0)
    frame.place(relx=0.7, rely=0.5, anchor="center")

    # Title Label
    title_label = ctk.CTkLabel(frame, text="Track Tour Order", font=("Copperplate Gothic Bold", 32, "bold"), text_color="black")
    title_label.grid(row=0, column=0, columnspan=2, pady=(20, 30))

    # Sender Details Section
    sender_frame = ctk.CTkFrame(frame, width=screen_width * 0.6, height=300, fg_color="#3B8ED0", corner_radius=10)
    sender_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

    consignment_no_label = ctk.CTkLabel(sender_frame, text="Enter Consignment number:", font=("Copperplate Gothic Bold", 18),
                                        fg_color="#3B8ED0", text_color="white")
    consignment_no_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    consignment_no_entry = ctk.CTkEntry(sender_frame, font=("Copperplate Gothic Bold", 16), text_color="black", fg_color="white")
    consignment_no_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    # Submit Button (✅ Fixed command)
    submit_button = ctk.CTkButton(frame, text="Track Order", font=("Copperplate Gothic Bold", 18), text_color="black",
                                  fg_color="#3B8ED0", hover_color="#D65C07", command=track_order)
    submit_button.grid(row=5, column=0, columnspan=2, pady=30)

    # Exit Button
    exit_button = ctk.CTkButton(frame, text="Exit", font=("Copperplate Gothic Bold", 18), text_color="white",
                                fg_color="red", hover_color="#D65C07", command=root.quit)
    exit_button.grid(row=6, column=0, columnspan=2, pady=5)

show_main_form()
root.mainloop()
