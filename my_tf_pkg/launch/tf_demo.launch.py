#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
오토모티브SW프로그래밍 5주차 실습 런치 파일: TF2 데모 시스템 통합 실행
작성자: 김동주 교수 (deekim@cu.ac.kr)

[설명]
정적 브로드캐스터(static_tf_broadcaster), 동적 브로드캐스터(dynamic_tf_broadcaster),
그리고 TF 버퍼 리스너(tf_listener) 세 노드를 단일 명령으로 동시에 실행하고
프로세스 수명주기를 관리하는 ROS 2 런치 파일입니다.
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        Node(
            package='my_tf_pkg',
            executable='static_tf',
            name='static_tf_broadcaster',
            output='screen'
        ),

        Node(
            package='my_tf_pkg',
            executable='dynamic_tf',
            name='dynamic_tf_broadcaster',
            output='screen'
        ),

        Node(
            package='my_tf_pkg',
            executable='tf_listener',
            name='tf_listener',
            output='screen'
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            output='screen'
        )
    ])