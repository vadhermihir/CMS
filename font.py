import tkinter as tk
import tkinter.font as tkfont

# Initialize Tkinter root window
root = tk.Tk()
root.title("Available Fonts")

# Set the window size
root.geometry("800x600")

# Create a Canvas widget with a scrollbar
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas that will hold the font labels
frame = tk.Frame(canvas)

# Create a window in the canvas to place the frame
canvas.create_window((0, 0), window=frame, anchor="nw")

# Display each font in the list as a label in the frame
available_fonts = tkfont.families()
for font in available_fonts:
    label = tk.Label(frame, text=font, font=(font, 14))
    label.pack()

# Configure the scrollbar
scrollbar.config(command=canvas.yview)

# Pack the canvas and scrollbar into the root window
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Update the scroll region of the canvas whenever the window changes
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Run the Tkinter event loop
root.mainloop()
