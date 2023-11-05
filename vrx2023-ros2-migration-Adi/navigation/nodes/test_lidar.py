#!/usr/bin/env python
import rospy
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from cv_bridge import CvBridge
import cv2

import time
import numpy as np
from std_msgs.msg import Float32
from vrx_gazebo.msg import Task
from uuid_msgs.msg import UniqueID

import math

#instead of using CVbridge, use Rviz or program David recommended

class LidarSubscriberNode(Node):
	def __init__(self):
        	super().__init__('lidar_subscriber')
        	self.subscription = self.create_subscription(
        	PointCloud2,
        	'/wamv/sensors/lidars/lidar_wamv/points',
        	self.image_callback,
        	10)
        	self.bridge = CvBridge()	
	def image_callback(self, msg):
         	try:
         	# Convert ROS Image message to OpenCV format
         	# Need to implement Rviz or ROS Board
         	cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
         	except Exception as e:
         		self.get_logger().error("Error converting image: %s" % str(e))
         	return
