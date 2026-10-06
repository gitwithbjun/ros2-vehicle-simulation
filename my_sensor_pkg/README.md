# ROS2 Sensor Simulation & Emergency Stop

## 1. 프로젝트 개요

ROS2와 Gazebo Sim을 이용하여 차량에 LiDAR, RGB Camera, IMU 센서를 구성하고,
Gazebo 센서 데이터를 ROS2 토픽으로 전달하는 센서 시뮬레이션 프로젝트입니다.

LiDAR `/scan`, Camera `/camera/image_raw`, IMU `/imu/data` 토픽을
`ros_gz_bridge`를 이용하여 ROS2로 전달하였으며,
센서 데이터 통신에는 Best Effort QoS를 적용하였습니다.

추가 과제로 LiDAR 데이터를 이용한 전방 긴급 정지 감지 노드를 구현하였습니다.

---

## 2. 주요 기능

### LiDAR

- Topic: `/scan`
- 설정 주기: 10 Hz
- 360도 거리 측정
- SensorDataQoS / Best Effort 적용

### RGB Camera

- Topic: `/camera/image_raw`
- 해상도: 640x480
- 설정 주기: 30 Hz

### IMU

- Topic: `/imu/data`
- 설정 주기: 50 Hz
- 각속도 및 선형 가속도 측정

---

## 3. Emergency Stop 구현

`emergency_stop_node.py`에서 `/scan` 토픽을 Best Effort QoS로 구독합니다.

LiDAR의 정면 방향을 0 rad로 기준으로 하여
정면 ±20도 영역의 거리 데이터만 검사합니다.

각 LiDAR 데이터의 각도는 다음 방식으로 계산합니다.

```text
angle = angle_min + index * angle_increment

GPT활용 내용
- ROS2 Python 패키지 구조 및 setup.py 설정 확인
- Xacro include 오류 원인 분석
- Gazebo 센서와 ros_gz_bridge 연결 문제 분석
- Best Effort QoS 설정 및 검증 방법 확인
- LiDAR LaserScan 메시지의 각도 계산 방식 학습
- Emergency Stop 노드 구현 과정에서 Python 문법 및 ROS2 Subscriber 구조 학습
AI가 제시한 내용을 그대로 사용하기보다는
실제 Gazebo 및 ROS2 환경에서 명령어를 실행하고 출력 결과를 확인하면서 수정하였습니다.

보강 내용
기본 실습 코드에서는 전체 LiDAR 거리 중 최소 거리를 확인하는 방식이 사용되었지만,
이번 과제에서는 차량 진행 방향에 있는 장애물만 판단할 수 있도록
정면 ±20도 범위의 LiDAR 데이터만 검사하도록 개선하였습니다.
또한 Gazebo와 ROS2 간 센서 브릿지의 QoS를 직접 확인한 결과,
초기에는 ROS publisher가 Reliable로 설정되어 있었습니다.
sensor_bridge.yaml에 Sensor Data QoS 프로파일을 적용하여
Publisher와 Subscriber 모두 BEST_EFFORT로 통일하였습니다.
실제 센서 주기가 설정값보다 낮게 측정되는 현상에 대해서도
Gazebo의 Real Time Factor를 확인하여 시스템 성능과 시뮬레이션 속도의 영향을 분석하였습니다.