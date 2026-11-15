"""Fixed-step planar simulation using existing Atlas guidance, kinematics and safety."""
import math
from dataclasses import dataclass, field
from atlas.geometry.positionvector import Position, Vector
from atlas.orientation.pose import Pose
from atlas.orientation.rotations import Rotation
from atlas.guidance.goalcontroller import GoToGoalController
from atlas.kinematics.motionupdate import MotionUpdate
from atlas.machine_manager.machine_manager import MachineManager
from .maps import ObstacleMap

@dataclass
class RobotAgent:
    name: str
    pose: Pose
    goal: Position
    radius: float = 0.2
    max_speed: float = 1.0
    max_turn_rate: float = 2.0
    status: str = "idle"
    manager: MachineManager = field(init=False, repr=False)
    trajectory: list = field(default_factory=list, repr=False)

    def __post_init__(self):
        if not self.name or self.radius <= 0 or self.max_speed <= 0 or self.max_turn_rate <= 0:
            raise ValueError("Invalid robot configuration")
        self.manager = MachineManager(self.name)
        self.manager.initialize_robot(self.name, "go_to_goal", (self.pose.position.x, self.pose.position.y, 0))
        self.manager.start_mission()
        if not self.manager.mission_running:
            raise ValueError("Robot could not enter AUTO")
        self.status = "moving"
        self.trajectory.append((self.pose.position.x, self.pose.position.y))

    @classmethod
    def from_dict(cls, data):
        x, y = data["start"][:2]
        gx, gy = data["goal"][:2]
        theta = float(data.get("heading", 0.0))  # radians
        return cls(data["name"], Pose(Position(x, y, 0), Rotation.rotation_z(theta)),
                   Position(gx, gy, 0), float(data.get("radius", 0.2)),
                   float(data.get("max_speed", 1.0)), float(data.get("max_turn_rate", 2.0)))

class SimulationWorld:
    def __init__(self, obstacle_map: ObstacleMap, robots: list[RobotAgent], dt=0.1, goal_tolerance=0.15):
        if dt <= 0 or not math.isfinite(dt) or goal_tolerance <= 0:
            raise ValueError("Invalid simulation timestep/tolerance")
        self.map, self.robots, self.dt, self.goal_tolerance = obstacle_map, robots, dt, goal_tolerance
        self.time = 0.0
        names = [r.name for r in robots]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate robot names")
        for robot in robots:
            p = robot.pose.position
            if self.map.collides(p.x, p.y, robot.radius):
                raise ValueError(f"Robot {robot.name} starts in collision")
            if self.map.collides(robot.goal.x, robot.goal.y, robot.radius):
                raise ValueError(f"Robot {robot.name} goal is obstructed")
        for i, a in enumerate(robots):
            for b in robots[i+1:]:
                if math.hypot(a.pose.position.x-b.pose.position.x, a.pose.position.y-b.pose.position.y) < a.radius+b.radius:
                    raise ValueError("Overlapping robot starts")
        self.controller = GoToGoalController(0.5, 1.5)

    @classmethod
    def from_dict(cls, config):
        return cls(ObstacleMap.from_dict(config["map"]),
                   [RobotAgent.from_dict(r) for r in config["robots"]],
                   float(config.get("dt", 0.1)), float(config.get("goal_tolerance", 0.15)))

    def snapshot(self):
        return {"time": self.time, "robots": [
            {"name": r.name, "x": float(r.pose.position.x), "y": float(r.pose.position.y),
             "heading": float(math.atan2(r.pose.orientation.rotation_matrix[1,0], r.pose.orientation.rotation_matrix[0,0])),
             "status": r.status, "goal": [r.goal.x, r.goal.y]} for r in self.robots]}

    def step(self):
        # Sequential deterministic update. Future versions can replace with simultaneous conflict resolution.
        for r in self.robots:
            if r.status != "moving":
                continue
            p = r.pose.position
            if p.distance_to(r.goal) <= self.goal_tolerance:
                r.status = "reached"
                r.manager.stop_mission()
                continue
            safe, _ = r.manager.check_safety()
            if not safe:
                r.status = "stopped_safety"
                r.manager.mission_monitor()
                continue
            velocity, turn = self.controller.linearpcontroller(r.pose, r.goal)
            speed = min(max(float(velocity.x), 0.0), r.max_speed)
            turn = max(-r.max_turn_rate, min(r.max_turn_rate, float(turn)))
            candidate = MotionUpdate(r.pose).update_pose(Vector(speed, 0, 0), turn, self.dt)
            q = candidate.position
            blocked = not self.map.path_clear(p.x, p.y, q.x, q.y, r.radius)
            for other in self.robots:
                if other is r:
                    continue
                if not blocked and not self._clear_of_robot(p, q, r.radius, other):
                    blocked = True
            if blocked:
                r.status = "blocked"
                r.manager.safety_manager.navigable_path = False
                r.manager.mission_monitor()
                continue
            r.pose = candidate
            r.manager.position = (q.x, q.y, q.z)
            r.trajectory.append((q.x, q.y))
            if q.distance_to(r.goal) <= self.goal_tolerance:
                r.status = "reached"
                r.manager.stop_mission()
        self.time += self.dt
        return self.snapshot()

    @staticmethod
    def _clear_of_robot(p, q, radius, other):
        ox, oy = other.pose.position.x, other.pose.position.y
        dx, dy = q.x-p.x, q.y-p.y
        length_sq = dx*dx + dy*dy
        t = 0 if length_sq == 0 else max(0, min(1, ((ox-p.x)*dx+(oy-p.y)*dy)/length_sq))
        return math.hypot(p.x+t*dx-ox, p.y+t*dy-oy) >= radius + other.radius

    def run(self, steps):
        if steps < 0:
            raise ValueError("steps must be nonnegative")
        for _ in range(steps):
            self.step()
        return self.snapshot()
