#!/usr/bin/env python3

# 수학 함수 사용을 위해 import
# math.radians(20)처럼 "20도"를 라디안으로 바꿀 때 사용
import math

# ROS2 Python 라이브러리
import rclpy

# 모든 ROS2 노드는 Node 클래스를 기반으로 만듦
from rclpy.node import Node

# 라이다 메시지 타입
# /scan 토픽의 데이터 형식
from sensor_msgs.msg import LaserScan

# 센서 데이터용 QoS
# Best Effort 방식이 기본으로 들어 있음
from rclpy.qos import qos_profile_sensor_data


# EmergencyStopNode라는 새로운 ROS2 노드 클래스 생성
class EmergencyStopNode(Node):

    # __init__은 클래스가 만들어질 때 자동으로 실행되는 함수
    def __init__(self):

        # 부모 클래스인 Node의 초기화 함수 호출
        # 노드 이름은 emergency_stop_node
        super().__init__('emergency_stop_node')

        # /scan 토픽을 구독
        self.scan_sub = self.create_subscription(
            LaserScan,                  # 메시지 타입
            '/scan',                    # 구독할 토픽 이름
            self.scan_callback,         # 메시지가 오면 실행할 함수
            qos_profile_sensor_data     # Best Effort QoS
        )

        # 노드가 정상적으로 시작됐는지 확인용 로그
        self.get_logger().info('Emergency Stop 노드 시작')


    # /scan 메시지가 들어올 때마다 자동으로 실행되는 함수
    def scan_callback(self, msg):

        # 전방 범위는 정면 기준 ±20도
        front_angle_limit = math.radians(20)

        # msg.ranges는 거리 값들이 들어있는 리스트
        # enumerate를 사용하면
        # index와 distance를 동시에 꺼낼 수 있음
        for index, distance in enumerate(msg.ranges):

            # 현재 인덱스가 몇 도 방향인지 계산
            angle = msg.angle_min + index * msg.angle_increment

            # 전방 ±20도 범위인지 확인
            if abs(angle) <= front_angle_limit:

                # 거리 값이 실제 센서 측정 범위 안에 있는지 확인
                # 너무 작거나 너무 큰 값은 제외
                if msg.range_min < distance < msg.range_max:

                    # 장애물이 1.0m 이내인지 확인
                    if distance <= 1.0:

                        # 긴급 정지 경고 출력
                        # error 레벨은 터미널에서 보통 빨간색 계열로 표시됨
                        self.get_logger().error(
                            f'[EMERGENCY_STOP] 전방 장애물 감지! 거리: {distance:.2f}m'
                        )

                        # 하나 찾았으면 더 검사할 필요가 없으므로 반복 종료
                        break


# 프로그램 시작점
def main(args=None):

    # ROS2 Python 시스템 초기화
    rclpy.init(args=args)

    # 우리가 만든 노드 객체 생성
    node = EmergencyStopNode()

    # 노드를 계속 실행
    # /scan 메시지가 들어올 때마다 callback이 호출됨
    rclpy.spin(node)

    # 종료 시 노드 정리
    node.destroy_node()

    # ROS2 종료
    rclpy.shutdown()


# 이 파일을 직접 실행했을 때 main() 함수 실행
if __name__ == '__main__':
    main()