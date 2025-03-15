import cv2
import numpy as np
import os


def train_model():

    data_path = "../Dataset"
    folders = os.listdir(data_path)

    training_data, labels = [], []

    # Load images and labels
    for folder in folders:
        folder_path = os.path.join(data_path, folder)
        if os.path.isdir(folder_path):
            student_id = int(folder.split("_")[0])
            images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

            for img in images:
                img_path = os.path.join(folder_path, img)
                image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if image is not None:
                    training_data.append(np.asarray(image, dtype=np.uint8))
                    labels.append(student_id)

    labels = np.asarray(labels, dtype=np.int32)

    # Create and train the model
    model = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8
)
    model.train(np.asarray(training_data), np.asarray(labels))


    os.makedirs("../Trained_Model", exist_ok=True)

    # Save the trained model
    model.save("../Trained_Model/trained_model.xml")

    print("Model training completed and saved successfully!")

if __name__ == "__main__":
    train_model()

'''import os
import cv2
import numpy as np
import joblib
from skimage.feature import hog
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder

def extract_hog_features(image):
    """
    Extracts HOG (Histogram of Oriented Gradients) features from a grayscale image.
    """
    return hog(image, pixels_per_cell=(8, 8), cells_per_block=(2, 2), feature_vector=True)

def train_svm_model():
    data_path = "../Dataset"
    if not os.path.exists(data_path):
        print("❌ Dataset directory not found! Please check the path.")
        return

    folders = os.listdir(data_path)
    feature_vectors, labels = [], []

    print("🔄 Scanning dataset and extracting HOG features...")

    for folder in folders:
        folder_path = os.path.join(data_path, folder)

        if not os.path.isdir(folder_path):
            continue  # Skip non-folder files

        try:
            student_id = folder.split("_")[0]  # Extract student ID from folder name
        except ValueError:
            print(f"⚠️ Skipping folder '{folder}' (Invalid ID format).")
            continue

        images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not images:
            print(f"⚠️ No images found in '{folder}', skipping...")
            continue

        for img in images:
            img_path = os.path.join(folder_path, img)
            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            if image is None:
                print(f"⚠️ Could not read image: {img_path}, skipping...")
                continue

            image = cv2.resize(image, (128, 128))  # Resize for consistency
            features = extract_hog_features(image)

            feature_vectors.append(features)
            labels.append(student_id)

    if len(feature_vectors) == 0:
        print("❌ No valid images found for training. Check dataset structure!")
        return

    print(f"✅ Extracted HOG features from {len(feature_vectors)} images.")

    # Convert labels to numerical values
    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(labels)

    # Train SVM classifier
    print("🔄 Training SVM model...")
    model = SVC(kernel="linear", probability=True)
    model.fit(feature_vectors, labels)

    # Save model and label encoder
    os.makedirs("../Trained_Model", exist_ok=True)
    joblib.dump(model, "../Trained_Model/svm_face_model.pkl")
    joblib.dump(label_encoder, "../Trained_Model/label_encoder.pkl")

    print("✅ SVM model training completed and saved successfully!")

if __name__ == "__main__":
    train_svm_model()
'''