from simple_facerec import SimpleFacerec
from report_matcher import match_report
import cv2
import os

# Load face encodings
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

# Load text reports
child_reports = {}
for filename in os.listdir("reports/"):
    if filename.endswith(".txt"):
        with open(f"reports/{filename}", "r") as f:
            child_reports[filename[:-4]] = f.read()

# Simulate someone describing a child
observed_description = input("Describe the child (e.g., mole on right cheek): ")

# Match reports text
matched_names = match_report(child_reports, observed_description)
print("📋 Matched reports (based on description):", matched_names)

# Start webcam for face match
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    face_locations, face_names = sfr.detect_known_faces(frame)

    for name in face_names:
        if name in matched_names:
            print(f"🎯 FOUND MATCHING CHILD: {name}")
        elif name != "Unknown":
            print(f"👀 Face matched but no report match: {name}")

    cv2.imshow("Trackify - Face Detection", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
