from pupil_apriltags import Detector
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
detector = Detector(families='tag36h11')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(gray)

    for det in detections:
        # Get the corners of the tag
        corners = det.corners.astype(int)
        
        # Draw rectangle around the tag
        cv2.polylines(frame, [corners], True, (0, 255, 0), 2)
        
        # Draw tag ID
        center = det.center.astype(int)
        cv2.putText(frame, f"Tag {det.tag_id}", 
                    (center[0] - 20, center[1] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        print(f"Detected tag ID: {det.tag_id}")

    cv2.imshow('AprilTag Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
