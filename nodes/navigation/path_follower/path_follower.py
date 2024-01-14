import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64
from std_msgs.msg import String
from mp_msgs.msg import Waypoint

# Waypoint custom msg type:
# Point pt
# bool passthrough

import time
import numpy as np

class PathFollower(Node):
	def __init__(self):
		super().__init__('path_follower')
		
		# [lat, lon, hdg, passthrough (for tgt)]
		self.current_pose = []
		self.target_pose = []
		
		self.arrived = False
		self.ANGLE_THR = 3
		self.MIN_DIST = 0.00003

		# pubs
		self.arrived_pub = self.create_publisher(String, '/wamv/navigation/arrived', 10)
		self.mc_torqeedo = self.create_publisher(String, '/wamv/torqeedo/motor_cmd', 10)

		# subs
		self.lat_s = self.create_subscription(Float64, "/wamv/sensors/gps/lat", self.lat_cb, 10)
		self.lon_s = self.create_subscription(Float64, "/wamv/sensors/gps/lon", self.lon_cb, 10)
		self.hdg_s = self.create_subscription(Float64, "/wamv/sensors/gps/hdg", self.hdg_cb, 10)
		self.tgt_s = self.create_subscription(Waypoint, "/wamv/navigation/target", self.tgt_cb, 10)


	def torqeedo_cmd(self, pwrL, pwrR, posL, posR):
		msg = String()
		pub_str = '{"lp":' + str(pwrL) +  ', "rp":' + str(pwrR) + ', "la":' + str(posL) +', "ra":'+str(posR)+ '}'
		msg.data = pub_str
		self.mc_torqeedo.publish(msg)

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

	def tgt_cb(self, data):
		self.target_pose[0] = data.pt.x
		self.target_pose[1] = data.pt.y
		self.target_pose[3] = data.passthrough

		self.arrived = False

	# just gets lon data
	def lon_cb(self, data):
		self.current_pose[0] = data.data

	# gets lat data and also calculates tgt angle
	def lat_cb(self, data):
		self.current_pose[1] = data.data
		self.target_pose[2] = self.get_bearing(self.target_pose[1], self.target_pose[0], self.current_lat, self.current_lon)

		dist = ((self.target_pose[1] - self.current_pose[1])**2 + (self.target_pose[0] - self.current_pose[0])**2) ** (1/2)
		if(abs(dist) < self.MIN_DIST):
			self.arrived = True
			print("Arrived")
			pub_str = String()
			pub_str.data = 'Arrived'
			self.arrived_pub.publish(pub_str)
		else:
			self.arrived = False


	def hdg_cb(self, data):
		compass = data.data % 360
		if(compass<0):
			compass = 360 + compass
		print("compass: ",format(compass))
		
		angle_thr = self.ANGLE_THR
		angle_diff = self.target_pose[2] - compass

		err = math.sqrt(
            math.pow(self.current_lat - self.target_lat, 2) +
            math.pow(self.current_lon - self.target_lon)
            )
		kp = 1 # to be tuned
		ki = 1
		kd = 1
		pwr = err * kp
		
		# steering
		skp = 1
		s_pwr = angle_diff * skp

		if ((angle_diff) > angle_thr):
			self.torqeedo_cmd(s_pwr, -s_pwr, 0, 0)
			print("turning clockwise")
		elif ((angle_diff) < -angle_thr):
			self.torqeedo_cmd(-s_pwr, s_pwr, 0, 0)
			print("turning anticlockwise")
		else:
			if(not self.arrived):
				if (self.target_pose[3]):
					self.torqeedo_cmd(300,300, 0, 0)
				else:
					self.torqeedo_cmd(pwr,pwr, 0, 0)
				print("go straight")
				self.initial_alignment = False

def main(args=None):
	rclpy.init()
	path_follower = PathFollower()
	rclpy.spin(path_follower)
    
if __name__ == '__main__':
        main()
