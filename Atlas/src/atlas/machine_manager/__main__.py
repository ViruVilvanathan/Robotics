from atlas.machine_manager.machine_manager import MachineManager

def __main__():
        Atlas = MachineManager("Atlas")  # Singleton instance of MachineManager
        print(Atlas.initialize_robot("Atlas", "Exploration", (0, 0, 0)))  # Initialize the robot with a name, mission, and position
        print(Atlas.get_machine_status())  # Get the machine status
        print(Atlas.start_mission())  # Start the mission
        print(Atlas.get_machine_status())  # Get the machine status after starting the mission
        print(Atlas.mission_monitor())  # Monitor the mission (should be healthy)
        Atlas.safety_manager.power_status = False  # Simulate a power system failure
        print(Atlas.mission_monitor())  # Monitor the mission (should trigger E-stop)
        print(Atlas.get_machine_status())  # Get the machine status after E-stop
        print(Atlas.stop_mission())  # Attempt to stop the mission (should fail due to E-stop)
        print(Atlas.get_machine_status())  # Get the machine status after attempting to stop the mission
        print(Atlas.mission_monitor())  # Attempt to change state to IDLE (should fail due to E-stop)
        print(Atlas.unload_mission())  # Attempt to unload the mission (should fail due to E-stop)
        print(Atlas.get_machine_status())  # Get the machine status after attempting to unload the mission
        print(Atlas.initialize_robot("Atlas", "Exploration2", (0, 0, 0)))  # Attempt to change state to IDLE (should fail due to E-stop)
        print(Atlas.get_machine_status())  # Get the machine status after attempting to re-initialize the robot
        print(Atlas.start_mission())    
        print(Atlas.get_machine_status())  # Get the machine status after attempting to start a new mission
        print(Atlas.mission_monitor())  # Monitor the mission (should be healthy)
        
if __name__ == "__main__":

    __main__()