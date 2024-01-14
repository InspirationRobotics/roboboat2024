import socket
import sys
from std_msgs.msg import String
import serial
import rclpy
from rclpy.node import Node

class client(Node):

    def __init__(self):
        super().__init__('client')
        timer_period = 0.1  # seconds
        self.i = 0
        self.subscription = self.create_subscription(
            String,
            "/wamv/torqeedo/motor_cmd",
            self.mc_callback,
            10)
        self.subscription  # prevent unused variable warning

    def mc_callback(self, data):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        send_data = data.data
        print(data.data)
        print(send_data.encode('utf-8'))
        self.s.sendto(send_data.encode('utf-8'), ("192.168.1.5", 8000))

def main(args=None):
    rclpy.init(args=args)

    client_t = client()

    rclpy.spin(client_t)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    client_t.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
