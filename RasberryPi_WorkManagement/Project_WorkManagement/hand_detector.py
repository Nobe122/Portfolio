# hand_detector.py
import mediapipe as mp
import cv2

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        if not result.multi_hand_landmarks:
            return None

        landmarks = result.multi_hand_landmarks[0]
        handedness = result.multi_handedness[0].classification[0].label
        return self._classify_gesture(landmarks, handedness)

    def _classify_gesture(self, landmarks, handedness):
        fingers = self._finger_states(landmarks, handedness)

        thumb, index, middle, ring, pinky = fingers

        # --- PALM ---
        if fingers.count(True) == 5:
            return "PALM"

        # --- FIST ---
        if fingers.count(True) == 0:
            return "FIST"

        # --- PEACE ---
        if index and middle and not ring and not pinky:
            return "PEACE"

        return None


    def _finger_states(self, landmarks, handedness):
    # lm.landmark でアクセス
        landmarks = landmarks.landmark

        fingers = []

        # --- 親指 ---
        thumb_tip = landmarks[4]
        thumb_ip  = landmarks[3]
        if handedness == "Right":
            fingers.append(thumb_tip.x < thumb_ip.x)
        else:  # Left
            fingers.append(thumb_tip.x > thumb_ip.x)

        # --- 人差し指 ---
        fingers.append(landmarks[8].y < landmarks[6].y)

        # --- 中指 ---
        fingers.append(landmarks[12].y < landmarks[10].y)

        # --- 薬指 ---
        fingers.append(landmarks[16].y < landmarks[14].y)

        # --- 小指 ---
        fingers.append(landmarks[20].y < landmarks[18].y)

        return fingers

