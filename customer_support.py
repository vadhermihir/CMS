import tkinter as tk
from tkinter import messagebox
import mysql.connector
import customtkinter as ctk
from PIL import Image, ImageTk

def submit_query():
    name = your_name_entry.get().strip()
    email = your_email_entry.get().strip()
    query = your_query_entry.get().strip()

    if not name or not email or not query:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cms"
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customer_queries (user_name, user_email, user_query) VALUES (%s, %s, %s)", (name, email, query))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Your query has been submitted successfully!")

        # Clear fields after submission
        your_name_entry.delete(0, tk.END)
        your_email_entry.delete(0, tk.END)
        your_query_entry.delete(0, tk.END)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Initialize Tkinter window
root = tk.Tk()
root.attributes("-fullscreen", True)
root.title("Customer Support")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set up background image
bg_image_path = "images/c4.jpg"
bg_image = Image.open(bg_image_path)
bg_image_resized = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
bg_image_tk = ImageTk.PhotoImage(bg_image_resized)

canvas = ctk.CTkCanvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)
canvas.image = bg_image_tk

# Frame for the form
frame = ctk.CTkFrame(root, fg_color="#FFC736", width=0, height=0, corner_radius=0)
frame.place(relx=0.7, rely=0.5, anchor="center")

# Title Label
title_label = ctk.CTkLabel(frame, text="Customer Support", font=("Copperplate Gothic Bold", 32, "bold"), text_color="black")
title_label.grid(row=0, column=0, columnspan=2, pady=(20, 30))

# Welcome Label
font_size = int(screen_height * 0.05)
welcome_label = ctk.CTkLabel(root, text="Customer Support Page!", font=("Copperplate Gothic Bold", font_size, "bold"), text_color="white", bg_color="black", width=screen_width, height=70)
welcome_label.place(relx=0.5, rely=0.1, anchor="center")

# Form Frame
sender_frame = ctk.CTkFrame(frame,width=800,height=300, corner_radius=0, fg_color="#3B8ED0")
sender_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

# Form Frame
sender_frame1 = ctk.CTkFrame(frame, width=800,height=300, corner_radius=0, fg_color="#3B8ED0")
sender_frame1.grid(row=2, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

# Form Frame
sender_frame2 = ctk.CTkFrame(frame, width=800,height=300, corner_radius=0, fg_color="#3B8ED0")
sender_frame2.grid(row=3, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

# Form Labels & Entries
def create_label_entry(parent, text, row):
    label = ctk.CTkLabel(parent, text=text, font=("Copperplate Gothic Bold", 18), fg_color="#3B8ED0", text_color="white")
    label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
    entry = ctk.CTkEntry(parent, font=("Copperplate Gothic Bold", 16), text_color="black", fg_color="white")
    entry.grid(row=row, column=1, padx=20, pady=15, ipadx=20, ipady=10, sticky="ew")
    return entry

your_name_entry = create_label_entry(sender_frame, "Your Name:", 0)
your_email_entry = create_label_entry(sender_frame1, "Your Email:", 1)
your_query_entry = create_label_entry(sender_frame2, "Your Query:", 2)

# Submit Button
submit_button = ctk.CTkButton(frame, text="Submit", command=submit_query, font=("Arial", 14), fg_color="#4CAF50", text_color="white")
submit_button.grid(row=4, column=0, columnspan=2, pady=20,ipadx=20, ipady=10)

root.mainloop()
