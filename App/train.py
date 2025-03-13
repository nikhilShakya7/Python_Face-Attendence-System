import cv2
import numpy as np
import os

def train_model():
    # Path to dataset
    data_path = "../Dataset"
    folders = os.listdir(data_path)

    training_data, labels = [], []

    # Load images and labels
    for folder in folders:
        folder_path = os.path.join(data_path, folder)
        if os.path.isdir(folder_path):  # Ensure it's a folder
            student_id = int(folder.split("_")[0])  # Assuming the folder name is the student ID
            images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

            for img in images:
                img_path = os.path.join(folder_path, img)
                image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if image is not None:
                    training_data.append(np.asarray(image, dtype=np.uint8))
                    labels.append(student_id)  # Assign the student ID as label

    labels = np.asarray(labels, dtype=np.int32)

    # Create and train the model
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(np.asarray(training_data), np.asarray(labels))

    # Ensure the directory exists
    os.makedirs("../Trained_Model", exist_ok=True)

    # Save the trained model
    model.save("../Trained_Model/trained_model.xml")

    print("Model training completed and saved successfully!")

if __name__ == "__main__":
    train_model()
