import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os
import bcrypt
from dotenv import load_dotenv

from App.resetAttendance import reset_attendance

ATTENDANCE_APP_SCRIPT = r"E:\8th sem\New folder\PythonProject1\.venv\Scripts\python.exe"
SCRIPT_ARG = r"attendance_system.py"

load_dotenv()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH").encode('utf-8')

def toggle_password():
    if entry_password.cget("show") == "*":
        entry_password.config(show="")
        toggle_btn.config(text="🙈")
    else:
        entry_password.config(show="*")
        toggle_btn.config(text="👁")


# Login Authentication Function
def login(event=None):
    username = entry_username.get()
    password = entry_password.get()

    if username == ADMIN_USERNAME and bcrypt.checkpw(password.encode('utf-8'), ADMIN_PASSWORD_HASH):
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
        root.destroy()
        launch_app()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

# to launch the attendance system 
def launch_app():
    root = tk.Tk()
    root.title("Face Attendance System")
    root.geometry("1920x1480")

    bg_img = Image.open("../Resources/app-bg.png")
    bg_img = bg_img.resize((1920, 950))
    bg_photo = ImageTk.PhotoImage(bg_img)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    title_label = tk.Label(root, text="Face Attendance System", font=("Times", 50, "bold"), fg="#333")
    title_label.pack(pady=100)

    button_style = {
        "font": ("times", 20, "bold"),
        "width": 20,
        "height": 2,
        "bg": "#5F9EA0",
        "fg": "white",
        "activebackground": "#4682B4",
        "activeforeground": "black",
        "bd": 3,
        "relief": "raised"
    }

    add_student_btn = tk.Button(text="➕ Add Student", command=open_add_student, **button_style)
    add_student_btn.pack(pady=10)
    view_attendance_btn = tk.Button(text="📊 View Attendance", command=open_view_attendance, **button_style)
    view_attendance_btn.pack(pady=10)
    take_attendance_btn = tk.Button(text="📸 Take Attendance", command=take_attendance, **button_style)
    take_attendance_btn.pack(pady=10)
    remove_student_btn = tk.Button(text="❌ Remove Student", command=remove_student, **button_style)
    remove_student_btn.pack(pady=10)

    reset_btn = tk.Button(
        text="🔄️Reset",
        command=reset_attendance,
        font=("times", 14, "bold"),
        width=10, height=1,
        bg="#FF6347", fg="white",
        activebackground="#CD5C5C", activeforeground="black",
        bd=2, relief="raised"
    )
    reset_btn.place(relx=0.1, rely=0.9, anchor="se")


    root.mainloop()

# Functions for handling the attendance system actions
def open_add_student():
    subprocess.Popen([ATTENDANCE_APP_SCRIPT, "addStudent.py"])

def take_attendance():
    subprocess.Popen([ATTENDANCE_APP_SCRIPT, "detection.py"])

def open_view_attendance():
    subprocess.Popen([ATTENDANCE_APP_SCRIPT, "viewAttendance.py"])

def remove_student():
    subprocess.Popen([ATTENDANCE_APP_SCRIPT, "removeStudent.py"])




# Initialize Tkinter Window for Admin Login
root = tk.Tk()
root.title("Admin Login")
root.geometry("1920x950")
root.configure(bg="#F4F4F4")

try:
    bg_img = Image.open("../Resources/admin.jpg")
    bg_img = bg_img.resize((150, 150))
    bg_photo = ImageTk.PhotoImage(bg_img)
    bg_label = tk.Label(root, image=bg_photo, bg="#F4F4F4")
    bg_label.image = bg_photo
    bg_label.pack(pady=20)
except FileNotFoundError:
    print("Background image not found.")

# Title Label
title_label = tk.Label(root, text="Admin Login", font=("Arial", 30, "bold"), fg="#333", bg="#F4F4F4")
title_label.pack(pady=20)

# Username Field
tk.Label(root, text="Username:", font=("Arial", 16), bg="#F4F4F4").pack(pady=5)
entry_username = tk.Entry(root, font=("Arial", 14), width=40, bd=2, relief="solid", justify="center")

entry_username.bind("<FocusIn>", lambda event: entry_username.delete(0, tk.END))
entry_username.pack(pady=10, ipady=5)

# Password
tk.Label(root, text="Password:", font=("Arial", 16), bg="#F4F4F4").pack(pady=5)
password_frame = tk.Frame(root, bg="#F4F4F4")
entry_password = tk.Entry(password_frame, font=("Arial", 14), width=30, bd=2, relief="solid", justify="center", show="*")

entry_password.bind("<FocusIn>", lambda event: entry_password.delete(0, tk.END))
entry_password.pack(side="left", padx=5, ipady=5)

toggle_btn = tk.Button(password_frame, text="👁", font=("Arial", 12), command=toggle_password, relief="flat", bg="#F4F4F4")
toggle_btn.pack(side="left")
password_frame.pack(pady=5)

# Login Button

btn_login = tk.Button(root, text="Login", font=("Arial", 16, "bold"), bg="#5F9EA0", fg="white", width=15, height=2, bd=3, relief="raised", command=login)
btn_login.pack(pady=30)


root.bind("<Return>", login)


footer_label = tk.Label(root, text="Face Attendance System", font=("Arial", 12), fg="#666", bg="#F4F4F4")
footer_label.pack(side="bottom", pady=70)

root.mainloop()
