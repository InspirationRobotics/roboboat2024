#testing functionality of the classes within "floating_objects"

from floating_objects import Object_Colors, Object_Types, Floating_Object
from testing_objects import *
import numpy as np
#import rospya
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import String
from std_msgs.msg import Float64
from obj_msg.msg import MapInfo
from obj_msg.msg import Obj
from obj_msg.msg import Objlst
from obj_msg.msg import BinaryMap
from geometry_msgs.msg import Point


import json

class testing_mission_comms(Node):
    def __init__(self):
        super().__init__('testing_mission_comms')
        self.generate_buoys_for_testing()
        self.point_publisher_ = self.create_publisher(Point, '/wamv/path/boat_point', 10)
        self.map_publisher_ = self.create_publisher(BinaryMap, '/wamv/path/vmap', 10)
        self.floating_objects_publisher_ = self.create_publisher(Objlst, '/wamv/path/floating_objects',10)

        timer_period = 1
        self.timer = self.create_timer(timer_period, self.timer_callback)


    def timer_callback(self):
        self.publish_map()
        self.publish_points()
        self.publish_floating_objects()

    def publish_map(self):
        aMap = BinaryMap()

        aMap.objects = [0]*(100*100)
        aMap.m.origin_lat = 0.0
        aMap.m.origin_lon = 0.0
        aMap.m.hdg = np.pi/2
        aMap.m.density = 1.0
        aMap.m.w = 100
        aMap.m.h = 100
        #print(aMap)
        self.map_publisher_.publish(aMap)

    def publish_points(self):
        aPoint = Point()
        aPoint.x = 1300.0
        aPoint.y = 1300.0
        #print(aPoint)
        self.point_publisher_.publish(aPoint)
    
    def publish_floating_objects(self):
        anObjlst = Objlst()
        self.prepare_obj_list(anObjlst)
        print(anObjlst)
        self.floating_objects_publisher_.publish(anObjlst)

    def generate_buoys_for_testing(self):
        self.list_of_buoys = []
        #bouyes_loc = np.array([[[10,10],[20,10]],[[10,15], [20,15]]])
        #self.list_of_buoys = create_list(bouyes_loc)
        self.list_of_buoys = [Floating_Object(Object_Colors.PURPLE,[150,1000],Object_Types.WILDLIFE_CROCODILE)]
        self.list_of_buoys = self.list_of_buoys+[Floating_Object(Object_Colors.PURPLE,[140,1150],Object_Types.WILDLIFE_PLATYPUS)]
        self.list_of_buoys = self.list_of_buoys+[Floating_Object(Object_Colors.PURPLE,[200,1250],Object_Types.WILDLIFE_TURTLE)]

        
        """
        bouyes_loc = np.array([[[270,180],[180,110],[100,100],[120,280],[250,250],[300,100]],[[180,60],[100,350],[350,50],[350,180],[300,320],[140,340]]])
        self.list_of_buoys = create_list(bouyes_loc) + self.list_of_buoys
        purple_buoys = create_list_color(np.array([[500,200], [500, 600]]), Object_Colors.PURPLE)
        white_buoys = create_list_color(np.array([[70,100], [60,300], [80,50],[90,370]]), Object_Colors.WHITE)
        #white_buoys = create_list_color(np.array([[7,10], [6,30], [9,37]]), Object_Colors.WHITE)
        #gate_buoys = create_list_color(np.array([[70,70], [70,80]]), Object_Colors.WHITE)
        self.list_of_buoys = self.list_of_buoys+white_buoys
        """
        
        
        bouyes_loc = np.array([[[1200,800]],[[1200,1100]]])
        self.list_of_buoys = self.list_of_buoys + create_list(bouyes_loc)
        self.list_of_buoys = self.list_of_buoys + create_list_color(np.array([[1200,900], [1200,1000]]), Object_Colors.WHITE)
        self.list_of_buoys = self.list_of_buoys + create_list_color(np.array([[1000,950]]), Object_Colors.BLACK)
        self.list_of_buoys = self.list_of_buoys + [Floating_Object(Object_Colors.PURPLE,[1210,1020],Object_Types.BEACON)]
        
        #self.list_of_buoys = self.list_of_buoys+white_buoys#+gate_buoys
        #self.list_of_buoys = self.list_of_buoys+purple_buoys
        
    
    def prepare_obj_list(self, anObjlst):
        for i in self.list_of_buoys:
            newObj = Obj()
            newObj.type = int(i.type)
            newObj.color = int(i.color)
            newObj.w = int(i.location[0])
            newObj.h = int(i.location[1])
            anObjlst.objects.append(newObj)

def main(args=None):
    rclpy.init()
    map = testing_mission_comms()

    rclpy.spin(map)
    print(rclpy)
if __name__ == '__main__':
    main()
