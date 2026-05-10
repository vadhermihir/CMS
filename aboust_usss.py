import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

# Initialize Tkinter Window
root = tk.Tk()
root.attributes("-fullscreen", True)
root.title("Track Tour Order")

# Get Screen Size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


def about_us():

    bg_image_path = "images/c4.jpg"
    bg_image = Image.open(bg_image_path)
    bg_image_resized = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_image_tk = ImageTk.PhotoImage(bg_image_resized)

    canvas = ctk.CTkCanvas(root, width=screen_width, height=screen_height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)
    canvas.image = bg_image_tk

    frame = ctk.CTkFrame(root, fg_color="#ffffff", width=350, height=1100,
                         corner_radius=10, border_width=4,border_color="black")
    frame.place(x=700,y=180)

    # Adjust the font size based on the screen height
    font_size = int(screen_height * 0.05)  # Font size is 5% of screen height

    # Title label inside the frame
    title_label = ctk.CTkLabel(frame, text="About Us", font=("Copperplate Gothic Bold", 32, "bold"), text_color="black")
    title_label.grid(row=0, column=0, pady=(20, 10), padx=20)

    description = """
            🚀 Welcome to Mv Enterprise!

            At Mv ENTERPRISE, we are committed to providing fast, reliable, and secure courier services.
            With years of experience in the logistics industry, we ensure that every package is handled 
            with utmost care and efficiency.

            🌟 Why Choose Us?
            ✅ Fast & Reliable Delivery
            ✅ Secure Handling
            ✅ Affordable Rates
            ✅ Real-Time Tracking
            ✅ 24/7 Customer Support

            📌 Our Mission:
            We aim to bridge distances by delivering not just parcels but trust and reliability.
            Whether it’s a business shipment, personal gift, or urgent document, we ensure 
            it reaches its destination safely and on time.

            📌 Our Vision:
            To become a leading courier service provider, known for innovation, efficiency, and customer satisfaction.

            📦 Your Package, Our Priority!
            """

    desc_label = ctk.CTkLabel(frame, text=description, font=("Arial", 16), text_color="black", wraplength=screen_width * 0.6)
    desc_label.grid(row=1, column=0, padx=20, pady=10)

    # Welcome Banner
    welcome_label12 = ctk.CTkLabel(
        root,
        text="About Us Page!",
        font=("Copperplate Gothic Bold", font_size, "bold"),
        text_color="white",
        fg_color="black",  # Proper background color for CTkLabel
        width=screen_width,
        height=100,
    )
    welcome_label12.place(relx=0.5, rely=0.1, anchor="center")

about_us()
root.mainloop()
