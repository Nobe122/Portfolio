import cv2
import time

class FaceDetector:
    def __init__(self, timeout=5.0):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_eye.xml"
        )

        self.last_seen_time = None
        self.timeout = timeout

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,      # 小さめに
            minNeighbors=4,
            minSize=(40, 40)      # ← ここが重要
        )

        now = time.time()
        face_present = False

        for (x, y, w, h) in faces:
            face_present = True
            self.last_seen_time = now

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            eyes = self.eye_cascade.detectMultiScale(
                roi_gray, 1.1, 5, minSize=(15, 15)
            )
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(
                    roi_color, (ex, ey),
                    (ex+ew, ey+eh), (0, 255, 0), 1
                )

        if face_present:
            return True

        if self.last_seen_time is None:
            return False

        return (now - self.last_seen_time) < self.timeout
