import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


def remove_student(student_id):
    try:
        conn = sqlite3.connect("../Database/attendance.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM attendance WHERE student_id = ?", (student_id,))
        student = cursor.fetchone()

        if not student:
            messagebox.showerror("Error", "Student ID not found.")
            return

        # Delete student from database
        cursor.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))
        conn.commit()
        conn.close()

        data_path = f"../Dataset/{student_id}"
        if os.path.exists(data_path):
            for file in os.listdir(data_path):
                file_path = os.path.join(data_path, file)
                os.remove(file_path)
            os.rmdir(data_path)

        messagebox.showinfo("Success", f"Student {student_id} removed successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")


def open_remove_student():
    remove_window = tk.Toplevel()
    remove_window.title("Remove Student")
    remove_window.geometry("1920x950")
    remove_window.configure(bg="#63C5DA")

    form_frame = ttk.Frame(remove_window, padding=30, relief="ridge")
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Apply styles
    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 16))
    style.configure("TEntry", font=("Arial", 16), padding=10)
    style.configure("TButton", font=("Arial", 18, "bold"), padding=10)

    # Title Label
    title_label = tk.Label(form_frame, text="Remove Student", font=("Arial", 20, "bold"), fg="#333")
    title_label.grid(row=0, column=0, columnspan=2, pady=15)

    # Student ID Label and Entry
    ttk.Label(form_frame, text="Student ID:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
    id_entry = ttk.Entry(form_frame)
    id_entry.grid(row=1, column=1, padx=10, pady=10, ipadx=30, ipady=5)

    def delete_student():
        student_id = id_entry.get().strip()
        if student_id:
            remove_student(student_id)
            remove_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter a Student ID.")

    ttk.Button(form_frame, text="Remove Student", command=delete_student).grid(row=2, column=0, columnspan=2, pady=20, ipadx=20, ipady=10)

    remove_window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_remove_student()
    root.mainloop()
