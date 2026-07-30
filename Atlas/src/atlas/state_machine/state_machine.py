from enum import StrEnum

class RobotState(StrEnum):
    OFF = "OFF"
    IDLE = "IDLE"
    MANUAL = "MANUAL"
    AUTO = "AUTO"       
    E_STOP = "E_STOP"
    
class StateMachine:
    def __init__(self):
        self._current_state = RobotState.OFF
        self.previous_state = RobotState.OFF
        self.success = False
        self.reason = ""

        self.allowed_transitions = {
            RobotState.OFF: [RobotState.IDLE],
            RobotState.IDLE: [RobotState.MANUAL, RobotState.AUTO],
            RobotState.MANUAL: [RobotState.IDLE],
            RobotState.AUTO: [RobotState.IDLE, RobotState.E_STOP],
            RobotState.E_STOP: [RobotState.IDLE],
        }
    @property
    def current_state(self):
        return self._current_state

    def _state_transition(self, requested_state):
        self.previous_state = self.current_state
        self._current_state = requested_state


    def request_transition(self, requested_state):
        if requested_state in self.allowed_transitions[self.current_state]:
            self._state_transition(requested_state)
            self.success = True
            self.reason = "Transition from {} to {} successful.".format(self.previous_state, requested_state)

        elif requested_state == self.current_state:
            self.success = False
            self.reason = "Already in {} state. No transition needed.".format(self.current_state)
        else:
            self.success = False
            self.reason = f"Transition from {self.current_state} to {requested_state} is not allowed."

        return {
            "success": self.success,
            "previous_state": self.previous_state,
            "requested_state": requested_state,
            "current_state": self.current_state,
            "reason": self.reason,
        }

if __name__ == "__main__":
    atlas_state = StateMachine()

    print(atlas_state.request_transition("AUTO"))
    print(atlas_state.request_transition("IDLE"))
    print(atlas_state.request_transition("IDLE"))
    print(atlas_state.request_transition("MANUAL"))
    print(atlas_state.request_transition("AUTO"))
    print(atlas_state.request_transition("IDLE"))
    print(atlas_state.request_transition("E_STOP"))
