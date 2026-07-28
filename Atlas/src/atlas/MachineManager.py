from state_machine import StateMachine


class MachineManager:
    def __init__(self, name):
        self.name = name 
        self.mission_loaded = False
        self.mission_running = False
        self.mission = None
        self.state_machine = StateMachine()
        self.position = (0, 0, 0)  # x, y, z coordinates
   

    def change_state(self, requested_state):
        if self.check_safety():
            return self.state_machine.request_transition(requested_state)


    def load_mission(self, mission):
        if self.mission_running:
            print("Cannot load a new mission while another mission is running.")
            return

        self.mission = mission
        self.mission_loaded = True
        print(f"Mission '{mission}' loaded for robot '{self.name}'.")

    def start_mission(self):
        if not self.mission_loaded:
            print(f"No mission loaded for robot '{self.name}'. Cannot start mission.")
            return

        transition_result = self.change_state("AUTO")
        if transition_result["success"]:
            print(f"Robot '{self.name}' is starting the mission '{self.mission}'.")
            self.mission_running = True
        else:
            print(f"Failed to start mission: {transition_result['reason']}")

    def stop_mission(self):
        transition_result = self.change_state("IDLE")
        if transition_result["success"]:
            print(f"Robot '{self.name}' has stopped the mission '{self.mission}'.")
            self.mission_running = False
        else:
            print(f"Failed to stop mission: {transition_result['reason']}")

    def get_status(self):
        return {
            "name": self.name,
            "current_state": self.state_machine.current_state,
            "mission_loaded": self.mission_loaded,
            "mission_running": self.mission_running,
            "position": self.position,
        }
    def check_safety(self):
        return True  # Placeholder for actual safety checks 
    #checks for safety conditions and returns True if safe, False otherwise

            
