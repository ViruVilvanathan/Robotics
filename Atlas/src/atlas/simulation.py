from atlas.geometry.positionvector import Position
from atlas.orientation.pose import Pose
from atlas.orientation.rotations import Rotation
from atlas.guidance.goalcontroller import GoToGoalController
from atlas.kinematics.motionupdate import MotionUpdate

import matplotlib.pyplot as plt
import numpy as np


def simulate_robot_movement(
    initial_pose: Pose,
    goal_position: Position,
    fig,
    ax
):
    # Controller gains
    kv = 0.5
    kw = 1.0

    controller = GoToGoalController(kv, kw)

    # Simulation parameters
    dt = 0.1
    max_steps = 1000
    goal_tolerance = 0.1

    current_pose = initial_pose
    trajectory = [current_pose]

    # -------------------------
    # Reset plot for new run
    # -------------------------

    ax.clear()

    ax.set_aspect("equal")
    ax.set_xlabel("World X")
    ax.set_ylabel("World Y")
    ax.set_title("Atlas Autonomous Navigation")

    # Plot goal
    ax.plot(
        goal_position.x,
        goal_position.y,
        "x",
        markersize=10,
        label="Goal"
    )

    # Plot objects that will be updated
    trajectory_line, = ax.plot(
        [],
        [],
        label="Trajectory"
    )

    robot_point, = ax.plot(
        [],
        [],
        "o",
        label="Atlas"
    )

    ax.legend()

    heading_arrow = None

    # -------------------------
    # Simulation loop
    # -------------------------

    for step in range(max_steps):

        # Controller computes body-frame velocity and angular velocity
        linear_velocity_vector, angular_velocity = (
            controller.linearpcontroller(
                current_pose,
                goal_position
            )
        )

        # Motion model integrates from the latest pose
        motion_update = MotionUpdate(current_pose)

        current_pose = motion_update.update_pose(
            linear_velocity_vector,
            angular_velocity,
            dt
        )

        trajectory.append(current_pose)

        # -------------------------
        # Update visualization
        # -------------------------

        x_history = [
            pose.position.x
            for pose in trajectory
        ]

        y_history = [
            pose.position.y
            for pose in trajectory
        ]

        trajectory_line.set_data(
            x_history,
            y_history
        )

        robot_point.set_data(
            [current_pose.position.x],
            [current_pose.position.y]
        )

        # Body +x axis expressed in world frame
        forward_world = (
            current_pose
            .orientation
            .rotation_matrix[:, 0]
        )

        forward_x = forward_world[0]
        forward_y = forward_world[1]

        ax.set_xlim(-1, 6)
        ax.set_ylim(-1, 6)

        # Remove previous heading arrow
        if heading_arrow is not None:
            heading_arrow.remove()

        # Draw updated heading arrow
        heading_arrow = ax.arrow(
            current_pose.position.x,
            current_pose.position.y,
            forward_x * 0.5,
            forward_y * 0.5,
            head_width=0.15,
            length_includes_head=True
        )

        # Adjust plot limits
        
        expand_axes_if_needed(
            ax,
            current_pose.position.x,
            current_pose.position.y,
            margin=1.0
            )

        # Redraw without blocking
        fig.canvas.draw_idle()
        fig.canvas.flush_events()

        plt.pause(0.05)

        # -------------------------
        # Goal condition
        # -------------------------

        if (
            current_pose
            .position
            .distance_to(goal_position)
            < goal_tolerance
        ):
            print(
                f"Goal reached in {step + 1} steps"
            )
            break

    else:
        print(
            "Maximum steps reached without reaching the goal."
        )

    return current_pose, trajectory, step + 1

def expand_axes_if_needed(ax, x, y, margin=1.0):
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()

    new_x_min = x_min
    new_x_max = x_max
    new_y_min = y_min
    new_y_max = y_max

    if x < x_min + margin:
        new_x_min = x - margin

    if x > x_max - margin:
        new_x_max = x + margin

    if y < y_min + margin:
        new_y_min = y - margin

    if y > y_max - margin:
        new_y_max = y + margin

    ax.set_xlim(new_x_min, new_x_max)
    ax.set_ylim(new_y_min, new_y_max)

if __name__ == "__main__":

    plt.ion()

    fig, ax = plt.subplots()
    plt.show(block=False)

    # Initial Atlas pose
    current_pose = Pose(
        Position(0, 0, 0),
        Rotation().rotate_body("z", np.pi / 2)
    )

    while plt.fignum_exists(fig.number):

        user_input = input(
            "\nEnter goal x y, or 'q' to quit: "
        ).strip()

        if user_input.lower() == "q":
            break

        try:
            x_str, y_str = user_input.split()

            goal_x = float(x_str)
            goal_y = float(y_str)

        except ValueError:
            print("Enter goal as: x y")
            print("Example: 5 5")
            continue

        # Planar navigation invariant:
        # keep goal z equal to Atlas's current z
        goal_position = Position(
            goal_x,
            goal_y,
            current_pose.position.z
        )

        final_pose, trajectory, steps = simulate_robot_movement(
            current_pose,
            goal_position,
            fig,
            ax
        )

        # THIS is what makes the navigation cumulative
        current_pose = final_pose

        print(
            f"Final Position: "
            f"({current_pose.position.x:.3f}, "
            f"{current_pose.position.y:.3f}, "
            f"{current_pose.position.z:.3f})"
        )

        print(f"Total Steps: {steps}")

    plt.close(fig)