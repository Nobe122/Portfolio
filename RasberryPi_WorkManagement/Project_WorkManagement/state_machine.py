from enum import Enum

class State(Enum):
    IDLE = 0
    WORKING = 1
    BREAK = 2
    FINISHED = 3

class StateMachine:
    def __init__(self):
        self.state = State.IDLE

    def update(self, face_present, gesture=None):
        prev = self.state

        if self.state == State.IDLE:
            if face_present:
                self.state = State.WORKING
                return True, self.state, "FACE_DETECTED"

        elif self.state == State.WORKING:
            if not face_present: # ON
                self.state = State.FINISHED
                return True, self.state, "FACE_LOST"
            if gesture == "PALM":
                self.state = State.BREAK
                return True, self.state, "PALM"
            if gesture == "PEACE":
                self.state = State.FINISHED
                return True, self.state, "PEACE"

        elif self.state == State.BREAK:
            if gesture == "FIST":
                self.state = State.WORKING
                return True, self.state, "FIST"

        return False, self.state, None
