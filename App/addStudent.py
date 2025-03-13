import os
import subprocess
import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


def open_add_student(root):

    def save_student_to_db(student_id, name, course):
        try:
            conn = sqlite3.connect("../Database/attendance.db")
            cursor = conn.cursor()

            # Insert into database (without photo path for now)
            cursor.execute('''
                INSERT INTO attendance (student_id, name, course)
                VALUES (?, ?, ?)
            ''', (student_id, name, course))

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student added successfully!")

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Student ID already exists.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def capture_photo_and_train(student_id, name, course):
        try:
            # Run dataset.py to capture images
            print("Capturing images for the student...")
            subprocess.run(["python", "dataset.py", student_id, name, course])

            # Run detection.py after capturing images
            print("Running detection.py to train the model...")
            subprocess.run(["python", "detection.py"])

            messagebox.showinfo("Success", "Student added and model trained successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while capturing images or training: {e}")

    def show_details():
        student_id = id_entry.get()
        name = name_entry.get()
        course = course_entry.get()

        if student_id and name and course:
            save_student_to_db(student_id, name, course)

            # Capture photo and train the model
            capture_photo_and_train(student_id, name, course)

            details_window = tk.Toplevel(add_window)
            details_window.title("Student Details")
            details_window.geometry("300x400")
            details_window.configure(bg="#f0f0f0")

            tk.Label(details_window, text=f"ID: {student_id}", font=("Arial", 14), bg="#f0f0f0", fg="#333").pack(pady=10)
            tk.Label(details_window, text=f"Name: {name}", font=("Arial", 14), bg="#f0f0f0", fg="#333").pack(pady=10)
            tk.Label(details_window, text=f"Course: {course}", font=("Arial", 14), bg="#f0f0f0", fg="#333").pack(pady=10)

        else:
            messagebox.showerror("Error", "All fields are required!")

    add_window = tk.Toplevel(root)
    add_window.title("Add Student")
    add_window.geometry("400x500")
    add_window.configure(bg="#F5F5F5")

    title_label = tk.Label(add_window, text="Add Student", font=("Arial", 20, "bold"), bg="#F5F5F5", fg="#333")
    title_label.pack(pady=20)

    tk.Label(add_window, text="Student ID", font=("Arial", 12), bg="#F5F5F5", fg="#333").pack(pady=5)
    id_entry = tk.Entry(add_window, font=("Arial", 12), width=25, bd=2, relief="solid")
    id_entry.pack(pady=10)

    tk.Label(add_window, text="Name", font=("Arial", 12), bg="#F5F5F5", fg="#333").pack(pady=5)
    name_entry = tk.Entry(add_window, font=("Arial", 12), width=25, bd=2, relief="solid")
    name_entry.pack(pady=10)

    tk.Label(add_window, text="Course", font=("Arial", 12), bg="#F5F5F5", fg="#333").pack(pady=5)
    course_entry = tk.Entry(add_window, font=("Arial", 12), width=25, bd=2, relief="solid")
    course_entry.pack(pady=10)

    photo_label = tk.Label(add_window, text="No photo selected", font=("Arial", 12), bg="#F5F5F5", fg="#333")
    photo_label.pack(pady=10)

    show_button = tk.Button(add_window, text="Show Detail & Add Student", font=("Arial", 12), bg="#007BFF", fg="white",
                            relief="flat", width=25, height=2, command=show_details)
    show_button.pack(pady=15)

    add_window.mainloop()
