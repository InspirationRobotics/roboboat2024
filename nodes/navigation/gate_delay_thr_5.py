#!/usr/bin/env python
import rclpy
from rclpy.node import Node
import time
import numpy as np
from std_msgs.msg import Float32
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int16
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
# from geometry_msgs.msg import Quaternion
# from geometry_msgs.msg import Pose
# from geometry_msgs.msg import Point
# from geographic_msgs.msg import WayPoint
# from geographic_msgs.msg import GeoPoint
# from geographic_msgs.msg import KeyValue
# from geographic_msgs.msg import GeoPath
# from geographic_msgs.msg import GeoPoseStamped


import math


class GPS_Nav(Node):

    def __init__(self):
        super().__init__('gps_navigator')
        self.current_lat = 0
        self.current_lon = 0
        self.target_angle = 0.0
        self.target_lon = 0
        self.target_lat = 0
        self.arrived = True
        self.waypoint_done = False
        self.waypoint_started = False
        self.station_started = False
        self.target_distance = 0
        # TODO: tune threshold
        self.MIN_DIST = 0.00003 #in lat/lon
        # TODO: finetune
        self.ANGLE_THR = 5 # angle in degrees
        self.arrived_pub = self.create_publisher(String, '/wamv/navigation/arrived', 10)
        self.mc_torqeedo = self.create_publisher(String, '/wamv/torqeedo/motor_cmd', 10)
        self.navigation_input=self.create_publisher(String,'navigation_input',10)
        self.waypoint_list = []
        self.waypoint_index = 0
        print("Navigator Init done")

    def torqeedo_cmd(self, pwrL, pwrR, posL, posR):
        msg = String()
        pub_str = '{"lp":' + str(pwrL) +  ', "rp":' + str(pwrR) + ', "la":' + str(posL) +', "ra":'+str(posR)+ '}'
        msg.data = pub_str
        self.mc_torqeedo.publish(msg)

    def lon_callback(self, data):
        self.current_lon = data.data

    def lat_callback(self, data):
        print("enter lat callback")
        self.current_lat = data.data
        self.target_angle = self.get_bearing(self.target_lat, self.target_lon, self.current_lat, self.current_lon)
        #print("TARGET ANGLE "+str(math.degrees(self.target_angle)))
        print("Current Lat: {0}, Current Lon: {1}".format(self.current_lat, self.current_lon))
        self.target_distance = ((self.target_lat - self.current_lat)**2 + (self.target_lon - self.current_lon)**2) ** (1/2)
        print("Target distance: {0}".format(self.target_distance))
        if(abs(self.target_distance) < self.MIN_DIST):
            self.arrived = True
            print("Arrived")
            pub_str = String()
            pub_str.data = 'Arrived'
            self.arrived_pub.publish(pub_str)
            #checking if all the waypoints are done
            if(self.waypoint_index < len(self.waypoint_list)-1):
                self.waypoint_index = self.waypoint_index+1
                self.target_lat = (self.waypoint_list[self.waypoint_index][0])
                self.target_lon = (self.waypoint_list[self.waypoint_index][1])
                print("Proceeding to next Waypoint {0} {1}".format(self.target_lat, " ", self.target_lon))
                self.arrived = False
        else:
            self.arrived = False


    def hdg_callback(self, data):
        print("enter  heading callback")
        print("Waypoint # ", self.waypoint_index)
        orientation = data.data
        
        self.target_angle=self.get_bearing(self.target_lat,self.target_lon,self.current_lat,self.current_lon)
        #self.target_angle=math.degrees(self.target_angle)
        #self.target_angle=self.target_angle%360
        print("#### TARGET ANGLE "+str(self.target_angle))
        if(self.target_angle<0):
               self.target_angle=360+self.target_angle

        
        print("TARGET ANGLE adjusted "+str(self.target_angle))
        rotation = orientation
        print("##### Heading:", orientation)
        print("target angle  degrees ", self.target_angle)
        print("Current Rotation : degrees ", rotation)
        # print("target angle  : {0} radians / {1} degrees".format(self.target_angle, math.degrees(self.target_angle)))
        # print("Current Rotation : {0} radians / {1} degrees".format(rotation, math.degrees(rotation)))


        compass = rotation
        compass=compass%360
        print("compass: ",format(compass))

        angle_thr = self.ANGLE_THR
        angle_diff = self.target_angle - compass
        print("#######Angle Diff " ,  format(angle_diff));
        print("#######Angle thr " ,  format(angle_thr));

        msg=String()
        if self.arrived:
            self.waypoint_done = True
            #publish the stop command
            print("Arrived , not going further")
            dir_to_move = "s"
            msg.data=dir_to_move
            self.navigation_input.publish(msg)
            return

        # TODO: PID pass through / target
        if ((angle_diff) > angle_thr):
            dir_to_move = "d"
            #publish CW command
            msg.data=dir_to_move
            self.navigation_input.publish(msg)
            print("turning clockwise")
            time.sleep(0.5)
            dir_to_move = "w"
            msg.data=dir_to_move
            self.navigation_input.publish(msg)
            print("continue after turning clockwise")
        elif ((angle_diff) < -angle_thr):
            dir_to_move = "a"
            #publish CCW/ACW command
            msg.data=dir_to_move
            self.navigation_input.publish(msg)
            print("turning anticlockwise")
            time.sleep(0.5)
            dir_to_move = "w"
            msg.data=dir_to_move
            self.navigation_input.publish(msg)
            print("continue after turning anti-clockwise")
        else:
            if(not self.arrived):
                dir_to_move = "w"
                #publish go straight command
                msg.data=dir_to_move
                self.navigation_input.publish(msg)
                print("go straight")
                self.initial_alignment = False
            else: #stop the boat
                print("arrived / stop")
                dir_to_move = "s"
                msg.data=dir_to_move
                self.navigation_input.publish(msg)

    def target_callback(self, data):
        self.target_lon = data.x
        self.target_lat = data.y
        # TODO: Extract passthrough = True/False
        self.arrived = False
        print("Waypoint:")
        print(self.target_lat)
        print(self.target_lon)
        ####test code
        #time.sleep(2)
        #pub_str = String()
        #pub_str.data = 'Arrived'
        #self.arrived_pub.publish(pub_str)
        return 

    def waypoint_callback(self):
        gps = self.create_subscription(Float64, "/wamv/sensors/gps/lat", self.lat_callback, 10)
        gps2 = self.create_subscription(Float64, "/wamv/sensors/gps/lon", self.lon_callback, 10)
        hdg = self.create_subscription(Float64, "/wamv/sensors/gps/hdg", self.hdg_callback, 10)
        self.waypoint_list=[]
        self.waypoint_index=0
        #array = []
        with open('lat_lon.txt') as f:
            for line in f: # read rest of lines
                self.waypoint_list.append([float(x) for x in line.split()])
        print(self.waypoint_list)
        #simple case of 1 waypoint; removing for loop for reading all of the waypoints
        self.target_lat=(self.waypoint_list[0][0])
        self.target_lon=(self.waypoint_list[0][1])      
        # for i in range(len(self.waypoint_list)):
        #     self.target_lat = (self.waypoint_list[i][0])
        #     self.target_lon = (self.waypoint_list[i][1])
        #     self.initial_alignment = True
        #     self.waypoint_done = False
        #     self.arrived = False
        #     self.initial_alignment = True
        #     print("Waypoint:")
        #     print(self.target_lat)
        #     print(self.target_lon)

            # while (not self.waypoint_done):
            #    time.sleep(0.1)
            #    if(rospy.is_shutdown()):
            #       break;
        self.all_done = True

    def euler_from_quaternion(q):
       t3 = +2.0 * (q.w * q.z + q.x * q.y)
       t4 = +1.0 - 2.0 * (q.y * q.y + q.z * q.z)
       yaw_z = math.atan2(t3, t4)
       return yaw_z


    def get_bearing(self, lat2, long2, lat1, long1):
        dLon = (long2 - long1)
        dLat = (lat2 - lat1)
        y = math.sin(dLon) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
        #brng = math.atan2(y, x) - 3.1415/2
        brng = math.atan2(y, x)
        brng = math.degrees(brng)
        brng=(brng+360)%360;
        brng=360-brng;
        # if(brng < -3.1415):
        #     brng = brng + (2*3.1415)
        # elif (brng > 3.1415):
        #     brng = brng - (2*3.1415)

        return brng

def main(args=None):
    rclpy.init()
    navigator = GPS_Nav()
    navigator.waypoint_callback()
    rclpy.spin(navigator)
    
if __name__ == '__main__':
        main()

