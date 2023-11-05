#!/usr/bin/env python
from gps_navigator import GPS_Nav 
import rclpy

def main(args=None):
    rclpy.init(args=args)
    node = GPS_Nav()
    node.waypoint()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()


