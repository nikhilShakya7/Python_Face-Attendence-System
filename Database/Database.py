import sqlite3


def initialize_database():
    conn = sqlite3.connect("../Database/attendance.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        course TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL,
        timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,        
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        UNIQUE(student_id, date)  
    )
    """)

    conn.commit()
    conn.close()


initialize_database()