import csv
import time
from datetime import datetime

class WorkLogger:
    def __init__(self, path="/home/kazuki/VScode_saves/Project/work_log.csv"):
        self.path = path
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def end(self):
        end_time = time.time()
        duration = int(end_time - self.start_time)

        with open(self.path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d"),
                duration
            ])
