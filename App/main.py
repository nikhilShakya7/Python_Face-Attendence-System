import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import threading
from PIL import Image, ImageTk
import cv2
import numpy as np

VENV_PYTHON = r"E:\8th sem\New folder\PythonProject1\.venv\Scripts\python.exe"

# Load face recognizer and classifier globally
model = cv2.face.LBPHFaceRecognizer_create()
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


# Function to capture images and train model
def capture_images(student_id, name):
    data_path = f"../Dataset/{student_id}"
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    cap = cv2.VideoCapture(0)
    count = 0

    while count < 30:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            face = cv2.resize(face, (200, 200))
            img_name = os.path.join(data_path, f"{count}.jpg")
            cv2.imwrite(img_name, face)
            count += 1

        cv2.imshow("Capturing Images", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print('Image capture completed.')


# Function to start face recognition and mark attendance
def take_attendance():
    try:
        # Run detection.py script using subprocess
        result = subprocess.run([VENV_PYTHON, "detection.py"], check=True, text=True, capture_output=True)

        # If the subprocess runs successfully, output will be captured
        print(result.stdout)  # Print the standard output from detection.py

        # Optionally, show a success message in the Tkinter UI
        messagebox.showinfo("Success", "Attendance process completed successfully.")

    except subprocess.CalledProcessError as e:
        # If the subprocess fails, print error details
        messagebox.showerror("Error", f"An error occurred: {e.stderr}")


# Function to view attendance
def view_attendance():
    view_window = tk.Toplevel(root)
    view_window.title("View Attendance")
    view_window.geometry("600x400")

    tree = ttk.Treeview(view_window, columns=("ID", "Name", "Course", "Status", "Timestamp"), show="headings")

    tree.heading("ID", text="Student ID")
    tree.heading("Name", text="Name")
    tree.heading("Course", text="Course")
    tree.heading("Status", text="Status")
    tree.heading("Timestamp", text="Timestamp")

    tree.column("ID", width=100)
    tree.column("Name", width=150)
    tree.column("Course", width=100)
    tree.column("Status", width=100)
    tree.column("Timestamp", width=100)

    try:
        conn = sqlite3.connect("../Database/attendance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, name, course, Status, timestamp FROM attendance")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            tree.insert("", tk.END, values=row)

        tree.pack(expand=True, fill=tk.BOTH)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to open 'Add Student' window
def open_add_student():
    add_window = tk.Toplevel(root)
    add_window.title("Add Student")
    add_window.geometry("350x300")

    tk.Label(add_window, text="Student ID:", font=("Arial", 12)).pack(pady=5)
    id_entry = tk.Entry(add_window)
    id_entry.pack(pady=5)

    tk.Label(add_window, text="Name:", font=("Arial", 12)).pack(pady=5)
    name_entry = tk.Entry(add_window)
    name_entry.pack(pady=5)

    tk.Label(add_window, text="Course:", font=("Arial", 12)).pack(pady=5)
    course_entry = tk.Entry(add_window)
    course_entry.pack(pady=5)

    # Function to save student & capture images
    def save_student_to_db():
        student_id = id_entry.get().strip()
        name = name_entry.get().strip()
        course = course_entry.get().strip()

        if student_id and name and course:
            try:
                conn = sqlite3.connect("../Database/attendance.db")
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO attendance (student_id, Name, Course) VALUES (?, ?, ?)''',
                               (student_id, name, course))
                conn.commit()
                conn.close()

                # Run image capture in a separate thread
                def run_capture():
                    capture_images(student_id, name)
                    subprocess.run([VENV_PYTHON, "train.py"])  # Train model after capturing
                    root.after(0, lambda: messagebox.showinfo("Success", f"Student {name} added successfully!"))

                threading.Thread(target=run_capture, daemon=True).start()
                add_window.destroy()

            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Database error: {e}")
        else:
            messagebox.showerror("Error", "Please fill all fields.")

    # Button to add student & capture images
    tk.Button(add_window, text="Add Student & Capture Photo", font=("Arial", 12),
              command=save_student_to_db).pack(pady=15)


# Create the main window
root = tk.Tk()
root.title("Face Attendance System")
root.geometry("640x480")

# Background Image
bg_img = Image.open("../Resources/app-bg.png")
bg_img = bg_img.resize((640, 480))
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Title Label
title_label = tk.Label(root, text="Face Attendance System", font=("Times", 20, "bold"), fg="#333")
title_label.pack(pady=40)

# Buttons
ttk.Button(root, text="View Attendance", command=view_attendance).pack(pady=10)
ttk.Button(root, text="Add Student", command=open_add_student).pack(pady=10)
ttk.Button(root, text="Take Attendance", command=take_attendance).pack(pady=10)

# Run the GUI
root.mainloop()
