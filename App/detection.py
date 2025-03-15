import cv2
import numpy as np
import sqlite3

# Function to fetch the student name from the database
def get_student_name(student_id):
    conn = sqlite3.connect('../Database/attendance.db')  # Connect to your database (change the path if needed)
    cursor = conn.cursor()

    # Query to fetch student name based on ID
    cursor.execute("SELECT name FROM attendance WHERE student_id=?", (student_id,))
    row = cursor.fetchone()

    conn.close()

    # If the student exists, return their name, otherwise return "Unknown"
    if row:
        return row[0]  # Name is in the first column
    else:
        return "Unknown"

# Load the trained model
model = cv2.face.LBPHFaceRecognizer_create()
model.read("../Trained_Model/trained_model.xml")  # Load the trained model from the XML file

# Create the face classifier
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#face_classifier = cv2.CascadeClassifier("App/haarcascade_frontalface_default.xml")

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi = gray[y:y + h, x:x + w]
        roi = cv2.resize(roi, (200, 200))

        student_id, confidence = model.predict(roi)
        confidence = int(100 * (1 - (confidence / 300)))  # Convert confidence to percentage

        # Display the result
        if confidence > 80:  # Confidence threshold for recognition
            student_name = get_student_name(student_id)  # Fetch name from database
            cv2.putText(frame, f"Name: {student_name} ({confidence}%)", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) == 13:  # Press Enter to exit
        break

cap.release()
cv2.destroyAllWindows()