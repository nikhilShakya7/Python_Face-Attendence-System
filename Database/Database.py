import sqlite3

# Connect to the database
conn = sqlite3.connect("../Database/attendance.db")
cursor = conn.cursor()

#  Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        student_id TEXT UNIQUE,
        Name TEXT,
        Status TEXT DEFAULT 'Absent',
        Course TEXT,
        timestamp TEXT
      
    )

''')

# Commit changes and close the connection
conn.commit()
conn.close()