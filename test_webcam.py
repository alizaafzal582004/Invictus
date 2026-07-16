from ultralytics import YOLO
import cv2

# Load lightweight pose model
model = YOLO('yolov8n-pose.pt')

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Webcam nahi khul saka. Camera connected hai check karo.")
    exit()

print("Webcam khul gaya. Band karne ke liye 'q' dabao.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame nahi mil raha, exiting...")
        break

    # Run pose detection on the frame
    results = model(frame, verbose=False)

    # Draw skeleton/keypoints on frame
    annotated_frame = results[0].plot()

    cv2.imshow('Pose Detection Test', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()