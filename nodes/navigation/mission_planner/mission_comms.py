
import rclpy
from rclpy.node import Node
from starAlgorithm.Astar import *
import numpy as np
from floating_objects import Object_Colors, Object_Types, Floating_Object
from mission_planner import *
from obj_msg.msg import *
from geometry_msgs.msg import *
from sensor_msgs.msg import Image
from geometry_msgs.msg import Vector3

class mission_comms(Node):

    def __init__(self):
        super().__init__('mission_comms')
        self.theMissions = mission_planner([],[])
        self.vmap_sub = self.create_subscription(
            BinaryMap,
            '/wamv/path/vmap',
            self.map_callback,
            10)
        self.vmap_sub  # prevent unused variable warning
        """
        self.pose_sub = self.create_subscription(
            Vector3,
            '/boat_pos_map_frame',
            self.pose_callback,
            10)
        self.pose_callback
        """
        self.pose_sub = self.create_subscription(
            Point,
            '/wamv/path/boat_point',
            self.pose_callback,
            10)
        self.pose_callback
        
        
        
        
        self.map_path = self.create_publisher(VectorArray, '/map_path', 10)

        
        

        self.floating_object_sub = self.create_subscription(
            Objlst,
            '/wamv/path/floating_objects',
            self.floating_objects_callback,
            10)
        
        
        self.ocupancy_map_sub = self.create_subscription(
            Image,
            '/slam_occupancy_grid_map',
            self.ocupancy_map_callback,
            1)
        self.ocupancy_map_sub
        


        self.floating_objects_callback
        self.map = None
        self.pose = []
        self.floating_object = []
        timer_period = 1
        self.timer = self.create_timer(timer_period, self.update_info)

    def update_info(self):
        tic = time.time()
        self.theMissions.check_mission_readiness(self.floating_object,self.map)
        desired_path = self.theMissions.do_a_mission(np.array(self.pose))
        if desired_path is None:
            return
        forOcupiedSpaces = VectorArray()
        forOcupiedSpaces.vec3list = [Vector3()]*np.shape(desired_path)[0]

        for i in range(np.shape(desired_path)[0]):
            tempObject = Vector3()
            tempObject.x = float(desired_path[i][0])
            tempObject.y = float(desired_path[i][1])
            tempObject.z = float(0)
            forOcupiedSpaces.vec3list[i] = tempObject

        self.map_path.publish(forOcupiedSpaces)
        
    def map_callback(self, message):
        my_map = np.array(message.objects)
        my_map = np.resize(my_map,(message.m.w, message.m.h)).astype('uint8')
        #self.map = my_map

    def ocupancy_map_callback(self, message):
        #print(message.height)
        #print(message.width)
        #print(message.encoding)
        self.map = message
        pass
    
    def pose_callback(self, message):
        self.pose = [message.y, message.x]

    def floating_objects_callback(self, message):
        self.floating_object = []
        for i in message.objects:
            self.floating_object.append(Floating_Object(i.color,np.array([i.w, i.h]),i.type))

def main(args=None):
    rclpy.init(args=args)

    the_mission_comms = mission_comms()

    rclpy.spin(the_mission_comms)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    the_mission_comms.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
