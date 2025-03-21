import cv2
import os

def capture_images(student_id, name):
    if not student_id:
        print("Error: Student ID is required.")
        return

    data_path = f"../Dataset/{student_id}"
    os.makedirs(data_path, exist_ok=True)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    count = 0

    while count < 50:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        face_classifier = cv2.CascadeClassifier("App/haarcascade_frontalface_default.xml")

        faces = face_classifier.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            face = cv2.resize(face, (200, 200))
            img_name = os.path.join(data_path, f"{count}.jpg")
            cv2.imwrite(img_name, face)
            count += 1

        cv2.imshow("Capturing Images", frame)
        if cv2.waitKey(100) or count ==50:
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Image capture completed for student ID: {student_id}.")

