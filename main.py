import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

from functions.audio_params import audio_ai_params
from functions.add_texts import add_texts
from functions.guide import installation_guide


root = tk.Tk()
root.title("Loqui")
root.geometry("300x300")

# Set minimum and maximum window size
root.minsize(280, 290)
root.maxsize(320, 310)

# Set background color
root.configure(bg='#333333')

style = ttk.Style()

# Set button style
style.configure("TButton",
                foreground="black",
                background="white",
                font=("Helvetica", 15, "bold"),
                padding=7)

# Load an image
image = PhotoImage(file="ressources/logo_loqui.png")
image_label = tk.Label(root, image=image, bg='#333333')
image_label.pack(pady=5)

start_button = ttk.Button(root, text="Start", command=audio_ai_params, style="TButton")
start_button.pack(pady=6)

add_text_button = ttk.Button(root, text="Add Data", command=add_texts, style="TButton")
add_text_button.pack(pady=6)

add_text_button = ttk.Button(root, text="Local LLM Guide", command=installation_guide, style="TButton")
add_text_button.pack(pady=6)

# Center the window on the screen
root.update_idletasks()
x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
root.geometry(f"+{x}+{y}")

root.mainloop()