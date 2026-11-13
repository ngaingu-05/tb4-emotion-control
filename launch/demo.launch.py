"""Start Gazebo/RViz, undock, then start emotion control."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription,
                            RegisterEventHandler, TimerAction)
from launch.conditions import IfCondition, UnlessCondition
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    launch_dir = os.path.join(get_package_share_directory('tb4_emotion_control'), 'launch')
    emotion_control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_dir, 'emotion.launch.py')),
        launch_arguments={'python': LaunchConfiguration('python'),
                          'camera': LaunchConfiguration('camera'),
                          'mock_emotion': LaunchConfiguration('mock_emotion'),
                          'use_sim_time': 'true', 'show_window': 'true'}.items())
    undock_action = ExecuteProcess(
        cmd=['ros2', 'action', 'send_goal', '/undock', 'irobot_create_msgs/action/Undock', '{}'],
        output='screen', condition=IfCondition(LaunchConfiguration('auto_undock')))
    return LaunchDescription([
        DeclareLaunchArgument('python', default_value=os.path.expanduser('~/turtlebot4/.venv-emotion/bin/python')),
        DeclareLaunchArgument('camera', default_value='0'),
        DeclareLaunchArgument('mock_emotion', default_value=''),
        DeclareLaunchArgument('auto_undock', default_value='true'),
        DeclareLaunchArgument('start_delay', default_value='20.0',
                               description='Delay before control when auto_undock is false'),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(os.path.join(launch_dir, 'simulation.launch.py'))),
        RegisterEventHandler(OnProcessExit(target_action=undock_action, on_exit=[emotion_control])),
        TimerAction(period=15.0, actions=[undock_action]),
        TimerAction(period=LaunchConfiguration('start_delay'), actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(launch_dir, 'emotion.launch.py')),
                condition=UnlessCondition(LaunchConfiguration('auto_undock')),
                launch_arguments={'python': LaunchConfiguration('python'),
                                  'camera': LaunchConfiguration('camera'),
                                  'mock_emotion': LaunchConfiguration('mock_emotion'),
                                  'use_sim_time': 'true', 'show_window': 'true'}.items())
        ]),
    ])
