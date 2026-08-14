from atlas.geometry.positionvector import Position, Vector
from atlas.orientation.pose import Pose
from atlas.guidance.goalcontroller import GoToGoalController
from atlas.orientation.rotations import Rotation
import pytest
import numpy as np

def test_linearpcontroller():
    # Initialize the controller with some gains
    kv = 0.5
    kw = 1.0
    controller = GoToGoalController(kv, kw)

    # Define the current pose of the robot
    current_pose = Pose(Position(0,0,0), Rotation().rotate_body('z', np.pi/2))  # Facing along the y-axis
    # Define the goal position
    goal_position = Position(3, 0, 0)

    # Call the linearpcontroller method
    linear_velocity_vector, angular_velocity = controller.linearpcontroller(current_pose, goal_position)

    # Assertions to check if the computed velocities match the expected values
    assert np.isclose(linear_velocity_vector.x, 1.5)
    assert np.isclose(linear_velocity_vector.y, 0)
    assert np.isclose(linear_velocity_vector.z, 0)
    assert np.isclose(angular_velocity, -np.pi/2)  # The robot needs to turn -90 degrees to face the goal