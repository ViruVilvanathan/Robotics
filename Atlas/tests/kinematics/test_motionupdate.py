from atlas.geometry.positionvector import Position, Vector
from atlas.orientation.pose import Pose
from atlas.orientation.rotations import Rotation
from atlas.kinematics.motionupdate import MotionUpdate

import pytest
import numpy as np

def test_update_pose():
    initial_position = Position(0, 0, 0)
    initial_orientation = Rotation()
    initial_pose = Pose(initial_position, initial_orientation)
    motion_update = MotionUpdate(initial_pose)

    velocity = Vector(1, 0, 0)  # Move along x-axis
    ang_velocity_z = np.pi / 2  # Rotate 90 degrees around z-axis
    dt = 1.0  # Time step of 1 second

    new_pose = motion_update.update_pose(velocity, ang_velocity_z, dt)

    expected_position = Position(1, 0, 0)  # After moving along x-axis for 1 second
    expected_orientation = initial_orientation.rotate_body('z', ang_velocity_z)

    assert np.allclose(new_pose.position.x, expected_position.x)
    assert np.allclose(new_pose.position.y, expected_position.y)
    assert np.allclose(new_pose.position.z, expected_position.z)
    assert np.allclose(new_pose.orientation.rotation_matrix,
                       expected_orientation.rotation_matrix)
