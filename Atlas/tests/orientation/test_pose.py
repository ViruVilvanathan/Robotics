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
