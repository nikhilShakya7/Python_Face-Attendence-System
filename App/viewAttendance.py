import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

def view_attendance():
    view_window = tk.Toplevel()
    view_window.title("View Attendance")
    view_window.geometry("600x400")

    tree = ttk.Treeview(view_window, columns=("ID", "Name", "Course", "Status", "Timestamp"), show="headings")

    tree.heading("ID", text="Student ID")
    tree.heading("Name", text="Name")
    tree.heading("Course", text="Course")
    tree.heading("Status", text="Status")
    tree.heading("Timestamp", text="Timestamp")

    tree.column("ID", width=80
                )
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

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    view_attendance()
    root.mainloop()