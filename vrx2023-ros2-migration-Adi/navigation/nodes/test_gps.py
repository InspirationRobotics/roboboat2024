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

	def gps_callback(self, data):
		print("entergps callback")
		self.current_lat = data.latitude
		self.current_lon = data.longitude
		left = rospy.Publisher('/wamv/thrusters/left_thrust_cmd', Float32, queue_size=10)
		right = rospy.Publisher('/wamv/thrusters/right_thrust_cmd', Float32, queue_size=10)
		self.target_angle = self.get_bearing(self.current_lat, self.current_lon, self.target_lat, self.target_lon)
		print("Current Lat: {0}, Current Lon: {1}".format(self.current_lat, self.current_lon))
		self.target_distance = ((self.target_lat - self.current_lat)**2 + (self.target_lon - self.current_lon)**2) ** (1/2)
		print("Target distance: {0}".format(self.target_distance))
		if(abs(self.target_distance) < self.MIN_DIST):
			#right.publish(0.0)
			#left.publish(0.0)
			self.arrived = True
			print("Arrived")

	def imu_callback(self, data):
		print("enter  imu callback")
		orientation = data.orientation
		rotation = self.euler_from_quaternion(orientation)
		left = rospy.Publisher('/wamv/thrusters/left_thrust_cmd', Float32, queue_size=10)
		right = rospy.Publisher('/wamv/thrusters/right_thrust_cmd', Float32, queue_size=10)
		lateral = rospy.Publisher('/wamv/thrusters/lateral_thrust_cmd', Float32, queue_size=10)
		print("target angle  : {0} radians / {1} degrees".format(self.target_angle, math.degrees(self.target_angle)))
		print("Current Rotation : {0} radians / {1} degrees".format(rotation, math.degrees(rotation)))

		comp = math.degrees(rotation)
		comp=comp%360
		if(comp<0):
			comp=360+comp
		print("comp: ",format(comp)) 
		left.publish(1.0)
		right.publish(-1.0)
		
if __name__ == '__main__':
	try:
		navigator = GPS_Nav()
		navigator.gps_callback()
	except rospy.ROSInterruptException:
		pass
