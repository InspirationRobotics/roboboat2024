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
import time


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
		self.ANGLE_THR = 5 
		self.ANGLE_THR_P = 0.005 
		self.DIR_SAMPLE_TIME = 2 
		self.initial_alignment = False
		self.station_keep = False 
		self.keep_bearing = 0 
		self.keep_lat = 0
		self.keep_lon = 0
		self.prev_lat = 0
		self.prev_lon = 0
		self.last_time = time.time()
		self.brg = 0

	def gps_callback(self, data):
		print("entergps callback")
		self.current_lat = data.latitude
		self.current_lon = data.longitude
		self.target_angle = self.get_bearing(self.current_lat, self.current_lon, self.target_lat, self.target_lon)
		print("Current Lat: {0}, Current Lon: {1}".format(self.current_lat, self.current_lon))
		self.target_distance = ((self.target_lat - self.current_lat)**2 + (self.target_lon - self.current_lon)**2) ** (1/2)
		print("Target distance: {0}".format(self.target_distance))
		if(abs(self.target_distance) < self.MIN_DIST):
			#right.publish(0.0)
			#left.publish(0.0)
			self.arrived = True
			print("Arrived")
		orientation = self.get_orientation(self.current_lat, self.current_lon)
		print("orintation:")
		print(orientation)
		self.new_Nav(orientation)

	def get_orientation(self, lat, lon):
		cur_time = time.time()
		print("BEARING: "+str(self.brg))
		if(cur_time-self.last_time > self.DIR_SAMPLE_TIME):
			self.prev_lat = lat
			self.prev_lon = lon
			self.last_time = time.time()
		#self.brg = self.get_bearing(lat, lon, self.prev_lat, self.prev_lon)
		self.brg = self.get_bearing(self.prev_lat, self.prev_lon, lat, lon)
		return self.brg

	def imu_callback(self, data):
		print("enter  imu callback")

	def differential(self, pwrL, pwrR):
		mc_pub = rospy.Publisher('/wamv/thrusters/differential_speed', String, queue_size=10)
		pub_str = '{"lp":' + str(pwrL) +  ', "rp":' + str(pwrR) +  '}'
		mc_pub.publish(pwrR)

	def new_Nav(self, orientation):
		print("Enter new nav")
		comp = math.degrees(orientation)
		comp=comp%360
		if(comp<0):
			comp=360+comp
		print("comp: ",format(comp)) 
		print("comp done")

		self.target_angle=math.degrees(self.target_angle)
		self.target_angle=self.target_angle%360
		if(self.target_angle<0):
			self.target_angle=360+self.target_angle
		speed1 = 0.0
		speed2 = 0.0
		angle_thr = self.ANGLE_THR
		print("target angle: ", format(self.target_angle))
		angle_diff = comp - self.target_angle
		print("angle diff: ", format(angle_diff))
		dir = 1
		normal_power = 0.8
		if(abs(angle_diff) > 180):
			dir *= -1
			print("DIR: "+str(dir))
		if(angle_diff < 0):
			dir *= -1
			print("DIR: "+str(dir))
		if(abs(angle_diff) > angle_thr):
			power_delta = (abs(angle_diff))/5000
			#power_delta = 0.05
			print("power_delta: ", format(power_delta))
			lower_power = normal_power - power_delta
			higher_power = normal_power + power_delta
			print("low_power: ", format(lower_power))
			print("high_power: ", format(higher_power))
			
			if(dir == -1):
				self.differential(lower_power, higher_power)
				print("counter clockwise")
			else:
				self.differential(higher_power, lower_power)
				print("clockwise")
		else:
			self.differential(normal_power, normal_power)
			print("straight")
			
		
	def calculate_target_angle(self, goal):
		return -math.atan2((goal.latitude - self.current_lat),(goal.longitude - self.current_lon))

	def calculate_target_distance(goal):
		return ((goal.latitude - self.current_lat)**2 + (goal.longitude - self.current_lon)**2) ** (1/2)


	def waypoint_callback(self, data):
	    gps = rospy.Subscriber("/wamv/sensors/gps/gps/fix", NavSatFix, self.gps_callback)
	    imu = rospy.Subscriber("/wamv/sensors/imu/imu/data", Imu, self.imu_callback)    

	    for i in range(0,3):
		    self.target_lat = (data.poses[i].pose.position.latitude)
		    self.target_lon = (data.poses[i].pose.position.longitude)
		    self.keep_bearing = self.euler_from_quaternion(data.poses[i].pose.orientation)
		    self.initial_alignment = True
		    self.station_keep = False
		    self.waypoint_done = False
		    self.arrived = False
		    self.initial_alignment = True
		    print("Waypoint:")
		    print(self.target_lat)
		    print(self.target_lon)
		    print(self.keep_bearing)

		    while (not self.waypoint_done):
		       time.sleep(0.1)
		       if(rospy.is_shutdown()):
		          break;
	    self.all_done = True

	def waypoint(self):
	    rospy.init_node('gps_navigator', anonymous=True)
	    task_info_sub = rospy.Subscriber("/vrx/wayfinding/waypoints", GeoPath, self.waypoint_callback)
	    while (not rospy.is_shutdown() and not self.all_done):
		    time.sleep(0.1)

	def get_quaternion_from_euler(self, angle):
		ret = np.sin(angle/2) - np.cos(angle/2) 
		return ret

	def euler_from_quaternion(self, q):
		t3 = +2.0 * (q.w * q.z + q.x * q.y)
		t4 = +1.0 - 2.0 * (q.y * q.y + q.z * q.z)
		yaw_z = math.atan2(t3, t4)
		return yaw_z
		

	def get_bearing(self, lat2, long2, lat1, long1):
		dLon = (long2 - long1)
		y = math.sin(dLon) * math.cos(lat2)
		x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
		brng = math.atan2(y, x) - 3.1415/2
		if(brng < -3.1415):
			brng = brng + (2*3.1415)	
		elif (brng > 3.1415):
			brng = brng - (2*3.1415)	

		return brng


if __name__ == '__main__':
	try:
		navigator = GPS_Nav()
		navigator.waypoint()
	except rospy.ROSInterruptException:
		pass
