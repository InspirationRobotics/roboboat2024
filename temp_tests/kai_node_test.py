#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

class Dummy_Node(Node):
    def __init__(self):
        super.__init__('Dummy')
        self.dummy = self.create_publisher(String, '/nav/buoy_points', 10)
        print('Dummy initilized')
    
    def plot_buoys(self, buoys):
        '''
        buoys: float32 array of buoy points
        '''
        msg = Float32MultiArray()
        msg.data = buoys
        self.dummy.publish(msg)

rclpy.init()
test_buoys = [0., 0.2, 0.3]
dummy = Dummy_Node()
dummy.plot_buoys(test_buoys)
rclpy.spin(navigator)
