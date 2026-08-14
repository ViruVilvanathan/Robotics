from atlas.geometry.positionvector import Position, Vector
from atlas.orientation.rotations import Rotation
from atlas.orientation.pose import Pose
import numpy as np

class MotionUpdate:

    def __init__(self, Pose: Pose) -> None:
        self.position = Pose.position
        self.orientation = Pose.orientation
        self.pose = Pose

    def update_pose(self, velocity: Vector, ang_velocity_z: float, dt: float) -> Pose:
        #Update the pose of the robot with new position and orientation
        
        delta_position_body = Vector(velocity.x * dt, velocity.y * dt, velocity.z * dt)
        delta_position_world = self.pose.body_vector_to_world(delta_position_body)

        new_position = Position(
            self.position.x + delta_position_world.x,
            self.position.y + delta_position_world.y,
            self.position.z + delta_position_world.z
        )

        delta_theta = ang_velocity_z * dt
        new_orientation = self.orientation.rotate_body('z', delta_theta)

        return Pose(new_position, new_orientation)

