import cv2
import numpy as np
from pupil_apriltags import Detector
from symbol_recognition import recognize_symbol

# Game settings
PLAYER_HP = [10, 10]
ATTACKS = {
    'circle': ('Heal', lambda hp, opp: (min(hp+3, 10), opp)),
    'triangle': ('Fireball', lambda hp, opp: (hp, max(opp-4, 0))),
    'line': ('Slash', lambda hp, opp: (hp, max(opp-2, 0))),
}

font = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0)
detector = Detector(families='tag36h11')

frame_width, frame_height = 640, 480

turn = 0  # 0: Player 1, 1: Player 2
recording = False
path = []
message = ''

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (frame_width, frame_height))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(gray)
    # Mirror the frame for display
    display_frame = cv2.flip(frame, 1)

    # Draw AprilTag and record path if needed
    if detections:
        det = detections[0]
        center = det.center.astype(int)
        # Mirror the center x-coordinate for display
        mirrored_center = np.array([frame_width - center[0], center[1]])
        cv2.circle(display_frame, tuple(mirrored_center), 10, (0, 255, 0), 2)
        if recording:
            path.append(mirrored_center)
        cv2.putText(display_frame, f"Tag {det.tag_id}", (mirrored_center[0]-20, mirrored_center[1]-20), font, 0.7, (0,255,0), 2)

    # Draw path
    if len(path) > 1:
        for i in range(1, len(path)):
            cv2.line(display_frame, tuple(path[i-1]), tuple(path[i]), (255, 0, 0), 2)

    # UI
    cv2.putText(display_frame, f"Player 1 HP: {PLAYER_HP[0]}", (10, 30), font, 0.8, (255,255,255), 2)
    cv2.putText(display_frame, f"Player 2 HP: {PLAYER_HP[1]}", (350, 30), font, 0.8, (255,255,255), 2)
    cv2.putText(display_frame, f"Player {turn+1}'s turn", (200, 60), font, 0.8, (255,255,0), 2)
    if message:
        cv2.putText(display_frame, message, (100, 440), font, 1.0, (0,0,255), 3)

    cv2.imshow('AprilTag Combat', display_frame)
    key = cv2.waitKey(1) & 0xFF

    # Spacebar to start/stop drawing
    if key == 32:  # Space pressed
        if not recording:
            path = []
            recording = True
            message = 'Drawing...'
    elif key == ord('s') and recording:
        # 's' to stop drawing
        recording = False
        if len(path) > 10:
            symbol = recognize_symbol(path)
            if symbol in ATTACKS:
                attack_name, attack_fn = ATTACKS[symbol]
                PLAYER_HP[turn], PLAYER_HP[1-turn] = attack_fn(PLAYER_HP[turn], PLAYER_HP[1-turn])
                message = f"{attack_name}!"
            else:
                message = 'Unrecognized symbol!'
            # Switch turn
            turn = 1 - turn
        else:
            message = 'Draw a bigger symbol!'
        path = []
    elif key == ord('q'):
        break

    # Check for game over
    if PLAYER_HP[0] <= 0 or PLAYER_HP[1] <= 0:
        winner = 2 if PLAYER_HP[0] <= 0 else 1
        message = f"Player {winner} wins!"
        cv2.imshow('AprilTag Combat', display_frame)
        cv2.waitKey(2000)
        break

cap.release()
cv2.destroyAllWindows() 