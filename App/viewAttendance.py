import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from matplotlib import pyplot as plt
from tkcalendar import DateEntry
from saveAttendance import export_attendance

def show_graph(present_count, absent_count):
    labels = ['Present', 'Absent']
    counts = [present_count, absent_count]

    plt.bar(labels, counts, color=['#28a745', '#dc3545'])
    plt.title("Attendance Graph")
    plt.ylabel("Count")
    plt.xlabel("Status")
    plt.show()


def view_attendance():
    view_window = tk.Toplevel()
    view_window.title("View Attendance")
    view_window.geometry("1200x700")
    view_window.configure(bg="#f8f9fa")

    title_label = tk.Label(view_window, text="Attendance Records", font=("Arial", 20, "bold"), fg="#333", bg="#f8f9fa")
    title_label.pack(pady=10)

    search_frame = tk.Frame(view_window, bg="#f8f9fa")
    search_frame.pack(pady=10, fill="x", padx=20)
    tk.Label(search_frame, text="Search:", font=("Arial", 12), bg="#f8f9fa").pack(side="left", padx=5)
    search_entry = ttk.Entry(search_frame, width=50, font=("Arial", 12))
    search_entry.pack(side="left", padx=5)

    tk.Label(search_frame, text="Select Date:", font=("Arial", 12), bg="#f8f9fa").pack(side="left", padx=5)

    date_entry = DateEntry(
        search_frame,
        width=12,
        background='darkblue',
        foreground='white',
        borderwidth=2,
        date_pattern='yyyy-mm-dd',
        font=("Arial", 12)
    )
    date_entry.pack(side="left", padx=5)

    table_frame = tk.Frame(view_window)
    table_frame.pack(padx=20, pady=10, fill="both", expand=True)

    tree_scroll = ttk.Scrollbar(table_frame)
    tree_scroll.pack(side="right", fill="y")

    tree = ttk.Treeview(
        table_frame,
        columns=("ID", "Name", "Course", "Status", "Timestamp"),
        show="headings",
        yscrollcommand=tree_scroll.set,
        selectmode="extended"
    )
    tree.pack(expand=True, fill="both")
    tree_scroll.config(command=tree.yview)

    columns = [
        ("ID", 100, "center"),
        ("Name", 200, "center"),
        ("Course", 150, "center"),
        ("Status", 100, "center"),
        ("Timestamp", 250, "center")
    ]

    for col, width, anchor in columns:
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor=anchor)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    style.configure("Treeview", font=("Arial", 11), rowheight=30)
    style.map("Treeview", background=[("selected", "#007bff")])
    tree.tag_configure("present", background="#d4edda")
    tree.tag_configure("absent", background="#f8d7da")



    def load_attendance(filter_text=""):
        present_count = 0
        absent_count = 0
        for row in tree.get_children():
            tree.delete(row)

        selected_date = date_entry.get()
        use_date_filter = bool(selected_date)

        try:
            conn = sqlite3.connect("../Database/attendance.db")
            cursor = conn.cursor()
            query = """
                SELECT student_id, name, course, status, timestamp 
                FROM attendance
            """

            params = ()
            if filter_text:
                query += " WHERE name LIKE ? OR student_id LIKE ? OR course LIKE ?"
                search_param = f"%{filter_text}%"
                params = (search_param, search_param, search_param)

            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()

            present_count = 0
            absent_count = 0

            for row in rows:
                status = row[3].lower()
                tags = (status,) if status in ("present", "absent") else ()
                tree.insert("", tk.END, values=row, tags=tags)

                if status == "present":
                    present_count += 1
                elif status == "absent":
                    absent_count += 1

            update_statistics(present_count, absent_count)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load attendance: {e}")
        return present_count, absent_count

    def update_statistics(present, absent):
        if hasattr(view_window, 'stats_frame'):
            stats_frame = view_window.stats_frame
            for widget in stats_frame.winfo_children():
                widget.destroy()
        else:
            stats_frame = tk.Frame(view_window, bg="#f8f9fa")
            stats_frame.pack(pady=10, fill="x", padx=20)
            view_window.stats_frame = stats_frame

        total = present + absent

        tk.Label(stats_frame, text=f"Present: {present}", font=("Arial", 12, "bold"), bg="#d4edda", fg="#155724",
                 padx=10, pady=5).pack(side="left", padx=5)

        tk.Label(stats_frame, text=f"Absent: {absent}", font=("Arial", 12, "bold"), bg="#f8d7da", fg="#721c24",
                 padx=10, pady=5).pack(side="left", padx=5)

        tk.Label(stats_frame, text=f"Total: {total}", font=("Arial", 12, "bold"), bg="#e2e3e5", fg="#383d41",
                 padx=10, pady=5).pack(side="left", padx=5)

        if total > 0:
            percentage = (present / total) * 100
            tk.Label(stats_frame, text=f"Attendance Rate: {percentage:.1f}%", font=("Arial", 12, "bold"),
                     bg="#d1ecf1", fg="#0c5460", padx=10, pady=5).pack(side="left", padx=5)

    def search_records(event=None):
        load_attendance(search_entry.get().strip())

    search_entry.bind("<KeyRelease>", search_records)
    date_entry.bind("<<DateEntrySelected>>", search_records)

    def get_student_history(student_id):
        conn = sqlite3.connect("../Database/attendance.db")
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    date,
                    status,
                    timestamp
                FROM daily_attendance 
                WHERE student_id = ?
                ORDER BY date DESC
            """, (student_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load history: {e}")
            return []
        finally:
            conn.close()

    def show_student_details(event):
        selected_item = tree.focus()
        if not selected_item:
            return

        student_data = tree.item(selected_item, 'values')

        detail_window = tk.Toplevel(view_window)
        detail_window.title(f"Attendance History - {student_data[1]}")
        detail_window.geometry("800x600")
        detail_window.configure(bg="#f8f9fa")

        # Main container
        container = ttk.Frame(detail_window)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Student info frame
        info_frame = ttk.Frame(container)
        info_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(info_frame,
                  text=f"Student ID: {student_data[0]}",
                  font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(info_frame,
                  text=f"Name: {student_data[1]}",
                  font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", padx=5)
        ttk.Label(info_frame,
                  text=f"Course: {student_data[2]}",
                  font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=5)

        # Statistics frame
        stats_frame = ttk.Frame(container)
        stats_frame.pack(fill="x", pady=(0, 15))

        # Get history data
        history_data = get_student_history(student_data[0])

        if not history_data:
            ttk.Label(container, text="No attendance history found").pack()
            return

        # Calculate statistics
        total = len(history_data)
        present = sum(1 for record in history_data if record[1] and record[1].lower() == "present")
        absent = total - present
        rate = (present / total * 100) if total > 0 else 0

        # Display stats
        ttk.Label(stats_frame,
                  text=f"Total Records: {total}",
                  style='Stats.TLabel').pack(side="left", padx=5)
        ttk.Label(stats_frame,
                  text=f"Present: {present}",
                  style='Present.TLabel').pack(side="left", padx=5)
        ttk.Label(stats_frame,
                  text=f"Absent: {absent}",
                  style='Absent.TLabel').pack(side="left", padx=5)
        ttk.Label(stats_frame,
                  text=f"Attendance Rate: {rate:.1f}%",
                  style='Rate.TLabel').pack(side="left", padx=5)

        # History treeview
        tree_frame = ttk.Frame(container)
        tree_frame.pack(fill="both", expand=True)

        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")

        history_tree = ttk.Treeview(
            tree_frame,
            columns=("Date", "Day", "Status", "Time"),
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            height=15
        )

        tree_scroll_y.config(command=history_tree.yview)
        tree_scroll_x.config(command=history_tree.xview)


        columns = [
            ("Date", 120, "center"),
            ("Day", 100, "center"),
            ("Status", 100, "center"),
            ("Time", 100, "center")
        ]

        for col, width, anchor in columns:
            history_tree.heading(col, text=col)
            history_tree.column(col, width=width, anchor=anchor)

        for date, status, time in history_data:
            try:
                day = datetime.strptime(date, "%Y-%m-%d").strftime("%A") if date else "Unknown"
            except (ValueError, TypeError):
                day = "Invalid Date"

            tags = (status.lower(),) if status and status.lower() in ("present", "absent") else ()

            display_time = time if status and status.lower() == "present" and time else "N/A"

            history_tree.insert("", tk.END,
                                values=(
                                    date if date else "N/A",
                                    day,
                                    status if status else "N/A",
                                    display_time
                                ),
                                tags=tags)

        # Grid layout
        history_tree.grid(row=0, column=0, sticky="nsew")
        tree_scroll_y.grid(row=0, column=1, sticky="ns")
        tree_scroll_x.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure("Present.TLabel", background="#d4edda", foreground="#155724")
        style.configure("Absent.TLabel", background="#f8d7da", foreground="#721c24")
        style.configure("Stats.TLabel", background="#e2e3e5", foreground="#383d41")
        style.configure("Rate.TLabel", background="#d1ecf1", foreground="#0c5460")

        history_tree.tag_configure("present", background="#d4edda")
        history_tree.tag_configure("absent", background="#f8d7da")
    tree.bind("<Double-1>", show_student_details)

    button_frame = tk.Frame(view_window, bg="#f8f9fa")
    button_frame.pack(pady=10)

    def view_graph():
        present_count, absent_count = load_attendance()
        show_graph(present_count, absent_count)
    view_graph_button = tk.Button(
        button_frame, text="View Graph", font=("Arial", 12, "bold"),
        bg="#007bff", fg="white", padx=20, pady=5, bd=0,
        command=view_graph,
        relief=tk.FLAT, activebackground="#0056b3", activeforeground="white"
    )

    view_graph_button.pack(pady=5, padx=10, side="left")
    view_graph_button.bind("<Enter>", lambda e: view_graph_button.config(bg="#0056b3"))
    view_graph_button.bind("<Leave>", lambda e: view_graph_button.config(bg="#007bff"))

    save_button = tk.Button(
        button_frame, text="Save Record", font=("Arial", 12, "bold"),
        bg="#28a745", fg="white", padx=20, pady=5, bd=0,
        command=lambda: [export_attendance(), load_attendance()],
        relief=tk.FLAT, activebackground="#218838", activeforeground="white"
    )
    save_button.pack(pady=5)
    save_button.bind("<Enter>", lambda e: save_button.config(bg="#218838"))
    save_button.bind("<Leave>", lambda e: save_button.config(bg="#28a745"))
    load_attendance()

    view_window.update_idletasks()
    width = view_window.winfo_width()
    height = view_window.winfo_height()
    x = (view_window.winfo_screenwidth() // 2) - (width // 2)
    y = (view_window.winfo_screenheight() // 2) - (height // 2)
    view_window.geometry(f"{width}x{height}+{x}+{y}")
    view_window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    view_attendance()
    root.mainloop() 