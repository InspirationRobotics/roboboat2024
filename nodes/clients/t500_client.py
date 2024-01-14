import os
import json
import socket
import sys
from std_msgs.msg import String
import serial
import rclpy
from rclpy.node import Node

class client(Node):

    def __init__(self):
        super().__init__('client')
        print("init")
        timer_period = 0.1  # seconds
        self.i = 0
        self.subscription = self.create_subscription(
            String,
            "/wamv/t500/motor_cmd",
            self.mc_callback,
            10)
        self.subscription  # prevent unused variable warning

    def setpwm_port(self, pwm):
        os.system("cd /home/inspirationagx01/maestro-linux && ./UscCmd --servo " + str(0) + "," + str(pwm*4))

    def setpwm_starboard(self, pwm):
        os.system("cd /home/inspirationagx01/maestro-linux && ./UscCmd --servo " + str(1) + "," + str(pwm*4))

    def mc_callback(self, data):
        send_data = data.data
    #send_data = "11"
        print(data.data)

        command_json = json.loads(data.data, parse_int=int)
        left = command_json['lp']
        right = command_json['rp']
    
        print(command_json['lp'])
        print(command_json['rp'])

        self.setpwm_port(left)
        self.setpwm_starboard(right)
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
