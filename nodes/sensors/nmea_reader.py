from serial import Serial
from pynmeagps import NMEAReader

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64 
import numpy 
import math

class GPS_Reader(Node):
    def __init__(self):
        super().__init__('gps_reader')
        self.lat_pub = self.create_publisher(Float64, '/wamv/sensors/gps/lat', 10)
        self.lon_pub = self.create_publisher(Float64, '/wamv/sensors/gps/lon', 10)
        self.hdg_pub = self.create_publisher(Float64, '/wamv/sensors/gps/hdg', 10)
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
            msg = Float64()
            #print(msg)
            msg.data = parsed_data.lat
            self.lat_pub.publish(msg)
            print(msg)
        except Exception as e:
            #print(parsed_data)
            #print("exception")
            #print(e)
            pass
        try:
            msg = Float64()
            msg.data = parsed_data.lon
            self.lon_pub.publish(msg)
            print(msg)
        except:
            pass
        try:
            msg = Float64()
            msg.data = parsed_data.heading
            self.hdg_pub.publish(msg)
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
