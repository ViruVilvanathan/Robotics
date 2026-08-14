from atlas.geometry.positionvector import Position
from atlas.orientation.pose import Pose
from atlas.orientation.rotations import Rotation
from atlas.guidance.goalcontroller import GoToGoalController
from atlas.kinematics.motionupdate import MotionUpdate
import numpy as np

def simulate_robot_movement(initial_pose: Pose, goal_position: Position):
    # Initialize the controller with some gains
    kv = 0.5  # Linear velocity gain
    kw = 1.0  # Angular velocity gain
    controller = GoToGoalController(kv, kw)

    # Initialize the motion update with the initial pose
    motion_update = MotionUpdate(initial_pose)

    # Simulation parameters
    dt = 0.1  # Time step in seconds
    max_steps = 1000  # Maximum number of simulation steps

    current_pose = initial_pose

    trajectory = [current_pose.position]

    for step in range(max_steps):

        linear_velocity_vector, angular_velocity = controller.linearpcontroller(current_pose,goal_position)

        motion_update = MotionUpdate(current_pose)

        current_pose = motion_update.update_pose(linear_velocity_vector, angular_velocity, dt)

        # Check if the robot is close enough to the goal
        if current_pose.position.distance_to(goal_position) < 0.1:
            print(f"Goal reached in {step + 1} steps")
            break
        trajectory.append(current_pose.position)
    return current_pose, trajectory, step + 1

if __name__ == "__main__":
    # Define the initial pose of the robot
    initial_position = Position(0, 0, 0)
    initial_orientation = Rotation().rotate_body('z', np.pi / 2)  # Assuming a default orientation
    initial_pose = Pose(initial_position, initial_orientation)

    # Define the goal position
    goal_position = Position(5, 5, 0)

    # Run the simulation
    final_pose, trajectory, steps = simulate_robot_movement(initial_pose, goal_position)

    print(f"Final Pose: Position({final_pose.position.x}, {final_pose.position.y}, {final_pose.position.z}), "
          f"Orientation:\n{final_pose.orientation.rotation_matrix}",
            f"Total Steps: {steps}",
            trajectory)