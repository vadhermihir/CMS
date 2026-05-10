import tkinter as tk
from PIL import Image, ImageSequence, ImageTk
import gc  # Garbage collection

# Create the root window
root = tk.Tk()
root.title("Welcome Screen")
root.attributes("-fullscreen", True)  # Fullscreen mode
root.configure(bg='black')

# Screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

### Function to Load GIF with Frame Limiting ###
def load_gif(path, width, height, max_frames=50):  # Limit frames to reduce memory usage
    image = Image.open(path)
    frames = []
    for i, frame in enumerate(ImageSequence.Iterator(image)):
        if i >= max_frames:  # Stop loading after max_frames
            break
        frames.append(
            ImageTk.PhotoImage(frame.copy().convert("RGBA").resize((width, height), Image.Resampling.LANCZOS))
        )
    return frames

### First Screen (GIF Animation) ###
gif_frames = load_gif("images/go.gif", screen_width, screen_height, max_frames=50)

gif_label = tk.Label(root, bg='black')
gif_label.pack(expand=True, fill="both")

def update_gif(index):
    gif_label.config(image=gif_frames[index])
    root.after(50, update_gif, (index + 1) % len(gif_frames))  # Adjust speed

def animate_text(index=0):
    if index <= len(text_to_display):
        text_label.config(text=text_to_display[:index])
        root.after(60, animate_text, index + 1)

text_to_display = "Going to Supermarket"
text_label = tk.Label(root, text="", font=("Arial", 40, "bold"), fg="white", bg="black")
text_label.place(relx=0.5, rely=0.1, anchor="center")

# Transition to second screen
def switch_to_second_screen():
    gif_label.pack_forget()
    text_label.place_forget()
    gc.collect()  # Free memory
    show_second_screen()

root.after(4000, switch_to_second_screen)  # Show second screen after 3 seconds

### Second Screen (Static Image with Moving Text) ###
def show_second_screen():
    global bg_welcome_image  # Keep reference to prevent garbage collection

    root.geometry(f"{screen_width}x{screen_height}")

    # Load background image
    welcome_image_path = "images/image.jpeg"
    welcome_image = Image.open(welcome_image_path)
    welcome_image = welcome_image.resize((screen_width, screen_height))
    bg_welcome_image = ImageTk.PhotoImage(welcome_image)  # Keep global reference

    # Create canvas
    canvas = tk.Canvas(root, width=screen_width, height=screen_height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_welcome_image, anchor="nw")  # Display background

    # Add moving welcome text
    text_id = canvas.create_text(
        0, 200,
        text="Welcome to Grocery Store",
        font=("Arial", 45, "bold"),
        fill="black",
        anchor="w"
    )

    # Function to move text
    def move_text():
        x, y = canvas.coords(text_id)
        if x < screen_width:
            canvas.move(text_id, 6, 0)  # Move text (x+=6, y stays same)
            root.after(30, move_text)
        else:
            root.after(3000, show_third_screen)  # Show third screen after 10 sec

    move_text()


def show_third_screen():
    global third_gif_frames, third_gif_label

    # Load third GIF file
    third_gif_frames = load_gif("images/shop.gif", screen_width, screen_height, max_frames=50)

    # Create GIF label for third screen
    third_gif_label = tk.Label(root)
    third_gif_label.pack(expand=True, fill="both")

    # Function to update third GIF
    def update_third_gif(index):
        third_gif_label.config(image=third_gif_frames[index])
        root.after(50, update_third_gif, (index + 1) % len(third_gif_frames))  # Adjust speed

    update_third_gif(0)

    # Wait for 3 seconds, then go to login screen
    root.after(3000, show_login_screen)  # Show login screen after 3 seconds

### Login Screen (Placeholder Function) ###
def show_login_screen():
        root.destroy()  # Close welcome screen and open login window

# Start animations
update_gif(0)
root.after(500, animate_text)





root.mainloop()