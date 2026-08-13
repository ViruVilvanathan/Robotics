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

    assert np.allclose(pose.pose_transform_body_to_world(), expected_transform)

def test_inverse_pose_transform():
    pose = Pose(
        Position(1, 2, 3),
        Rotation()
        )

    Tinv = pose.inverse_pose_transform_world_to_body()

    assert np.allclose(Tinv @ pose.pose_transform_body_to_world(), np.eye(4))
    assert np.allclose(Tinv[:3, :3], np.eye(3))
    assert np.allclose(Tinv[:3, 3], [-1, -2, -3])

def test_pose_function():
    position = Position(1, 2, 3)
    orientation = Rotation.rotation_z(np.pi / 4)
    pose = Pose(position, orientation)
    goal = Position(4, 5, 6)

    v = pose.world_to_body(goal)

    goal_h = np.array([
        goal.x,
        goal.y,
        goal.z,
        1
    ])

    v_homo = pose.inverse_pose_transform_world_to_body() @ goal_h

    expected = np.array([v.x, v.y, v.z])

    assert np.allclose(v_homo[:3], expected)

def test_object_inworld_wrtbody():

    position = Position(1, 2, 3)
    orientation = Rotation.rotation_z(np.pi/2)
    pose = Pose(position, orientation)
    object_position_body = Position(1, 0, 0)

    object_position_world = pose.object_pose_world_from_bodyframe(object_position_body)

    assert object_position_world.x == pytest.approx(1)
    assert object_position_world.y == pytest.approx(3)
    assert object_position_world.z == pytest.approx(3)

def test_point_fromworldtobody():

    position = Position(1, 2, 3)
    orientation = Rotation.rotation_z(np.pi/2)
    pose = Pose(position, orientation)
    point_position_world = Position(1, 3, 3)

    point_position_body = pose.point_pose_world_to_bodyframe(point_position_world)

    assert point_position_body.x == pytest.approx(1)
    assert point_position_body.y == pytest.approx(0)
    assert point_position_body.z == pytest.approx(0)

    #assert that the transform of the point_position_bodyframe back to world frame gives the original point_position_world
    point_pose_bodytoworld = pose.object_pose_world_from_bodyframe(point_position_body)

    assert point_pose_bodytoworld.x == pytest.approx(point_position_world.x)
    assert point_pose_bodytoworld.y == pytest.approx(point_position_world.y)    
    assert point_pose_bodytoworld.z == pytest.approx(point_position_world.z)

