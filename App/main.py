import tkinter as tk
from tkinter import ttk
import subprocess
from PIL import Image, ImageTk

VENV_PYTHON = r"E:\8th sem\New folder\PythonProject1\.venv\Scripts\python.exe"

# Function to open 'Add Student' window
def open_add_student():
    subprocess.Popen([VENV_PYTHON, "addStudent.py"])

def take_attendance():
    subprocess.Popen([VENV_PYTHON, "detection.py"])
# Function to open 'View Attendance' window
def open_view_attendance():
    subprocess.Popen([VENV_PYTHON, "viewAttendance.py"])

# Create the main window
root = tk.Tk()
root.title("Face Attendance System")
root.geometry("1920x1480")

# Background Image
bg_img = Image.open("../Resources/app-bg.png")
bg_img = bg_img.resize((1920, 950))
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Title Label
title_label = tk.Label(root, text="Face Attendance System", font=("Times", 50, "bold"), fg="#333")
title_label.pack(pady=100)

style = ttk.Style()
style.configure("TButton", borderwidth=5, font=("Arial", 22), padding=20, background="#00BFFF", foreground="black",
                activebackground="#5F9EA0", activeforeground="white")
style.configure("Title.TLabel", font=("Times", 20, "bold"), foreground="#333")

# Buttons
ttk.Button(root, text="View Attendance", command=open_view_attendance).pack(pady=10)
ttk.Button(root, text="Add Student", command=open_add_student).pack(pady=10)
ttk.Button(root, text="Take Attendance", command=take_attendance).pack(pady=10, ipadx=20)

# Run the GUI
root.mainloop()