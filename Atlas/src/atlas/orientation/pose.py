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