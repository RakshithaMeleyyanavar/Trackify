import face_recognition
import cv2
import os
import glob
import numpy as np


class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

    def load_encoding_images(self, images_path):
        images_path = glob.glob(os.path.join(images_path, "*.*"))
        print(f"🔍 Found {len(images_path)} images for encoding.")

        for img_path in images_path:
            img_name = os.path.basename(img_path)
            print(f"📷 Loading image: {img_name}")

            # Load with OpenCV
            img = cv2.imread(img_path)

            # ✅ Step 1: Ensure image loaded
            if img is None:
                print(f"❌ Failed to load image: {img_name}")
                continue

            # ✅ Step 2: Convert to RGB format
            try:
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            except Exception as e:
                print(f"⚠️ Cannot convert {img_name} to RGB: {e}")
                continue

            # ✅ Step 3: Face encoding
            encodings = face_recognition.face_encodings(rgb_img)
            if encodings:
                self.known_face_encodings.append(encodings[0])
                self.known_face_names.append(os.path.splitext(img_name)[0])
            else:
                print(f"😶 No face found in {img_name}!")

    def detect_known_faces(self, frame):
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches and matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            face_names.append(name)

        # Scale face locations back up
        face_locations = [(top * 4, right * 4, bottom * 4, left * 4)
                          for (top, right, bottom, left) in face_locations]

        return face_locations, face_names
