import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SimplePublisher(Node):
    def __init__(self):
        super().__init__('simple_publisher')

        self.publisher_ = self.create_publisher(
            String,
            '/vehicle_status',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.timer_callback
        )

        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Vehicle Speed: {self.i} km/h'

        self.publisher_.publish(msg)

        self.get_logger().info(msg.data)

        self.i += 5


def main(args=None):
    rclpy.init(args=args)

    node = SimplePublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()