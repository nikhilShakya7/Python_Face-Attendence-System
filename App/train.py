import cv2
import numpy as np
import os

def preprocess_image(image):
    equalized = cv2.equalizeHist(image)
    blurred = cv2.GaussianBlur(equalized, (3, 3), 0)
    return blurred

def train_model():
    data_path = "../Dataset"
    folders = os.listdir(data_path)

    training_data, labels = [], []

    # Load images
    for folder in folders:
        folder_path = os.path.join(data_path, folder)
        if os.path.isdir(folder_path):
            student_id = int(folder.split("_")[0])
            images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

            for img in images:
                img_path = os.path.join(folder_path, img)
                image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if image is not None:
                    processed_image = preprocess_image(image)
                    training_data.append(np.asarray(processed_image, dtype=np.uint8))
                    labels.append(student_id)

    labels = np.asarray(labels, dtype=np.int32)

    model = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
    model.train(np.asarray(training_data), np.asarray(labels))

    os.makedirs("../Trained_Model", exist_ok=True)

    # Save the trained model
    model.save("../Trained_Model/trained_model.xml")

    print("Model training completed and saved successfully")

if __name__ == "__main__":
    train_model()