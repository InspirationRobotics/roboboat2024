import rclpy
from rclpy import Node
from std_msgs.msg import String

publisher = Node.create_publisher(String, './test_pub')
publisher.publish('1')

