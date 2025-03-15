import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import threading
import cv2

face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def capture_images(student_id, name):
    data_path = f"../Dataset/{student_id}"
    os.makedirs(data_path, exist_ok=True)

    cap = cv2.VideoCapture(0)
    count = 0

    while count < 50:
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
        if cv2.waitKey(10) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print('Image capture completed.')


def add_student(student_id, name, course):
    try:
        conn = sqlite3.connect("../Database/attendance.db")
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO attendance (student_id, Name, Course) VALUES (?, ?, ?)''',
                       (student_id, name, course))
        conn.commit()
        conn.close()

        # Capture images and train the model
        capture_images(student_id, name)
        subprocess.run([r"E:\8th sem\New folder\PythonProject1\.venv\Scripts\python.exe", "train.py"])

        print(f"Student {name} added successfully!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def open_add_student():

    add_window = tk.Toplevel()
    add_window.title("Add Student")
    add_window.geometry("400x350")
    add_window.configure(bg="#f0f0f0")


    title_label = tk.Label(add_window, text="Add Student", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
    title_label.pack(pady=10)


    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
    style.configure("TEntry", font=("Arial", 12), padding=5)
    style.configure("TButton", font=("Arial", 12, "bold"), padding=6)


    form_frame = ttk.Frame(add_window, padding=10)
    form_frame.pack(pady=10, padx=20, fill="both", expand=True)

    ttk.Label(form_frame, text="Student ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    id_entry = ttk.Entry(form_frame)
    id_entry.grid(row=0, column=1, padx=5, pady=5, ipadx=5)

    ttk.Label(form_frame, text="Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    name_entry = ttk.Entry(form_frame)
    name_entry.grid(row=1, column=1, padx=5, pady=5, ipadx=5)

    ttk.Label(form_frame, text="Course:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    course_entry = ttk.Entry(form_frame)
    course_entry.grid(row=2, column=1, padx=5, pady=5, ipadx=5)

    def save_student_to_db():
        """Gets user input and starts the student addition process."""
        student_id = id_entry.get().strip()
        name = name_entry.get().strip()
        course = course_entry.get().strip()

        if student_id and name and course:
            def run_add_student():
                add_student(student_id, name, course)
                add_window.after(0, lambda: messagebox.showinfo("Success", f"Student {name} added successfully!"))

            threading.Thread(target=run_add_student, daemon=True).start()
            add_window.destroy()
        else:
            messagebox.showerror("Error", "Please fill all fields.")

    # Button to add student & capture images
    ttk.Button(add_window, text="Add Student & Capture Photo", command=save_student_to_db).pack(pady=15)

    add_window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    open_add_student()
    root.mainloop()
