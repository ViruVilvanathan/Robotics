from atlas.state_machine import StateMachine
from atlas.safety_manager import SafetyManager


class MachineManager:
    def __init__(self, name):
        self.name = name 
        self.mission_loaded = False
        self.mission_running = False
        self.mission = None
        self.state_machine = StateMachine()
        self.safety_manager = SafetyManager()
        self.position = (0, 0, 0)  # x, y, z coordinates
    
    def request_auto(self) -> dict:
        is_safe, reason = self.check_safety()
        if self.mission_loaded and is_safe:
            return self.change_state("AUTO")
        else:
            return {"success": False, "reason": reason}

    def change_state(self, requested_state) -> dict:
        return self.state_machine.request_transition(requested_state)

    def mission_monitor(self) -> str:
        if not self.mission_running:
            return "Mission not running."
        is_safe, reason = self.check_safety()
        if is_safe:
            return f"Mission '{self.mission}' for robot '{self.name}' healthy."
        else:
            self.change_state("E_STOP")
            self.safety_manager.engage_estop()
            if self.mission_running:
                self.mission_running = False
                return f"Mission Aborted for robot '{self.name}'."
            else:
                return f"Mission not running"

    def load_mission(self, mission) -> None:
        self.mission = mission
        self.mission_loaded = True

    def initialize_robot(self, name, mission, position) -> str:
        self.name = name
        self.position = position
        self.load_mission(mission)
        self.reset_safety()
        self.change_state("IDLE")
        return f"Robot '{self.name}' initialized with mission '{self.mission}' at position {self.position}."

    def start_mission(self) -> str:
        if not self.mission_loaded:
            return f"No mission loaded for robot '{self.name}'. Cannot start mission."

        transition_result = self.request_auto()
        if transition_result["success"]:
            self.mission_running = True
            return f"Robot '{self.name}' is starting the mission '{self.mission}'."   
        else:
            return f"Failed to start mission: {transition_result['reason']}"

    def stop_mission(self) -> str:
        transition_result = self.change_state("IDLE")
        if transition_result["success"]:
            self.mission_running = False
            return f"Robot '{self.name}' has stopped the mission '{self.mission}'."
        else:
            return f"Failed to stop mission: {transition_result['reason']}"

    def unload_mission(self) -> str:
        if self.mission_running:
            return f"Cannot unload mission '{self.mission}' while it is running for robot '{self.name}'."
        self.mission = None
        self.mission_loaded = False
        return f"Mission unloaded for robot '{self.name}'."

    def get_machine_status(self) -> dict:
        return {
            "name": self.name,
            "current_state": self.state_machine.current_state,
            "mission_loaded": self.mission_loaded,
            "mission_running": self.mission_running,
            "position": self.position,
        }

    def check_safety(self) -> tuple[bool, str]:
        return self.safety_manager.motion_allowed()

    def reset_safety(self) -> None:
        self.safety_manager.release_estop()



