#!/usr/bin/env python
import rospy
import time
import numpy as np
from std_msgs.msg import Float32
from vrx_gazebo.msg import Task
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point
from geographic_msgs.msg import WayPoint
from geographic_msgs.msg import GeoPoint
from geographic_msgs.msg import KeyValue
from geographic_msgs.msg import GeoPath
from geographic_msgs.msg import GeoPoseStamped
from uuid_msgs.msg import UniqueID

import math


class GPS_Nav:

	def __init__(self):
		self.current_lat = 0
		self.current_lon = 0
		self.target_angle = 0.0
		self.arrived = False
		self.waypoint_done = False
		self.waypoint_started = False
		self.station_started = False
		self.all_done = False
		self.target_distance = 0
		self.MIN_DIST = 0.00002 
		self.SLO_DIST = 0.0001 
		self.MED_DIST = 0.005 
		self.MAX_SPEED = 0.9 
		self.MED_SPEED = 0.7 
		self.SLO_SPEED = 0.35 
		self.ANGLE_THR = 0.008 
		self.ANGLE_THR_P = 0.005 
		self.initial_alignment = True
		self.station_keep = False 
		self.keep_bearing = 0 
		self.keep_lat = 0
		self.keep_lon = 0
		self.counter = 0
		self.counter_max = 1000
		self.target_angle = 0

	def gps_callback(self, data):
		left = rospy.Publisher('/wamv/thrusters/left_thrust_cmd', Float32, queue_size=10)
		right = rospy.Publisher('/wamv/thrusters/right_thrust_cmd', Float32, queue_size=10)

	def imu_callback(self, data):
		print("enter  imu callback")
		orientation = data.orientation
		rotation = self.euler_from_quaternion(orientation)
		left = rospy.Publisher('/wamv/thrusters/left_thrust_cmd', Float32, queue_size=10)
		right = rospy.Publisher('/wamv/thrusters/right_thrust_cmd', Float32, queue_size=10)
		lateral = rospy.Publisher('/wamv/thrusters/lateral_thrust_cmd', Float32, queue_size=10)
		comp = math.degrees(rotation)
		comp=comp%360
		if(comp<0):
			comp=360+comp
		self.counter += 1
		if(self.counter>self.counter_max):
			rospy.signal_shutdown("max")		
			exit()
		if(self.turn_direction(self.target_angle, math.radians(comp))==1):
			left.publish(-0.5)
			right.publish(0.5)
		else:
			left.publish(0.5)
			right.publish(-0.5)

			

	def turn_direction(self, rad, comprad):
		print("comp: ",format(comprad)) 
		dir = 1
		diff = rad - comprad
		print("diff: ",format(diff)) 
		if(abs(diff)>3.14159):
			dir*=-1
		if(diff<0):
			dir*= -1
		if(dir==1):
			print("ccw")
		else:
			print("cw")	
		return dir
	
	def euler_from_quaternion(self, q):
                t3 = +2.0 * (q.w * q.z + q.x * q.y)
                t4 = +1.0 - 2.0 * (q.y * q.y + q.z * q.z)
                yaw_z = math.atan2(t3, t4)
                return yaw_z	

	def gps_navigator(self, tAngle):
		print("gps_vaigator entry")
		rospy.init_node('gps_navigator', anonymous=True)
		rate = rospy.Rate(10) # 10hz
		self.target_angle = tAngle

		test = rospy.Publisher('hello', Float32,queue_size=10)
		gps = rospy.Subscriber("/wamv/sensors/gps/gps/fix", NavSatFix, self.gps_callback)
		imu = rospy.Subscriber("/wamv/sensors/imu/imu/data", Imu, self.imu_callback)

		while (not self.arrived) or (self.station_keep):
			test.publish(1.0)
			time.sleep(0.1)
			if(rospy.is_shutdown()):
				break;
       



if __name__ == '__main__':
	try:
		navigator = GPS_Nav()
		target_ang = float(input("Target Angle:"))
		navigator.gps_navigator(target_ang)
	except rospy.ROSInterruptException:
		pass
