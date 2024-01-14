import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Float64

class Pub(Node):
    def __init__(self):
        super().__init__('pub')
        self.lat_pub = self.create_publisher(Float64, '/wamv/sensors/gps/lat', 10)
        self.lon_pub = self.create_publisher(Float64, '/wamv/sensors/gps/lon', 10)
        self.hdg_pub = self.create_publisher(Float64, '/wamv/sensors/gps/hdg', 10)
        timer_period = 0.1 #seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
    def timer_callback(self):
        msg = Float64()
        msg.data = 1.111111
        self.lat_pub.publish(msg)
        self.lon_pub.publish(msg)
        self.hdg_pub.publish(msg)
def main(args=None):
    rclpy.init(args = args)
    gps_reader = Pub()
    rclpy.spin(gps_reader)
    gps_reader.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()
