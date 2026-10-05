import tkinter as tk
from tkinter import ttk

root = tk.Tk()

root.title("My First Tkinter Window")
root.geometry("640x480")

label = ttk.Label(root, text="Hello, Tkinter!")

label.pack(padx=20, pady=20)

root.mainloop()