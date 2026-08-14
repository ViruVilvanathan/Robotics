from atlas.geometry.positionvector import Position, Vector
from atlas.orientation.pose import Pose

import numpy as np

class GoToGoalController:
    def __init__(self, kv: float, kw: float):
        self.kv = kv  # Linear velocity gain
        self.kw = kw  # Angular velocity gain

    def linearpcontroller(self, current_pose: Pose, goal_position: Position):
        #controller simple linear controller to move the robot towards a goal position linearly in x y plane and orient
        # Calculate the vector from the current position to the goal position
        vector_to_goal_world = current_pose.position.vector_to(goal_position)
        vector_to_goal_body = current_pose.world_vector_to_body(vector_to_goal_world)
        position_error = vector_to_goal_body.magnitude()

        # Calculate the desired heading (angle) to the goal
        heading_error = np.arctan2(vector_to_goal_body.y, vector_to_goal_body.x)

        # Compute linear and angular velocities
        linear_velocity = self.kv * position_error
        angular_velocity = self.kw * heading_error

        return Vector(linear_velocity, 0, 0) , angular_velocity

    







        
        