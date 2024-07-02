import gym
from gym import spaces
import numpy as np
import rclpy
from your_robot_module import Gazebo_Robot
from utils import calculate_reward
import cv2

class GazeboEnv(gym.Env):
    def __init__(self, robot_args, min_x, max_x, min_y, max_y):
        super(GazeboEnv, self).__init__()
        
        self.robot = Gazebo_Robot(robot_args, min_x, max_x, min_y, max_y)

        # Discrete action space with 5 possible actions
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(4,), dtype=np.float32)

        # Initialize ROS2
        rclpy.init(args=robot_args)

    def reset(self):
        # Reset the environment to an initial state and return an initial observation.
        self.robot.reset()
        observation = self._get_observation()
        return observation

    def step(self, action):
        # Execute one time step within the environment.
        self._apply_action(action)
        
        observation = self._get_observation()
        reward = self._compute_reward()
        done = self._check_done()

        return observation, reward, done, {}

    def _get_observation(self):
        # Get the current observation from the simulation
        depth_image, position, entropy_map, yaw, obstacle_map = self.robot.observation()
        
        # Prepare the observation dictionary
        observation = {
            'depth_image': depth_image,
            'yaw': np.array([yaw], dtype=np.float32),
            'entropy_map': entropy_map,
            'position': position,
            'obstacle_map': obstacle_map 
        }
        return observation

    def _compute_reward(self):
        # Compute the reward for the current state
        reward = calculate_reward(self.robot.entropy_map)
        return reward

    def _check_done(self):
        # Check if the episode is done
        done = self.robot.crash_detected()  # Example condition
        return done

    def _apply_action(self, action):
        # Define the action list as per your previous code
        action_list = ["Left", "H-Left", "Straight", "H-Right", "Right"]
        selected_action = action_list[action]
        
        # Command the robot using the selected action
        self.robot.command_velocity(selected_action)

    def render(self, mode='human'):
        depth_image = self._get_observation()['depth_image']
        # Convert depth image to a format suitable for display
        depth_image_display = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        cv2.imshow("Depth Image", depth_image_display)
        cv2.waitKey(1)

    def close(self):
        # Cleanup the environment
        self.robot.destroy_node()
        rclpy.shutdown()
