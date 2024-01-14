from serial import Serial
from pynmeagps import NMEAReader

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64 
from wamv_msgs.msg import GPS_data
import numpy 
import math
import time

class GPS_Reader(Node):
    def __init__(self):
        super().__init__('gps_reader')
        self.lat_pub = self.create_publisher(GPS_data, '/wamv/sensors/gps', 10)
        timer_period = 0.01 #seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.stream = Serial('/dev/ttyACM0', 115200, timeout=3)
    
    def timer_callback(self):
        #print("timer callback")
        nmr = NMEAReader(self.stream)
        (raw_data, parsed_data) = nmr.read()
        #print("read")
        #print (parsed_data)
        try:
            #self.lat_pub.publish(parsed_data.lat)
            msg = GPS_data()
            #print(msg)
            msg.lat = parsed_data.lat
            msg.lon = parsed_data.lon
            msg.hdg = parsed_data.heading
            msg.ts = time.time()

            self.lat_pub.publish(msg)
            print(msg)
        except Exception as e:
            #print(parsed_data)
            #print("exception")
            #print(e)
            pass

def main(args=None):
    rclpy.init(args = args)
    gps_reader = GPS_Reader()
    rclpy.spin(gps_reader)
    gps_reader.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()
