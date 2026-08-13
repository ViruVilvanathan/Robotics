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

    def pose_transform_body_to_world(self) -> np.ndarray:
        #Returns the 4x4 transformation matrix representing the pose for body to world transformation
        transformation_matrix = np.eye(4)
        transformation_matrix[:3, :3] = self.orientation.rotation_matrix
        transformation_matrix[:3, 3] = [self.position.x, self.position.y, self.position.z]
        return transformation_matrix

    def inverse_pose_transform_world_to_body(self) -> np.ndarray:
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
        #returns the 4x4 matrix representing the inverse pose transformation from world to body frame
        return transformation_matrix

    def object_pose_world_from_bodyframe(self, object_position_body: Position) -> Position:
        """Given an object's position in the body frame, compute its position in the world frame."""
        # Convert the object's position in the body frame to a homogenous vector
        object_vector_body = np.array([
            object_position_body.x,
            object_position_body.y,
            object_position_body.z,
            1
        ])

        # Rotate the vector to the world frame
        object_vector_world = self.pose_transform_body_to_world() @ object_vector_body

        # Translate to get the object's position in the world frame
        object_position_world = Position(
            object_vector_world[0],
            object_vector_world[1],
            object_vector_world[2]
        )

        return object_position_world

    def point_pose_world_to_bodyframe(self, point_position_world: Position) -> Position:
        #Given a point's position in the world frame, compute its position in the body frame.
        # Convert the point's position in the world frame to a homogenous vector
        point_vector_world = np.array([
            point_position_world.x,
            point_position_world.y,
            point_position_world.z,
            1
        ])

        # Apply the inverse transformation to get the point's position in the body frame
        point_vector_body = self.inverse_pose_transform_world_to_body() @ point_vector_world

        # Create a Position object for the point in the body frame
        point_position_body = Position(
            point_vector_body[0],
            point_vector_body[1],
            point_vector_body[2]
        )

        return point_position_body

    def body_vector_to_world(self, body_vector: Vector) -> Vector:
        # Convert the body vector to a numpy array
        body_vector_np = np.array([body_vector.x, body_vector.y, body_vector.z, 0])  # Homogeneous coordinates for vector

        # Rotate the vector to the world frame
        world_vector_np = self.pose_transform_body_to_world() @ body_vector_np

        # Create a new Vector object for the world vector
        world_vector = Vector(world_vector_np[0], world_vector_np[1], world_vector_np[2])

        return world_vector

    def world_vector_to_body(self, world_vector: Vector) -> Vector:
        # Convert the world vector to a numpy array
        world_vector_np = np.array([world_vector.x, world_vector.y, world_vector.z, 0])  # Homogeneous coordinates for vector

        # Apply the inverse transformation to get the vector in the body frame
        body_vector_np = self.inverse_pose_transform_world_to_body() @ world_vector_np

        # Create a new Vector object for the body vector
        body_vector = Vector(body_vector_np[0], body_vector_np[1], body_vector_np[2])

        return body_vector

    