from atlas.geometry.positionvector import Position, Vector
import pytest
import numpy as np
from atlas.orientation.pose import Pose
from atlas.orientation.rotations import Rotation

def test_world_to_body_with_yaw():
    pose = Pose(
        Position(2, 3, 1),
        Rotation.rotation_z(np.pi / 2)
    )

    goal = Position(7, 5, 4)

    result = pose.world_to_body(goal)

    assert pytest.approx(result.x) == 2
    assert pytest.approx(result.y) == -5
    assert pytest.approx(result.z) == 3

def test_pose_transform():
    position = Position(1, 2, 3)
    orientation = Rotation.rotation_z(np.pi / 4)
    pose = Pose(position, orientation)

    expected_transform = np.array([
        [np.cos(np.pi / 4), -np.sin(np.pi / 4), 0, 1],
        [np.sin(np.pi / 4), np.cos(np.pi / 4), 0, 2],
        [0, 0, 1, 3],
        [0, 0, 0, 1]
    ])

    assert np.allclose(pose.pose_transform(), expected_transform)

def test_inverse_pose_transform():
    pose = Pose(
        Position(1, 2, 3),
        Rotation()
        )

    Tinv = pose.inverse_pose_transform()

    assert np.allclose(Tinv @ pose.pose_transform(), np.eye(4))
    assert np.allclose(Tinv[:3, :3], np.eye(3))
    assert np.allclose(Tinv[:3, 3], [-1, -2, -3])

    