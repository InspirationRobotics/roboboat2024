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
		left_front = rospy.Publisher('/wamv/thrusters/left_front_thrust_cmd', Float32, queue_size=10)
		left_back = rospy.Publisher('/wamv/thrusters/left_rear_thrust_cmd', Float32, queue_size=10)
		right_front = rospy.Publisher('/wamv/thrusters/right_front_thrust_cmd', Float32, queue_size=10)
		right_back = rospy.Publisher('/wamv/thrusters/right_rear_thrust_cmd', Float32, queue_size=10)
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
		left_front = rospy.Publisher('/wamv/thrusters/left_front_thrust_cmd', Float32, queue_size=10)
		left_back = rospy.Publisher('/wamv/thrusters/left_rear_thrust_cmd', Float32, queue_size=10)
		right_front = rospy.Publisher('/wamv/thrusters/right_front_thrust_cmd', Float32, queue_size=10)
		right_back = rospy.Publisher('/wamv/thrusters/right_rear_thrust_cmd', Float32, queue_size=10)
		print("target angle  : {0} radians / {1} degrees".format(self.target_angle, math.degrees(self.target_angle)))
		print("Current Rotation : {0} radians / {1} degrees".format(rotation, math.degrees(rotation)))

		comp = math.degrees(rotation)
		comp=comp%360
		if(comp<0):
			comp=360+comp
		print("comp: ",format(comp)) 
		
		speed1 = 0.0
		speed2 = 0.0
		angle_thr = self.ANGLE_THR
		angle_diff = self.target_angle - rotation
		if (self.target_distance > self.MED_DIST):
			speed1 = self.MAX_SPEED
			if (self.initial_alignment or angle_diff > 0.1):
				speed2 = self.MAX_SPEED  * -1
			else:
				speed2 = self.MAX_SPEED  - 0.2
		elif (self.target_distance > self.SLO_DIST):
			speed1 = self.MED_SPEED
			if (self.initial_alignment or angle_diff > 0.1):
				speed2 = self.MED_SPEED  * -1
			else:
				speed2 = self.MED_SPEED  * -1
		else:
			angle_thr = self.ANGLE_THR_P
			speed1 = self.SLO_SPEED
			speed2 = self.SLO_SPEED * -1


		if self.arrived:
			angle_diff = self.keep_bearing - rotation
			if(not self.waypoint_done and abs(angle_diff) > self.ANGLE_THR):
				print("entered final rotation")
				speed1 = self.SLO_SPEED
				speed2 = self.SLO_SPEED * -1
			else:
			    self.waypoint_done = True
			    speed1 = 0
			    speed2 = 0
			    if(not self.station_keep):
				    return

		if ((angle_diff) > angle_thr):
			right_front.publish(speed1)
			right_back.publish(speed1)
			left_front.publish(speed2)
			left_back.publish(speed2)
			print("turning anticlockwise")
		elif ((angle_diff) < -angle_thr):
			right_front.publish(speed2)
			right_back.publish(speed2)
			left_front.publish(speed1)
			left_back.publish(speed1)
			print("turning clockwise")
		else:
			if(not self.arrived):
				print("go straight")
				right_front.publish(speed1)
				right_back.publish(speed1)
				left_front.publish(speed1)
				left_back.publish(speed1)
				self.initial_alignment = False

		if (self.waypoint_done and self.station_keep):
			print("stationkeeping")
			if(self.current_lon>self.target_lon+0.00001):
				if(self.keep_bearing > 0 and self.keep_bearing<3.14):
					right_front.publish(-0.3)
					right_back.publish(-0.3)
					left_front.publish(-0.3)
					left_back.publish(-0.3)
					print("SK: 1")
				else:
					right_front.publish(0.3)
					right_back.publish(0.3)
					left_front.publish(0.3)
					left_back.publish(0.3)
					print("SK: 2")
			elif(self.current_lon<self.target_lon-0.00001):
				if(self.keep_bearing > 0 and self.keep_bearing<3.14):
					right_front.publish(0.3)
					right_back.publish(0.3)
					left_front.publish(0.3)
					left_back.publish(0.3)
					print("SK: 3")
				else:
					right_front.publish(-0.3)
					right_back.publish(-0.3)
					left_front.publish(-0.3)
					left_back.publish(-0.3)
					print("SK: 4")
			if(self.current_lat<self.target_lat-0.00001):
				if(self.keep_bearing > -3.14/2 and self.keep_bearing<3.14/2):
					right_front.publish(0.5)
					right_back.publish(-0.5)
					left_front.publish(-0.5)
					left_back.publish(0.5)
					print("SK: 5")
				else:
					right_front.publish(-0.5)
					right_back.publish(0.5)
					left_front.publish(0.5)
					left_back.publish(-0.5)
					print("SK: 6")
			elif(self.current_lat>self.target_lat+0.00001):
				if(self.keep_bearing > -3.14/2 and self.keep_bearing<3.14/2):
					right_front.publish(-0.5)
					right_back.publish(0.5)
					left_front.publish(0.5)
					left_back.publish(-0.5)
					print("SK: 7")
				else:
					right_front.publish(0.5)
					right_back.publish(-0.5)
					left_front.publish(-0.5)
					left_back.publish(0.5)
					print("SK: 8")

	def calculate_curvature(self, goal):
		numerator = 2 * abs(goal.longitude - self.current_lon)
		denominator = self.calculate_target_distance(goal) ** 2
		curvature = numerator / denominator


	def calculate_twist(self, curvature, cmd_velocity):
		twist = Twist()
		twist.linear.x = cmd_velocity
		twist.angular.z = current_vel * curvature
		return twist

	def calculate_target_angle(self, goal):
		return -math.atan2((goal.latitude - self.current_lat),(goal.longitude - self.current_lon))

	def calculate_target_distance(goal):
		return ((goal.latitude - self.current_lat)**2 + (goal.longitude - self.current_lon)**2) ** (1/2)

	def gps_navigator(self, lat, lon, keep, heading):
		print("gps_vaigator entry")
		rospy.init_node('gps_navigator', anonymous=True)
		rate = rospy.Rate(10) # 10hz
		self.target_lat = lat
		self.target_lon = lon
		self.station_keep = keep
		self.keep_bearing = heading

		test = rospy.Publisher('hello', Float32,queue_size=10)
		gps = rospy.Subscriber("/wamv/sensors/gps/gps/fix", NavSatFix, self.gps_callback)
		imu = rospy.Subscriber("/wamv/sensors/imu/imu/data", Imu, self.imu_callback)

		while (not self.arrived) or (self.station_keep):
			test.publish(1.0)
			time.sleep(0.1)
			if(rospy.is_shutdown()):
				break;
       
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

	def station_callback(self, data):
	    print("Station callback") 
	    gps = rospy.Subscriber("/wamv/sensors/gps/gps/fix", NavSatFix, self.gps_callback)
	    imu = rospy.Subscriber("/wamv/sensors/imu/imu/data", Imu, self.imu_callback)    

	    self.target_lat = (data.pose.position.latitude)
	    self.target_lon = (data.pose.position.longitude)
	    self.keep_bearing = self.euler_from_quaternion(data.pose.orientation)
	    self.initial_alignment = True
	    self.station_keep = False
	    self.waypoint_done = False
	    self.arrived = False
	    self.initial_alignment = True
	    self.station_keep = True
	    print("Waypoint:")
	    print(self.target_lat)
	    print(self.target_lon)
	    print(self.keep_bearing)

	    while (not self.waypoint_done):
	       time.sleep(0.1)
	       if(rospy.is_shutdown()):
	          break

	def station(self):
	    print("Station Keeping") 
	    rospy.init_node('gps_navigator', anonymous=True)
	    print("node init")
	    task_info_sub = rospy.Subscriber("/vrx/station_keeping/goal", GeoPoseStamped, self.station_callback)
	    
	    while (not rospy.is_shutdown() and not self.all_done):
		    time.sleep(0.1)

	def task_callback(self, data):
	    print("Task callback") 
	    print(data.name) 
	    if(data.name == "wayfinding" and not self.waypoint_started) :
		    print("starting wayfinding") 
		    self.waypoint_started = True 
		    self.waypoint() 
	    if(data.name == "station_keeping" and not self.station_started) :
		    print("starting station_keeping") 
		    self.station_started = True 
		    self.station() 


	def tasks(self):
	    print("tasks") 
	    rospy.init_node('gps_navigator', anonymous=True)
	    task_info_sub = rospy.Subscriber("/vrx/task/info", Task, self.task_callback)
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

	def position_hold(bearing, lat, long):
		left_front = rospy.Publisher('/wamv/thrusters/left_front_thrust_cmd', Float32, queue_size=10)
		left_back = rospy.Publisher('/wamv/thrusters/left_back_thrust_cmd', Float32, queue_size=10)
		right_front = rospy.Publisher('/wamv/thrusters/right_front_thrust_cmd', Float32, queue_size=10)
		right_back = rospy.Publisher('/wamv/thrusters/right_back_thrust_cmd', Float32, queue_size=10)
		if(self.current_lat<lat-0.00005):
			right_front.publish(0.1)
			right_back.publish(0.1)
			left_front.publish(0.1)
			left_back.publish(0.1)
		if(self.current_lat>lat+0.00005):
			right_front.publish(-0.1)
			right_back.publish(-0.1)
			left_front.publish(-0.1)
			left_back.publish(-0.1)

		angle_thr = self.ANGLE_THR
		angle_diff = bearning - rotation
		if ((angle_diff) > angle_thr):
			right_front.publish(speed1)
			right_back.publish(speed1)
			left_front.publish(speed2)
			left_back.publish(speed2)
			print("turning anticlockwise")
		elif ((angle_diff) < -angle_thr):
			left_front.publish(speed1)
			left_back.publish(speed1)

if __name__ == '__main__':
	try:
		target_lat = float(input("Latitude:"))
		target_lon = float(input("Longitude:"))
		navigator = GPS_Nav()
		navigator.gps_navigator(target_lat, target_lon)
	except rospy.ROSInterruptException:
		pass
