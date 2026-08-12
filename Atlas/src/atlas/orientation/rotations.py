import numpy as np
from atlas.geometry.positionvector import Position, Vector

class Rotation:

    def __init__(self, rotation_matrix: np.ndarray = None) -> None:
        if rotation_matrix is None:
            self.rotation_matrix = np.eye(3)  # Identity matrix for no rotation
        else:
            self.rotation_matrix = rotation_matrix

    @staticmethod   
    def rotation_z(theta: float) -> 'Rotation':
        """Create a rotation around the Z-axis by theta radians."""
        c, s = np.cos(theta), np.sin(theta)
        rotation_matrix = np.array([[c, -s, 0],
                                     [s,  c, 0],
                                     [0,  0, 1]])
        return Rotation(rotation_matrix)

    @staticmethod
    def rotation_y(theta: float) -> 'Rotation':
        """Create a rotation around the Y-axis by theta radians."""
        c, s = np.cos(theta), np.sin(theta)
        rotation_matrix = np.array([[ c, 0, s],
                                     [ 0, 1, 0],
                                     [-s, 0, c]])
        return Rotation(rotation_matrix)
    @staticmethod
    def rotation_x(theta: float) -> 'Rotation':
        """Create a rotation around the X-axis by theta radians."""
        c, s = np.cos(theta), np.sin(theta)
        rotation_matrix = np.array([[1, 0,  0],
                                     [0, c, -s],
                                     [0, s,  c]])
        return Rotation(rotation_matrix)

    def rotate_world(self, axis: str, theta: float) -> 'Rotation':
        """Rotate the current rotation with respect to the world frame."""
        if axis == 'x':
            new_rotation = Rotation.rotation_x(theta)
        elif axis == 'y':
            new_rotation = Rotation.rotation_y(theta)
        elif axis == 'z':
            new_rotation = Rotation.rotation_z(theta)
        else:
            raise ValueError("Axis must be 'x', 'y', or 'z'.")
        
        # New rotation is applied after the current rotation
        combined_rotation_matrix = new_rotation.rotation_matrix @ self.rotation_matrix
        return Rotation(combined_rotation_matrix)

    def rotate_body(self, axis: str, theta: float) -> 'Rotation':
        """Rotate the current rotation with respect to the body frame."""
        if axis == 'x':
            new_rotation = Rotation.rotation_x(theta)
        elif axis == 'y':
            new_rotation = Rotation.rotation_y(theta)
        elif axis == 'z':
            new_rotation = Rotation.rotation_z(theta)
        else:
            raise ValueError("Axis must be 'x', 'y', or 'z'.")
        
        # New rotation is applied before the current rotation
        combined_rotation_matrix = self.rotation_matrix @ new_rotation.rotation_matrix
        return Rotation(combined_rotation_matrix)

    def __matmul__(self, other):
        return Rotation(self.rotation_matrix @ other.rotation_matrix)

