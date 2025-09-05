import time
import mediapipe as mp
import cv2
import numpy as np
import serial
import math
from collections import deque

# Connect to Arduino on COM9 at 9600 baud
arduino = serial.Serial("COM9", 9600)
time.sleep(2)  # give Arduino some time to reset after serial connection

# Initialize Mediapipe holistic model (tracks pose + hands + face)
mp_sol = mp.solutions.holistic
mp_holstic = mp_sol.Holistic(
    min_tracking_confidence=0.8,
    min_detection_confidence=0.8,
    refine_face_landmarks=True
)
mp_util = mp.solutions.drawing_utils

# Moving average buffers to smooth noisy sensor readings
claw_arr = deque(maxlen=5)
rshoulder_arr = deque(maxlen=5)
lshoulder_arr = deque(maxlen=5)
base_arr = deque(maxlen=5)

# Default starting values for each joint
claw_dist = 40
r_shoulder = 100
l_shoulder = 140
base_dist = 90


def get_distance(x1, x2, y1, y2):
    """Helper function to calculate Euclidean distance between 2 points"""
    distance = math.hypot(x2 - x1, y2 - y1)
    return distance


# Open webcam
cam = cv2.VideoCapture(0)

while True:
    success, frame = cam.read()
    h, w, _ = frame.shape
    if success:
        # Convert to RGB for Mediapipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = mp_holstic.process(frame_rgb)

        # --- Detect body pose (shoulders, etc.) ---
        if result.pose_landmarks:
            lm = result.pose_landmarks.landmark
            mp_util.draw_landmarks(frame, result.pose_landmarks, mp_sol.POSE_CONNECTIONS)

            # Right shoulder and wrist
            shoulderX, shoulderY = int(lm[12].x * w), int(lm[12].y * h)
            wristX, wristY = int(lm[16].x * w), int(lm[16].y * h)

            # Distance between wrist and shoulder → right shoulder angle
            rshoulder_arr.append(get_distance(shoulderX, wristX, shoulderY, wristY))
            r_shoulder = int(min(max(
                np.interp(np.mean(rshoulder_arr), (70, 290), (40, 140)), 40), 140))

            # Vertical offset wrist vs shoulder → left shoulder mapping
            lshoulder_arr.append(wristY - shoulderY)
            l_shoulder = int(min(max(
                np.interp(np.mean(lshoulder_arr), (-70, 70), (170, 100)), 100), 170))

            # Debug: show landmark indices on screen
            for i in range(33):
                x, y = int(lm[i].x * w), int(lm[i].y * h)
                cv2.putText(frame, f"{i}", (x, y),
                            cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

        # --- Detect right hand (for claw + base rotation) ---
        if result.right_hand_landmarks:
            cl = result.right_hand_landmarks.landmark
            mp_util.draw_landmarks(frame, result.right_hand_landmarks, mp_sol.HAND_CONNECTIONS)

            # Thumb and index tip → claw open/close
            thumbX, thumbY = int(cl[4].x * w), int(cl[4].y * h)
            indexX, indexY = int(cl[8].x * w), int(cl[8].y * h)

            # Wrist y-pos vs thumb y-pos → base rotation
            wristY = int(cl[0].y * h)
            claw_arr.append(get_distance(thumbX, indexX, thumbY, indexY))
            base_val = wristY - thumbY
            base_arr.append(base_val)

            # Clamp + smooth claw distance
            claw_dist = int(min(max(
                np.interp(np.mean(claw_arr), (0, 150), (40, 80)), 40), 80))

            # Clamp + smooth base rotation
            base_dist = int(min(max(
                np.interp(np.mean(base_arr), (-40, 80), (0, 180)), 0), 180))

            # Draw helper line between thumb and index
            cv2.line(frame, (thumbX, thumbY), (indexX, indexY), (0, 255, 0), 2)

        # Debug output (send to Arduino as well)
        print("claw: ", claw_dist)
        print("base val:", base_dist)
        print("right shoulder: ", r_shoulder)
        print("left shoulder: ", l_shoulder)

        # Send formatted string to Arduino
        arduino.write(f"{claw_dist}:{r_shoulder}:{l_shoulder}:{base_dist}\n".encode())

    # Flip frame for natural mirror view
    frame = cv2.flip(frame, 1)
    cv2.imshow("robo arm", frame)

    # Exit on ESC key
    if cv2.waitKey(1) & 0xff == 27:
        break

# Cleanup
arduino.close()
cv2.destroyAllWindows()
cam.release()
