#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import math
import time
import numpy as np
from std_msgs.msg import Float64
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from sensor_msgs.msg import LaserScan
from geographic_msgs.msg import WayPoint
from geographic_msgs.msg import GeoPoint
from geographic_msgs.msg import KeyValue
from geographic_msgs.msg import GeoPath
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import PoseArray
from geographic_msgs.msg import GeoPoseStamped
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

#from vrx_gazebo.msg import Task #can't import this

     
     
class GPS_Nav(Node): 
    def __init__(self):
        super().__init__("gps_navigator")
        self.poses = []
        self.i = 0
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
        #9000,900000, and 900 seem to move at basically the same speed, maybe it's capped at 1000
        #However, 90 is significantly different from 900
        self.MAX_SPEED = 9000.0 
        self.MED_SPEED = 7000.0 
        self.SLO_SPEED = 3500.0 
        self.ANGLE_THR = 0.8 
        self.ANGLE_THR_P = 0.5 
        self.initial_alignment = True
        self.station_keep = False 
        self.keep_bearing = 0 
        self.keep_lat = 0
        self.keep_lon = 0
        #self.gps_navigator(target_lat, target_lon)
        
          

    def gps_callback(self, data):
        print("entergps callback")
        print("i:" ,self.i)
        self.current_lat = data.latitude
        self.current_lon = data.longitude
        left_front = self.create_publisher(Float64, '/wamv/thrusters/left/thrust', 10)
        left_back = self.create_publisher(Float64, '/wamv/thrusters/left/thrust', 10)
        right_front = self.create_publisher(Float64, '/wamv/thrusters/right/thrust', 10)
        right_back = self.create_publisher(Float64, '/wamv/thrusters/right/thrust', 10)
        self.target_angle = self.get_bearing(self.current_lat, self.current_lon, self.target_lat, self.target_lon)
        #print("Current Lat: {0}, Current Lon: {1}".format(self.current_lat, self.current_lon))
        self.target_distance = ((self.target_lat - self.current_lat)**2 + (self.target_lon - self.current_lon)**2) ** (1/2)
        #print("Target distance: {0}".format(self.target_distance))
        if(abs(self.target_distance) < self.MIN_DIST):
			#right.publish(0.0)
            #left.publish(0.0)
            self.arrived = True
            speed1=0;
            speed2=0;
            print("Arrived")
            if(self.station_started):
            	print("holding place")
            	right_front.publish(-0.1)
            	right_back.publish(0.1)
            	left_front.publish(-0.1)
            	left_back.publish(0.1)
            if(not self.station_keep):
            	return

    def imu_callback(self, data):
        print("enter imu callback")
        print("i:" ,self.i)
        orientation = data.orientation
        rotation = self.euler_from_quaternion(orientation)
        left_front = self.create_publisher(Float64, '/wamv/thrusters/left/thrust', 10)
        left_back = self.create_publisher(Float64, '/wamv/thrusters/left/thrust', 10)
        right_front = self.create_publisher(Float64, '/wamv/thrusters/right/thrust', 10)
        right_back = self.create_publisher(Float64, '/wamv/thrusters/right/thrust', 10)
        #print("target angle  : {0} radians / {1} degrees".format(self.target_angle, math.degrees(self.target_angle)))
        #print("Current Rotation : {0} radians / {1} degrees".format(rotation, math.degrees(rotation)))

        comp = math.degrees(rotation)
        comp=comp%360
        if(comp<0):
            comp=360+comp
        #print("comp: ",format(comp)) 
		
        speed1 = 0.0
        speed2 = 0.0
        angle_thr = self.ANGLE_THR
        angle_diff = self.target_angle - rotation
        if (self.target_distance > self.MED_DIST):
            speed1 = self.MAX_SPEED
            if (self.initial_alignment or angle_diff > 0.1):
                speed2 = self.MAX_SPEED  * -1
            else:
            #this slows down the speed by 10x, it could be more if you want
                speed2 = self.MAX_SPEED  * -0.1
                #previously, speed1 was not also changed, so it was imbalanced
                speed1 = self.MAX_SPEED  * 0.1
        elif (self.target_distance > self.SLO_DIST):
            speed1 = self.MED_SPEED
            if (self.initial_alignment or angle_diff > 0.1):
                speed2 = self.MED_SPEED  * -1
            else:
                speed2 = self.MED_SPEED  * -0.1
                #speed1 and speed2 have to change here
                speed1 = self.MED_SPEED  * 0.1
        else:
            angle_thr = self.ANGLE_THR_P
            speed1 = self.SLO_SPEED
            #check this, I'm not sure if I changed it or it was like this originally
            speed2 = self.SLO_SPEED * -1


        if self.arrived:
            angle_diff = self.keep_bearing - rotation
            if(not self.waypoint_done and abs(angle_diff) > self.ANGLE_THR):
                #print("entered final rotation")
                speed1 = self.SLO_SPEED
                speed2 = self.SLO_SPEED * -1
            else:
                #self.waypoint_done = True
                if self.i < len(self.poses)-1:
                    self.i = self.i + 1
                    
                self.arrived = False
                self.target_lat = (self.poses[self.i].position._x)
                self.target_lon = (self.poses[self.i].position._y)
                speed1 = 0
                speed2 = 0
                
                if(not self.station_keep):
                    return

        if ((angle_diff) > angle_thr):
            msg_speed1 = Float64()
            msg_speed2 = Float64()
            msg_speed1.data = speed1
            msg_speed2.data = speed2

            right_front.publish(msg_speed1)
            right_back.publish(msg_speed1)
            left_front.publish(msg_speed2)
            left_back.publish(msg_speed2)
         #   print("turning anticlockwise")
          #  print(speed1)
           # print(speed2)

        elif ((angle_diff) < -angle_thr):
            msg_speed1 = Float64()
            msg_speed2 = Float64()
            #previously, the two following lines were backward, so msg_speed1 was speed 2 and msg_speed2 was speed1. However, since it was reversed again later, in the publishing messages section, it was incorrect.
            msg_speed1.data = speed1
            msg_speed2.data = speed2

            # Publish the messages
            right_front.publish(msg_speed2)
            right_back.publish(msg_speed2)
            left_front.publish(msg_speed1)
            left_back.publish(msg_speed1)
            #print("turning clockwise")
            #print(speed2)
            #print(speed1)
        else:
            if(not self.arrived):
             #   print("go straight")
                msg_speed = Float64()
                #this previously said "self.speed1" which didn't exist in this code. 
                msg_speed.data = speed1 * 15
                right_front.publish(msg_speed)
                right_back.publish(msg_speed)
                left_front.publish(msg_speed)
                left_back.publish(msg_speed)
                self.initial_alignment = False

                

    def calculate_curvature(self, goal):
        numerator = 2 * abs(goal.longitude - self.current_lon)
        denominator = self.calculate_target_distance(goal) ** 2
        curvature = numerator / denominator


#    def calculate_twist(self, curvature, cmd_velocity):
 #       twist = Twist()
  #      twist.linear.x = cmd_velocity
   #     twist.angular.z = current_vel * curvature
    #    return twist

    def calculate_target_angle(self, goal):
        return -math.atan2((goal.latitude - self.current_lat),(goal.longitude - self.current_lon))

    def calculate_target_distance(self, goal):
        return ((goal.latitude - self.current_lat)**2 + (goal.longitude - self.current_lon)**2) ** (1/2)

    def gps_navigator(self, lat, lon):
        print("gps_navigator entry")

       
        self.target_lat = lat
        self.target_lon = lon
        #self.test = self.create_publisher(Float32, "Hello", 10)
        gps = self.create_subscription(NavSatFix, "/wamv/sensors/gps/gps/fix", self.gps_callback, 10)
        imu = self.create_subscription(Imu, "/wamv/sensors/imu/imu/data", self.imu_callback, 10)

        
        #just a test, no function in the code
        #msg = Float32()
        #msg.data = self.target_lat
        #while rclpy.ok():
        #    self.test.publish(msg)
        #    time.sleep(0.1)

    def waypoint_callback(self, data):
        print("entered waypoint callback")
        gps = self.create_subscription(NavSatFix, "/wamv/sensors/gps/gps/fix", self.gps_callback, 10)
        imu = self.create_subscription(Imu, "/wamv/sensors/imu/imu/data", self.imu_callback, 10)
        

        print(".......................")
        self.target_lat = (data.poses[self.i].position._x)
        self.target_lon = (data.poses[self.i].position._y)
        self.poses = data.poses
        #print("i:" ,self.i)
        print("lat: ", self.target_lat)
        print("lon: ", self.target_lon)
        self.keep_bearing = self.euler_from_quaternion(data.poses[self.i].orientation)
        
        self.initial_alignment = True
        self.station_keep = False
        self.waypoint_done = False
        self.arrived = False
        self.initial_alignment = True
        print("Waypoint:")
        print(self.target_lat)
        print(self.target_lon)
        print(self.keep_bearing)

        #if self.arrived is True:
         #   self.i = self.i + 1
          #  self.arrived = False
            
            #while not self.waypoint_done:
             #   time.sleep
              #  self.create_timer(0.1, self.timer_callback)
               # if(not rclpy.ok()):
                #    break
        
        self.all_done = True

    def scan_callback(self, msg):
        
        return 0

    """def image_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        except Exception as e:
            self.get_logger().error("Error converting image: %s" % str(e))
            return self.gps_callback

        #creating publisher for result
        detected = self.create_publisher(
            PoseStamped, '/vrx/perception/landmark', 10)

        #Getting GPS location for calculations
        self.gps = self.create_subscription(
            NavSatFix, "/wamv/sensors/gps/gps/fix", self.gps_callback, 10)
        coordinates = self.gps.get_msg()
        
        #color detection
        #find algorithms to detect color in an image
        #create a filter/change color to black/wht, then appply another filter to draw bounding box around color image we're looking for.
        # converting pixels of the image to hsv from rgb
        

        Red_L_limit=np.array([0, 0, 100]) 
        Red_U_limit=np.array([30, 30, 255]) 

        Grn_L_limit=np.array([50, 30, 25]) 
        Grn_U_limit=np.array([75, 255, 30]) 

        Blk_L_limit=np.array([0, 0, 0]) 
        Blk_U_limit=np.array([26, 23, 23])
    
        grn=cv2.inRange(cv_image,Grn_L_limit,Grn_U_limit)
        red=cv2.inRange(cv_image,Red_L_limit,Red_U_limit)
        blk=cv2.inRange(cv_image,Blk_L_limit,Blk_U_limit)


        kernel = np.ones((5, 5), np.uint8)
        red = cv2.morphologyEx(red, cv2.MORPH_OPEN, kernel)
        grn = cv2.morphologyEx(grn, cv2.MORPH_OPEN, kernel)
        blk = cv2.morphologyEx(blk, cv2.MORPH_OPEN, kernel)


        red = cv2.GaussianBlur(red, (11,11), 0)
        grn = cv2.GaussianBlur(grn, (11,11), 0)
        blk = cv2.GaussianBlur(blk, (11,11), 0)


        ret, red_thresh = cv2.threshold(red, 230, 255, cv2.THRESH_BINARY)
        ret, grn_thresh = cv2.threshold(grn, 230, 255, cv2.THRESH_BINARY)
        ret, blk_thresh = cv2.threshold(blk, 230, 255, cv2.THRESH_BINARY)

        red_blur = cv2.blur(red_thresh, (10,10))
        grn_blur = cv2.blur(grn_thresh, (10,10))
        blk_blur = cv2.blur(blk_thresh, (10,10))

        ret2, red_thresh2 = cv2.threshold(red_blur, 1, 255, cv2.THRESH_OTSU)
        ret2, grn_thresh2 = cv2.threshold(grn_blur, 1, 255, cv2.THRESH_OTSU)
        ret2, blk_thresh2 = cv2.threshold(blk_blur, 1, 255, cv2.THRESH_OTSU)

        red_contours, red_heirarchy = cv2.findContours(red_thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        grn_contours, grn_heirarchy = cv2.findContours(grn_thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        blk_contours, grn_heirarchy = cv2.findContours(blk_thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        red_edges = cv2.Canny(image=red_thresh2, threshold1=100, threshold2=200)
        grn_edges = cv2.Canny(image=grn_thresh2, threshold1=100, threshold2=200)
        blk_edges = cv2.Canny(image=blk_thresh2, threshold1=100, threshold2=200)
        
        if len(red_contours) != 0:
            red_frame = cv_image
            print("red cont: ")#, red_contours)
            #r = max(red_contours, key = cv2.contourArea)
            #cv2.drawContours(red_frame, r, -1, 255, 3)
            #cv2.imshow("Red Contour", red_frame)
            detection = PoseStamped()
            detection.header = "mb_marker_buoy_red"
            detection.pose.x = coordinates.latitude
            detection.pose.y = coordinates.longitude
            detected.publish(detection)

            self.scan = self.create_subscription(
                LaserScan, "/wamv/sensors/lidars/lidar_wamv_sensor/scan", self.laser_scan_callback, 10)
            coordinates = self.gps.get_msg()

        if len(grn_contours) != 0:
            grn_frame = cv_image
            print("green cont: ")#,grn_contours)
            #g = max(grn_contours, key = cv2.contourArea)
            #cv2.drawContours(grn_frame, g, -1, 255, 3)
            #cv2.imshow("Green Contour", grn_frame)
            is_grn = True

        if len(blk_contours) != 0:
            blk_frame = cv_image
            print("black cont: ")#,blk_contours)
            #b = max(blk_contours, key = cv2.contourArea)
            #cv2.drawContours(blk_frame, b, -1, 255, 3)
            #cv2.imshow("black Contour", blk_frame)
            is_blk = True
            
        
        # Display the image using OpenCV
        cv2.imshow("Front Left Camera", cv_image)
        cv2.waitKey(1)
    



    def perception(self):
        print("perception.py")
        self.subscription = self.create_subscription(Image,'/wamv/sensors/cameras/front_left_camera_sensor/image_raw',self.image_callback,10)
        self.bridge = CvBridge()
"""

    def waypoint(self):
        print("wayppoint.py")
        task_info_sub = self.create_subscription(PoseArray, "/vrx/wayfinding/waypoints", self.waypoint_callback, 10)
        #imu = self.create_subscription(Imu, "/wamv/sensors/imu/imu/data", self.imu_callback, 10) 
        

    def station_callback(self, data):
        print("Station callback") 
        self.gps = self.create_subscription(
            NavSatFix, "/wamv/sensors/gps/gps/fix", self.gps_callback, 10)
        self.imu = self.create_subscription(
            Imu, "/wamv/sensors/imu/imu/data", self.imu_callback, 10)
        
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
            if(not rclpy.ok()):
                break
            
    def station(self):
        print("Station Keeping") 
        super().__init__("gps_navigator")
        print("node init")
        task_info_sub = self.create_subscription(
            GeoPoseStamped, "/vrx/station_keeping/goal", self.station_callback, 10)
        while (rclpy.ok() and not self.all_done):
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

#    def tasks(self):
 #       print("tasks") 
  #      super().__init__("gps_navigator")
   #     task_info_sub = self.create_subscription(
    #        Task, "/vrx/task/info", self.task_callback, 10) #need to import libraries
     #   while (rclpy.ok() and not self.all_done):
      #      time.sleep(0.1)

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

#    def position_hold(self, bearing, lat, long):
 #       self.left_front = self.create_publisher(Float32, '/wamv/thrusters/left/thrust', 10)
  #      self.left_back = self.create_publisher(Float32, '/wamv/thrusters/left/thrust', 10)
   #     self.right_front = self.create_publisher(Float32, '/wamv/thrusters/right/thrust', 10)
    #    self.right_back = self.create_publisher(Float32, '/wamv/thrusters/right/thrust', 10)
#
 #       if(self.current_lat<lat-0.00005):
  #          self.right_front.publish(0.1)
   #         self.right_back.publish(0.1)
    #        self.left_front.publish(0.1)
     #       self.left_back.publish(0.1)
      #  if(self.current_lat>lat+0.00005):
       #     self.right_front.publish(-0.1)
        #    self.right_back.publish(-0.1)
         #   self.left_front.publish(-0.1)
          #  self.left_back.publish(-0.1)
#
 #       angle_thr = self.ANGLE_THR
  #      angle_diff = bearing - rotation #where is this rotation coming from?
   #     if ((angle_diff) > angle_thr):
    #        self.right_front.publish(self.speed1)
     #       self.right_back.publish(self.speed1)
      #      self.left_front.publish(self.speed2)
       #     self.left_back.publish(self.speed2)
        #    print("turning anticlockwise")
#        elif ((angle_diff) < -angle_thr):
 #           self.left_front.publish(self.speed1)
  #          self.left_back.publish(self.speed1)
#
def main(target_lat,target_lon):
    rclpy.init(args=None)
    try:
        navigator = GPS_Nav()
        navigator.gps_navigator(target_lat,target_lon)
        rclpy.spin(navigator)
    except KeyboardInterrupt:
        pass
    
     
if __name__ == "__main__":
    target_lat = float(input("Latitude: "))
    target_lon = float(input("Longitude: "))
    main(target_lat,target_lon)