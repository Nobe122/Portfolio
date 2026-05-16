import subprocess
import numpy as np
import cv2

#WIDTH, HEIGHT = 320, 240
WIDTH, HEIGHT = 640, 480
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

class RpiCam:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.frame_size = width * height * 3 // 2
        self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    def read(self):
        raw = self.p.stdout.read(self.frame_size)
        if len(raw) != self.frame_size:
            return False, None
        yuv = np.frombuffer(raw, dtype=np.uint8).reshape((self.height * 3 // 2, self.width))
        frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
        return True, frame

    def release(self):
        if self.p.poll() is None:  # まだ動いているなら
            self.p.terminate()
            try:
                self.p.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.p.kill()
