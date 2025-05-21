import sqlite3
from tkinter import messagebox



def reset_attendance():
    try:
        conn = sqlite3.connect('../Database/attendance.db')
        cursor = conn.cursor()

        # Reset all students to Absent
        cursor.execute("UPDATE attendance SET status = 'Absent', timestamp = NULL")

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Attendance has been reset to 'Absent'.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error resetting attendance: {e}")

