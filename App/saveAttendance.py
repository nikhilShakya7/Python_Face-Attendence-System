import csv
import sqlite3
import os
from datetime import datetime
from tkinter import messagebox


def export_attendance():
    try:
        saved_folder = "../Saved Attendance"
        os.makedirs(saved_folder, exist_ok=True)

        conn = sqlite3.connect("../Database/attendance.db")
        cursor = conn.cursor()

        today_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")

        cursor.execute("SELECT DISTINCT student_id, name, course FROM attendance")
        all_students = cursor.fetchall()

        if len(all_students) == 0:
            messagebox.showwarning("No Data", "No student records found")
            return

        for student_id, name, course in all_students:
            cursor.execute("""
                INSERT OR IGNORE INTO students (student_id, name, course)
                VALUES (?, ?, ?)
            """, (student_id, name, course))

        cursor.execute("""
            SELECT student_id, status, timestamp 
            FROM attendance 
            WHERE timestamp LIKE ? || '%'
        """, (today_date,))
        today_records = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}

        for student_id, name, course in all_students:
            if student_id in today_records:
                status, timestamp = today_records[student_id]
            else:
                status = 'Absent'
                timestamp = f"{today_date} {current_time}"

            cursor.execute("""
                INSERT OR REPLACE INTO daily_attendance 
                (student_id, date, status, timestamp)
                VALUES (?, ?, ?, ?)
            """, (student_id, today_date, status, timestamp))

        conn.commit()

        filename = os.path.join(saved_folder, f"attendance_{today_date}.csv")

        with open(filename, mode="w", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow([f"Attendance Report - {today_date}"])
            writer.writerow([])
            writer.writerow(["Student ID", "Name", "Course", "Status", "Date", "Time"])

            cursor.execute("""
                SELECT s.student_id, s.name, s.course, d.status, d.timestamp
                FROM students s
                LEFT JOIN daily_attendance d ON s.student_id = d.student_id AND d.date = ?
                ORDER BY s.student_id
            """, (today_date,))

            records = cursor.fetchall()

            for record in records:
                student_id, name, course, status, timestamp = record
                if status == 'Present' and timestamp:
                    try:
                        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                        date_part = dt.strftime("%Y-%m-%d")
                        time_part = dt.strftime("%H:%M:%S")
                    except ValueError:
                        date_part = today_date
                        time_part = "N/A"
                else:
                    date_part = "N/A"
                    time_part = "N/A"

                writer.writerow([student_id, name, course, status, date_part, time_part])

            present_count = sum(1 for record in records if record[3] == 'Present')
            writer.writerow([])
            writer.writerow(["SUMMARY STATISTICS"])
            writer.writerow(["Total Students:", len(records)])
            writer.writerow(["Present:", present_count])
            writer.writerow(["Absent:", len(records) - present_count])
            writer.writerow(["Attendance Rate:", f"{present_count / len(records) * 100:.1f}%"])

        messagebox.showinfo("Success", f"Attendance saved")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save attendance: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()