from pupil_apriltags import Detector
import cv2
import numpy as np
import random

PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_SPEED = 4
PIPE_COLOR = (0, 200, 0)
NUM_PIPES = 3
PIPE_SPACING = 250  # horizontal distance between pipes

# Initialize pipes: each is [x, gap_y, passed]
pipes = []
for i in range(NUM_PIPES):
    x = 640 + i * PIPE_SPACING
    gap_y = random.randint(100, 380)
    pipes.append([x, gap_y, False])

cap = cv2.VideoCapture(0)
detector = Detector(families='tag36h11') # looks for this tag

# Set initial circle position to center (assuming 640x480)
frame_width, frame_height = 640, 480
bird_x = 100  # Fixed x-position for the bird
bird_radius = 15
circle_pos = [bird_x, frame_height // 2]

score = 0
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, frame = cap.read() # reads camera frame
    if not ret:
        print("Error: Could not read from webcam. Exiting.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # converts to grayscale to detect tag
    detections = detector.detect(gray) # detects tag

    if detections:
        det = detections[0]
        center = det.center.astype(int)
        # Only update y-position
        circle_pos[1] = center[1]
        cv2.putText(frame, f"Tag {det.tag_id}", 
                    (center[0] - 20, center[1] - 20),
                    font, 0.8, (0, 255, 0), 2)
        print(f"Detected tag ID: {det.tag_id}")

    collision = False
    for pipe in pipes:
        pipe[0] -= PIPE_SPEED  # Move left
        # Draw top pipe
        cv2.rectangle(frame, (pipe[0], 0), (pipe[0] + PIPE_WIDTH, pipe[1] - PIPE_GAP // 2), PIPE_COLOR, -1)
        # Draw bottom pipe
        cv2.rectangle(frame, (pipe[0], pipe[1] + PIPE_GAP // 2), (pipe[0] + PIPE_WIDTH, frame_height), PIPE_COLOR, -1)

        # Collision detection
        bird_left = bird_x - bird_radius
        bird_right = bird_x + bird_radius
        bird_top = circle_pos[1] - bird_radius
        bird_bottom = circle_pos[1] + bird_radius
        pipe_left = pipe[0]
        pipe_right = pipe[0] + PIPE_WIDTH
        pipe_bottom = pipe[1] - PIPE_GAP // 2
        pipe_top = pipe[1] + PIPE_GAP // 2
        if bird_right > pipe_left and bird_left < pipe_right and bird_top < pipe_bottom:
            collision = True
        if bird_right > pipe_left and bird_left < pipe_right and bird_bottom > pipe_top:
            collision = True
        if not pipe[2] and pipe_right < bird_x:
            score += 1
            pipe[2] = True

    # Respawn pipes that have moved off screen
    for pipe in pipes:
        if pipe[0] + PIPE_WIDTH < 0:
            pipe[0] = frame_width
            pipe[1] = random.randint(100, frame_height - 100)
            pipe[2] = False  # Reset passed flag

    # Draw yellow circle at the current position
    cv2.circle(frame, (bird_x, circle_pos[1]), bird_radius, (0, 255, 255), -1)

    # Draw score
    cv2.putText(frame, f"Score: {score}", (10, 40), font, 1.2, (255, 255, 255), 3)

    # If collision, show game over and break
    if collision:
        cv2.putText(frame, "GAME OVER", (180, 240), font, 2, (0, 0, 255), 5)
        cv2.imshow('AprilTag Detection', frame)
        cv2.waitKey(2000)
        # Show final score and prompt for restart or quit
        while True:
            frame_copy = frame.copy()
            cv2.putText(frame_copy, f"Final Score: {score}", (180, 300), font, 1.2, (255, 255, 255), 3)
            cv2.putText(frame_copy, "Press 'r' to restart or 'q' to quit", (60, 400), font, 0.8, (255, 255, 0), 2)
            cv2.imshow('AprilTag Detection', frame_copy)
            key = cv2.waitKey(0) & 0xFF
            if key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                exit()
            elif key == ord('r'):
                # Reset game state
                pipes = []
                for i in range(NUM_PIPES):
                    x = 640 + i * PIPE_SPACING
                    gap_y = random.randint(100, 380)
                    pipes.append([x, gap_y, False])
                circle_pos = [bird_x, frame_height // 2]
                score = 0
                break
        continue

    cv2.imshow('AprilTag Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Add a main guard for best practice
if __name__ == "__main__":
    pass  # The game runs on import, but this is a placeholder for future modularization
