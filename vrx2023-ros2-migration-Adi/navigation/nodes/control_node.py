#!/usr/bin/env python3.8

from std_msgs.msg import Float32
from geographic_msgs.msg import WayPoint
from geographic_msgs.msg import GeoPoint
from geographic_msgs.msg import KeyValue[]
from uuid_msgs.msg import UniqueID


def velocity_callback(data):
   	global x_linear
   	global z_angular
    x_linear = data.linear.x #goes straight
    z_angular = data.angular.z #turning speed/yaw?
    
    lrthrust.publish(x_linear)
	rrthrust.publish(x_linear)
	lfthrust.publish(x_linear)
	rfthrust.publish(x_linear)
		
	lrangle.publish(z_angular)
	rrangle.publish(z_angular)
	lfangle.publish(z_angular)
	rfangle.publish(z_angular)
    
def control_node():
    rospy.init_node('control_node', anonymous=True)
    
    lrthrust = rospy.Publisher('/wamv/thrusters/left_rear_thrust_cmd', Float32, queue_size=10)
    rrthrust = rospy.Publisher('/wamv/thrusters/right_rear_thrust_cmd', Float32, queue_size=10)
    lfthrust = rospy.Publisher('/wamv/thrusters/left_front_thrust_cmd', Float32, queue_size=10)
    rfthrust = rospy.Publisher('/wamv/thrusters/right_front_thrust_cmd', Float32, queue_size=10)
    
    lrangle = rospy.Publisher('/wamv/thrusters/left_rear_thrust_angle', Float32, queue_size=10)
    rrangle = rospy.Publisher('/wamv/thrusters/right_rear_thrust_angle', Float32, queue_size=10)
    lfangle = rospy.Publisher('/wamv/thrusters/left_front_thrust_angle', Float32, queue_size=10)
    rfangle = rospy.Publisher('/wamv/thrusters/right_front_thrust_angle', Float32, queue_size=10)

    rospy.Subscriber("twist_cmd", Twist, velocity_callback)
    
    rate = rospy.Rate(10) # 10hz
    
    # Loop to keep the program from shutting down unless ROS is shut down, or CTRL+C is pressed
    rospy.spin()
    

if __name__ == '__main__':
	x_linear = 0
	z_angular = 0
    control_node()
   
    
    
