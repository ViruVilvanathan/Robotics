
class SafetyManager:

    def __init__(self) -> None:
        self.power_status: bool = True
        self.perception_status: bool = True
        self.navigable_path: bool = True
        self.guidance_status: bool = True
        self.localization_status: bool = True
        self._estop_status: bool = False

    @property
    def estop_engaged(self) -> bool:
        return self._estop_status

    def motion_allowed(self) -> tuple[bool, str]:
        if self.estop_engaged:
            return False, "E-stop is engaged."
        if not self.power_status:
            return False, "Power system failure detected."
        if not self.perception_status:
            return False, "Perception system failure detected."
        if not self.navigable_path:
            return False, "No navigable path detected."
        if not self.guidance_status:
            return False, "Guidance system failure detected."
        if not self.localization_status:
            return False, "Localization system failure detected."
        return True, "All systems are operational."

    def engage_estop(self) -> None:
        self._estop_status = True

    def release_estop(self) -> None:
        self._estop_status = False

'''
Atlas = SafetyManager()  # Singleton instance of SafetyManager
print(Atlas.engage_estop())  # Engage E-stop for testing purposes
print(Atlas.motion_allowed())  # Check if motion is allowed (should return False due to E-stop)
print(Atlas.release_estop())  # Release E-stop
print(Atlas.motion_allowed())  # Check if motion is allowed (should return True now)
'''
