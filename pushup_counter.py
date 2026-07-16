from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO('yolov8n-pose.pt')

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# YOLO pose keypoint indices (COCO format)
LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST = 5, 7, 9
RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST = 6, 8, 10

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Webcam nahi khul saka.")
    exit()

counter = 0
stage = None  # "up" or "down"

print("Push-up counter shuru. Band karne ke liye 'q' dabao.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)
    annotated_frame = results[0].plot()

    try:
        keypoints = results[0].keypoints.xy[0].cpu().numpy()

        shoulder = keypoints[LEFT_SHOULDER]
        elbow = keypoints[LEFT_ELBOW]
        wrist = keypoints[LEFT_WRIST]

        angle = calculate_angle(shoulder, elbow, wrist)

        # Counting logic
        if angle > 160:
            stage = "up"
        if angle < 90 and stage == "up":
            stage = "down"
            counter += 1

        cv2.putText(annotated_frame, f'Angle: {int(angle)}', (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    except Exception:
        pass

    cv2.putText(annotated_frame, f'Push-Ups: {counter}', (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow('Push-Up Counter', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()