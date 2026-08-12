import numpy as np

from atlas.geometry.positionvector import Position, Vector
from atlas.orientation.rotations import Rotation


class Pose:
    def __init__(self, position: Position, orientation: Rotation) -> None:
        self.position = position
        self.orientation = orientation

    def world_to_body(self, goal: Position) -> Vector:
        displacement_world = self.position.vector_to(goal)

        v_world = np.array([
            displacement_world.x,
            displacement_world.y,
            displacement_world.z
        ])

        v_body = self.orientation.rotation_matrix.T @ v_world

        return Vector(
            v_body[0],
            v_body[1],
            v_body[2]
        )

    def pose_transform(self) -> np.ndarray:
        """Returns the 4x4 transformation matrix representing the pose."""
        transformation_matrix = np.eye(4)
        transformation_matrix[:3, :3] = self.orientation.rotation_matrix
        transformation_matrix[:3, 3] = [self.position.x, self.position.y, self.position.z]
        return transformation_matrix

    def inverse_pose_transform(self) -> np.ndarray:
        R = self.orientation.rotation_matrix

        t = np.array([
            self.position.x,
            self.position.y,
            self.position.z
        ])

        R_inv = R.T

        t_inv = -R_inv @ t

        transformation_matrix = np.eye(4)
        transformation_matrix[:3, :3] = R_inv
        transformation_matrix[:3, 3] = t_inv

        return transformation_matrix