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

# Create a Text widget inside the canvas that will hold the font names
text_widget = tk.Text(canvas, wrap="word", height=30, width=50, font=("Helvetica", 12))
text_widget.insert(tk.END, "List of Available Fonts:\n\n")

# Insert each font in the list into the text widget
available_fonts = tkfont.families()
for font in available_fonts:
    text_widget.insert(tk.END, f"{font}\n")

# Make the text widget read-only
text_widget.config(state=tk.DISABLED)

# Create a window in the canvas to place the Text widget
canvas.create_window((0, 0), window=text_widget, anchor="nw")

# Configure the scrollbar
scrollbar.config(command=canvas.yview)

# Pack the canvas and scrollbar into the root window
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Update the scroll region of the canvas whenever the window changes
text_widget.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Run the Tkinter event loop
root.mainloop()
