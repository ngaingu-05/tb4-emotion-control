"""Gazebo Harmonic TurtleBot 4 arena with RViz and ROS clock bridge."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    share = get_package_share_directory('tb4_emotion_control')
    world = os.path.join(share, 'worlds', 'emotion_arena.sdf')
    resources = ':'.join([
        os.path.dirname(get_package_share_directory('turtlebot4_description')),
        os.path.dirname(get_package_share_directory('irobot_create_description')),
    ])
    gz_launch = os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
    spawn_launch = os.path.join(get_package_share_directory('turtlebot4_gz_bringup'),
                                'launch', 'turtlebot4_spawn.launch.py')
    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('model', default_value='standard'),
        DeclareLaunchArgument('x', default_value='0.0'),
        DeclareLaunchArgument('y', default_value='0.0'),
        DeclareLaunchArgument('yaw', default_value='0.0'),
        SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', resources),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gz_launch),
            launch_arguments={'gz_args': f'{world} -r --render-engine-server ogre2'}.items(),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(spawn_launch),
            launch_arguments={
                'world': 'emotion_arena',
                'model': LaunchConfiguration('model'),
                'rviz': LaunchConfiguration('rviz'),
                'nav2': 'false',
                'slam': 'false',
                'localization': 'false',
                'use_sim_time': 'true',
                'x': LaunchConfiguration('x'),
                'y': LaunchConfiguration('y'),
                'yaw': LaunchConfiguration('yaw'),
            }.items(),
        ),
        Node(package='ros_gz_bridge', executable='parameter_bridge',
             arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'], output='screen'),
    ])
