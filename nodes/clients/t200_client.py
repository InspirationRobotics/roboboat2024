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
            "/wamv/t200/motor_cmd",
            self.mc_callback,
            10)
        self.subscription  # prevent unused variable warning

# setup PWM channels for each of the motors

    def setpwm_port_fore(self, pwm):
        os.system("cd /home/inspirationagx01/maestro-linux && ./UscCmd --servo " + str(0) + "," + str(pwm*4))

    def setpwm_port_aft(self, pwm):
        os.system("cd /home/inspirationagx01/maestro-linux && ./UscCmd --servo " + str(1) + "," + str(pwm*4))

    def setpwm_starboard_fore(self, pwm):
        os.system("cd /home/inspirationagx01/maestro-linux && ./UscCmd --servo " + str(2) + "," + str(pwm*4))

    def setpwm_starboard_aft(self, pwm):
        os.system("cd /home/inspirationagx01/maestro-linux && ./UscCmd --servo " + str(3) + "," + str(pwm*4))        

    def mc_callback(self, data):
        send_data = data.data
    #send_data = "11"
        print(data.data)
# need to revise the stuff inside the brackets
        command_json = json.loads(data.data, parse_int=int)
        left_front = command_json['lp']
        left_back = command_json['lp']        
        right_front = command_json['rp']
        right_back = command_json['rp']
    
        print(command_json['lp'])
        print(command_json['rp'])

        self.setpwm_port_fore(left_front)
        self.setpwm_port_aft(left_back)        
        self.setpwm_starboard_fore(right_front)
        self.setpwm_starboard_aft(right_back)
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
