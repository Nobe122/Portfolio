import cv2
import time
from face_detector import FaceDetector
from state_machine import StateMachine, State
from work_logger import WorkLogger
from hand_detector import HandDetector
from rpicam import RpiCam
#import speaker_ori as sp
import threading
import sys
import subprocess
import numpy as np
#from picamera2 import Picamera2
import system_call as sp

"""latest_gesture = None

def input_thread():
    global latest_gesture
    while True:
        key = sys.stdin.readline().strip()
        if key == "p":
            latest_gesture = "PALM"
        elif key == "f":
            latest_gesture = "FIST"
        elif key == "e":
            latest_gesture = "PEACE"

threading.Thread(target=input_thread, daemon=True).start()"""

# rpicam
"""picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(
    main={"size": (320, 240)}
))
picam2.start()"""


WIDTH, HEIGHT = 320, 240
FRAME_SIZE = WIDTH * HEIGHT * 3 // 2  # yuv420

cmd = [
    "rpicam-vid",
    "--codec", "yuv420",
    "--width", str(WIDTH),
    "--height", str(HEIGHT),
    "--framerate", "15",
    "-t", "0s",
    "--inline",
    "--nopreview",
    "-o", "-"
]

# p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

#cam = RpiCam(WIDTH, HEIGHT)
cam = RpiCam()

# cap = cv2.VideoCapture(0)
face_detector = FaceDetector()
state_machine = StateMachine()
logger = WorkLogger()
hand_detector = HandDetector()

finished_time = None    # 作業時間の記録
face_buffer = None   # 判定中の顔を保持
face_start_time = None   # 顔の判定時間の始まり
face_lock = False    # 顔の判定制御フラッグ
confirmed_face = None   # 一定時間判定した後の顔結果
FACE_HOLD_TIME = 3.0  # 3秒（30fpsなら約90フレーム）
gesture_buffer = None   # 判定中のジェスチャーを保持
gesture_start_time = None   # ジェスチャーの判定時間の始まり
gesture_lock = False    # ジェスチャーの判定制御フラッグ
confirmed_gesture = None   # 一定時間判定した後のジェスチャー結果
GESTURE_HOLD_TIME = 1.0  # 1秒（30fpsなら約30フレーム）
lock_release_time = None    # ジェスチャーと顔判定開始の時間

frame_count = 0

"""    raw = p.stdout.read(FRAME_SIZE)
    if len(raw) != FRAME_SIZE:
        break

    yuv = np.frombuffer(raw, dtype=np.uint8).reshape((HEIGHT * 3 // 2, WIDTH))
    frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)"""

print("System started")
while True:
    ret, frame = cam.read()
    if not ret:
        break

    # rpicam
    # frame = picam2.capture_array()

    frame_count += 1
    if frame_count % 2 == 1:
        cv2.imshow("camera", frame)
        #if cv2.waitKey(1) & 0xFF == 27:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        face = face_detector.detect(frame)
        gesture = hand_detector.detect(frame)

    # 顔判定
    if face_lock:
        if time.time() >= lock_release_time:
            face_lock = False
        else:
            face = None  # 判定だけ無効化
    else:
        if face is not None:
            if face != face_buffer:
                face_buffer = face
                face_start_time = time.time()
            else:
                if time.time() - face_start_time >= FACE_HOLD_TIME:
                    confirmed_face = face
                else:
                    confirmed_face = None
        else:
            face_buffer = None
            face_start_time = None
            confirmed_face = None

    # ジェスチャー判定
    if gesture_lock:
        if time.time() >= lock_release_time:
            gesture_lock = False
        else:
            gesture = None  # 判定だけ無効化
    else:
        if gesture is not None:
            if gesture != gesture_buffer:
                gesture_buffer = gesture
                gesture_start_time = time.time()
            else:
                if time.time() - gesture_start_time >= GESTURE_HOLD_TIME:
                    confirmed_gesture = gesture
                else:
                    confirmed_gesture = None
        else:
            gesture_buffer = None
            gesture_start_time = None
            confirmed_gesture = None

    changed, state, reason = state_machine.update(confirmed_face, confirmed_gesture)

    # 状態遷移
    if changed:
        print(f"[DEBUG] State -> {state.name}, reason={reason}")
        gesture_lock = True
        face_lock = True
        lock_release_time = None

        if state == State.WORKING:
            sp.read_str("Work has started.")
            logger.start()
            lock_release_time = time.time() + 1.0

        elif state == State.BREAK:
            sp.read_str("Please take a break.")
            lock_release_time = time.time() + 1.0

        elif state == State.FINISHED:
            sp.read_str("Good job. Work finished.")
            logger.end()
            finished_time = time.time()
            lock_release_time = time.time() + 3.0

    if state == State.FINISHED:
        if time.time() - finished_time > 5:
            break
            print("END")

    # 左上デバッグ
    if gesture:
        cv2.putText(
            frame,
            f"Gesture: {gesture}",
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
    if state:
        cv2.putText(
            frame,
            f"Gesture: {state}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

cam.release()
cv2.destroyAllWindows()
