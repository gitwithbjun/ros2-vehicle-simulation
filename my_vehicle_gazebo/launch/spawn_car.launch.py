#!/usr/bin/env python3

import os
import xacro

from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    gazebo_share = get_package_share_directory('my_vehicle_gazebo')
    description_share = get_package_share_directory('my_vehicle_description')

    world_file = os.path.join(
        gazebo_share,
        'worlds',
        'car_track.sdf'
    )

    bridge_yaml = os.path.join(
        gazebo_share,
        'config',
        'bridge.yaml'
    )

    xacro_file = os.path.join(
        description_share,
        'urdf',
        'vehicle.urdf.xacro'
    )

    doc = xacro.process_file(xacro_file)
    robot_description_content = doc.toxml()

    gz_sim_process = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_file],
        output='screen'
    )

    spawn_car_node = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_car',
        output='screen',
        arguments=[
            '-name', 'auto_vehicle',
            '-string', robot_description_content,
            '-x', '0.0',
            '-y', '-4.0',
            '-z', '0.15'
        ]
    )

    gz_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        output='screen',
        parameters=[{
            'config_file': bridge_yaml
        }]
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_content,
            'use_sim_time': True
        }]
    )

    return LaunchDescription([
        gz_sim_process,
        spawn_car_node,
        gz_bridge_node,
        robot_state_publisher_node
    ])