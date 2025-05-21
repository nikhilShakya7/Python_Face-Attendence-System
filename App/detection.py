import cv2
import numpy as np
import sqlite3
from datetime import datetime
from tkinter import messagebox

# Load the trained model
model = cv2.face.LBPHFaceRecognizer_create()
model.read("../Trained_Model/trained_model.xml")

face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
#face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# Store students who have already been marked present in this session
marked_students = set()
current_student = None
last_recognition_time = None


# Function to fetch the student name from the database
def get_student_name(student_id):
    conn = sqlite3.connect('../Database/attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM attendance WHERE student_id=?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else "Unknown"


# Function to get all student details
def get_student_details(student_id):
    conn = sqlite3.connect('../Database/attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, name, course, timestamp FROM attendance WHERE student_id=?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return row if row else (student_id, "Unknown", "N/A")


# Function to mark attendance in the database
def mark_attendance(student_id):
    global current_student, last_recognition_time
    try:
        conn = sqlite3.connect('../Database/attendance.db')
        cursor = conn.cursor()

        today_date = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%Y-%m-%d < %H:%M:%S > ")

        cursor.execute("""
            SELECT * FROM attendance 
            WHERE student_id = ? AND substr(timestamp, 1, 10) = ? AND Status = 'Present'
        """, (student_id, today_date))
        existing_record = cursor.fetchone()

        student_name = get_student_name(student_id)
        current_student = get_student_details(student_id)
        last_recognition_time = datetime.now()

        if existing_record:
            if student_id not in marked_students:
                messagebox.showinfo("Attendance", f"Attendance already marked for {student_name}.")
                marked_students.add(student_id)
        else:
            cursor.execute("""
                UPDATE attendance 
                SET Status = 'Present', timestamp = ? 
                WHERE student_id = ?
            """, (timestamp, student_id))
            conn.commit()
            messagebox.showinfo("Attendance", f"Attendance marked for {student_name} at {timestamp}.")
            marked_students.add(student_id)

        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error while marking attendance: {e}")


cap = cv2.VideoCapture(0)

cv2.namedWindow("Face Recognition Attendance System", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Face Recognition Attendance System", 1000, 700)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    overlay = frame.copy()
    cv2.rectangle(overlay, (width - 250, 0), (width, height), (40, 40, 40), -1)
    alpha = 0.8
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    header = np.zeros((70, width, 3), np.uint8)
    cv2.rectangle(header, (0, 0), (width, 70), (0, 102, 204), -1)
    frame[0:70, 0:width] = cv2.addWeighted(frame[0:70, 0:width], 0.7, header, 0.3, 0)

    cv2.putText(frame, "FACE RECOGNITION ATTENDANCE", (width // 2 - 280, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(frame, "SYSTEM", (width // 2 - 80, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%d %b %Y")
    cv2.putText(frame, f"{current_date}", (width - 130, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
    cv2.putText(frame, f"{current_time}", (width - 130, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)

    cv2.rectangle(frame, (width - 240, 90), (width - 10, 270), (60, 60, 60), 2)
    cv2.putText(frame, "STUDENT INFO", (width - 230, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
    if current_student:
        student_id, name, course, timestamp = current_student


        # Student details
        cv2.putText(frame, f"ID: {student_id}", (width - 230, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 255, 200), 1)
        cv2.putText(frame, f"Name: {name}", (width - 230, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 255, 200), 1)
        cv2.putText(frame, f"Course: {course}", (width - 230, 210),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 255, 200), 1)
        cv2.putText(frame, f"Last Marked:", (width - 230, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        cv2.putText(frame, f"{timestamp}", (width - 230, 260),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 255, 200), 1)
        status = "PRESENT" if student_id in marked_students else "RECOGNIZED And MARKED"
        status_color = (0, 255, 0) if status == "PRESENT" else (0, 255, 0)
        cv2.putText(frame, f"{status}", (width - 230, 290),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 1)
    else:
        cv2.putText(frame, "No student detected", (width - 230, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        cv2.putText(frame, "Looking for faces...", (width - 230, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)

    cv2.rectangle(frame, (width - 240, height - 180), (width - 10, height - 10), (60, 60, 60), 2)
    cv2.putText(frame, "INSTRUCTIONS", (width - 230, height - 150),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
    cv2.putText(frame, "- Press 'Q' to quit", (width - 230, height - 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    cv2.putText(frame, "- Stand in good lighting", (width - 230, height - 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    cv2.putText(frame, "- Face the camera directly", (width - 230, height - 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    # Face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi = gray[y:y + h, x:x + w]
        roi = cv2.resize(roi, (200, 200))

        student_id, confidence = model.predict(roi)
        confidence = int(100 * (1 - (confidence / 300)))

        if confidence > 78:
            # Get student details
            current_student = get_student_details(student_id)

            for i in range(1, 3):
                cv2.rectangle(frame, (x - i, y - i), (x + w + i, y + h + i),
                              (0, 255 - i * 50, 0), 2)

            # Display confidence near face
            cv2.putText(frame, f"{confidence}%", (x + w + 10, y + h // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

            if student_id not in marked_students:
                mark_attendance(student_id)
        else:
            current_student = None
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "UNKNOWN", (x + w // 2 - 40, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, f"{confidence}%", (x + w + 10, y + h // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

    cv2.imshow("Face Recognition Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
