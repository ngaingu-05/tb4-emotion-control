from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
import os


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('python', default_value=os.path.expanduser('~/turtlebot4/.venv-emotion/bin/python')),
        DeclareLaunchArgument('camera', default_value='0'),
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('stamped', default_value='true'),
        DeclareLaunchArgument('confidence', default_value='0.45'),
        DeclareLaunchArgument('inference_period', default_value='0.5'),
        DeclareLaunchArgument('show_window', default_value='true'),
        DeclareLaunchArgument('mock_emotion', default_value=''),
        Node(package='tb4_emotion_control', executable='emotion_control_node',
             prefix=[LaunchConfiguration('python'), ' '], output='screen',
             parameters=[{'camera': ParameterValue(LaunchConfiguration('camera'), value_type=int),
                          'use_sim_time': ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool),
                          'stamped': ParameterValue(LaunchConfiguration('stamped'), value_type=bool),
                          'confidence': ParameterValue(LaunchConfiguration('confidence'), value_type=float),
                          'inference_period': ParameterValue(LaunchConfiguration('inference_period'), value_type=float),
                          'show_window': ParameterValue(LaunchConfiguration('show_window'), value_type=bool),
                          'mock_emotion': LaunchConfiguration('mock_emotion')}]),
    ])
