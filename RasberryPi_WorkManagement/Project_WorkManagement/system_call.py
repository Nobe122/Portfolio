import subprocess
import time

def read_str(text):
    subprocess.Popen(
        ["espeak-ng", "-v", "en-us", "-s", "150", ""],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(0.1)
    subprocess.Popen(
        ["espeak-ng", "-v", "en-us", "-s", "150", text],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
