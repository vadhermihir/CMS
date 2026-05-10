import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

# Initialize CustomTkinter window
root = tk.Tk()

# Set the window to full screen
root.attributes("-fullscreen", True)
root.title("Track Tour Order")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and resize background image to fit the full screen
bg_image_path = "images/c88.png"
bg_image = Image.open(bg_image_path)
bg_image_resized = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
bg_image_tk = ImageTk.PhotoImage(bg_image_resized)

# Create a canvas to display the background image
canvas = ctk.CTkCanvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)
canvas.image = bg_image_tk  # Prevent garbage collection
custom_font = ("Copperplate Gothic Bold", 14)
# Create a welcome label
welcome_label = ctk.CTkLabel(
    root,
    text="Welcome To Order Manage  Page",
    font=("Copperplate Gothic Bold", 36, "bold"),
    text_color="white",
    bg_color="#0051AD",
    width=screen_width,
    height=100,
)
welcome_label.place(x=0, y=10)

# Main frame for content
frame = ctk.CTkFrame(root, fg_color="white", width=1520, height=730,
                     corner_radius=5, border_width=3, border_color="black")
frame.place(x=10, y=120)

# Scrollable frame for table
table_frame = ctk.CTkScrollableFrame(frame, width=1480, height=680, fg_color="white")
table_frame.place(x=10, y=10)

# Updated columns
columns = ["Sr No", "Consignment No", "Sender Name", "Sender Mobile", "Receiver Name", "Receiver Mobile", "Order Status", "Edit", "Delete"]

# Sample static data
data = [
    [1, "CN001", "Alice", "1234567890", "Bob", "9876543210", "Shipped"],
    [2, "CN002", "Charlie", "1234567891", "David", "9876543211", "In Transit"],
    [3, "CN003", "Eve", "1234567892", "Frank", "9876543212", "Delivered"],
    [4, "CN004", "Grace", "1234567893", "Hank", "9876543213", "Pending"],
]

# Styling for table
header_bg = "#FDC029"  # Dark Blue for headers
header_fg = "white"
row_colors = ["#0052B0", "#0052B0"]  # Alternating row colors
font_header = ("Copperplate Gothic Bold", 16, "bold")
font_cell = ("Copperplate Gothic Bold", 14)

# Create column headers with background color
for col_index, col_name in enumerate(columns):
    header = ctk.CTkLabel(table_frame, text=col_name, font=font_header, text_color="black", fg_color=header_bg, corner_radius=5)
    header.grid(row=0, column=col_index, padx=10, pady=10, sticky="ew")

# Insert data rows with alternating colors
for row_index, row_data in enumerate(data, start=1):
    row_bg = row_colors[row_index % 2]  # Alternate row colors
    for col_index, cell_data in enumerate(row_data):
        cell = ctk.CTkLabel(table_frame, text=cell_data, font=font_cell, text_color="white", fg_color=row_bg, corner_radius=5)
        cell.grid(row=row_index, column=col_index, padx=10, pady=5, sticky="ew")

    # Static Edit Button
    edit_button = ctk.CTkButton(table_frame, text="Edit",font=custom_font, fg_color="#3498DB", text_color="white", corner_radius=5)
    edit_button.grid(row=row_index, column=len(columns) - 2, padx=10, pady=5)

    # Static Delete Button
    delete_button = ctk.CTkButton(table_frame, text="Delete",font=custom_font, fg_color="#E74C3C", text_color="white", corner_radius=5)
    delete_button.grid(row=row_index, column=len(columns) - 1, padx=10, pady=5)

# Run the Tkinter main loop
root.mainloop()
