import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.lon_pub = self.create_publisher(Float64, '/wamv/sensors/gps/lon', 10)
        self.lat_pub = self.create_publisher(Float64, '/wamv/sensors/gps/lat', 10)
        self.hdg_pub = self.create_publisher(Float64, '/wamv/sensors/gps/hdg', 10)

        
def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    while rclpy.ok():
        msg = Float64()

        msg.data = 0.0
        minimal_publisher.lon_pub.publish(msg)
        minimal_publisher.lat_pub.publish(msg)
        minimal_publisher.hdg_pub.publish(msg)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
