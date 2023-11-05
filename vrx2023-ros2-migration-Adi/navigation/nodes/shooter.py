import rclpy
from std_msgs.msg import Bool
import time

def shoot():
    rclpy.init()
    node = rclpy.create_node('bool_publisher_node')
    publisher = node.create_publisher(Bool, '/wamv/shooters/ball_shooter/fire', 10)

    while rclpy.ok():
        msg = Bool()
        msg.data = True
        node.get_logger().info('Publishing: True')
        publisher.publish(msg)

        time.sleep(1)  # Publish every 1 second


if __name__ == '__main__':
    try:
        shoot()
    except KeyboardInterrupt:
        pass
