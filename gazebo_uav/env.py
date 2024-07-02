# coding=utf-8
# Copyright 2019 The SEED Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Gazebo UAV env factory."""

from absl import flags
from absl import logging

import gym
from seed_rl.common import common_flags

FLAGS = flags.FLAGS

# Environment settings.
flags.DEFINE_string('gazebo_uav', 'GazeboUAV-v0', 'Name of the custom environment.')
flags.DEFINE_string('robot_args', '--your-args', 'Arguments for initializing the robot environment.')

def create_environment(unused_task_id, config):
    """Returns a gym Gazebo UAV environment."""
    logging.info('Creating environment: %s', config.environment_name)
    env = gym.make(config.environment_name)
    return env
