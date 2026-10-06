#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
오토모티브SW프로그래밍 6주차 실습 런치 파일: 센서 시뮬레이션 브릿지 및 리스너 통합 실행
작성자: 김동주 교수 (deekim@cu.ac.kr)

[설명]
Gazebo Sim과 ROS 2 간 센서 토픽을 중계하는 ros_gz_bridge 노드와,
수신된 센서 데이터를 전처리하는 멀티스레드 sensor_listener 노드를
동시에 실행하는 ROS 2 런치 파일입니다.
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """
    센서 브릿지 및 리스너 노드를 기동하는 LaunchDescription 반환
    """
    # 1. 브릿지 YAML 설정 파일 경로 계산 (code06/config/sensor_bridge.yaml)
    sensor_share = get_package_share_directory('my_sensor_pkg')
    default_bridge_config = os.path.join(sensor_share, 'config', 'sensor_bridge.yaml')
    start_sim_arg = DeclareLaunchArgument(
        'start_sim', default_value='true',
        description='Start Gazebo and spawn the vehicle; false if already running'
    )
    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('my_vehicle_gazebo'),
            'launch', 'spawn_car.launch.py'
        )),
        condition=IfCondition(LaunchConfiguration('start_sim'))
    )

    # 2. 런치 인자 선언
    bridge_config_arg = DeclareLaunchArgument(
        'bridge_config',
        default_value=os.path.normpath(default_bridge_config),
        description='ros_gz_bridge 센서 매핑 YAML 설정 파일의 절대 경로'
    )

    # 3. ros_gz_bridge 노드 정의
    # Gazebo 내부의 /scan, /camera/image_raw, /imu/data 토픽을 ROS 2 토픽으로 실시간 변환
    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='sensor_parameter_bridge',
        parameters=[{
            'config_file': LaunchConfiguration('bridge_config'),
            'use_sim_time': True
        }],
        output='screen'
    )

    # 4. 멀티스레드 센서 리스너 노드 정의
    # Best Effort QoS 프로파일 및 MultiThreadedExecutor 기반으로 3대 센서 데이터 수신/가공
    sensor_listener_node = Node(
        package='my_sensor_pkg',
        executable='sensor_listener',
        name='sensor_listener_node',
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        start_sim_arg,
        simulation,
        bridge_config_arg,
        bridge_node,
        sensor_listener_node
    ])
