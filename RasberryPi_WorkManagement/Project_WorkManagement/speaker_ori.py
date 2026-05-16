import pyttsx3
import threading
import queue

class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init(driverName="espeak")
        self.engine.setProperty("rate", 150)
        self.q = queue.Queue()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        while True:
            text = self.q.get()
            if text is None:
                break
            self.engine.say(text)
            self.engine.runAndWait()

    def speak(self, text):
        self.q.put(text)

speaker = Speaker()

def read_str(text):
    speaker.speak(text)
